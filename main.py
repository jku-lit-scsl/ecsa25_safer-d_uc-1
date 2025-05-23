import json
import logging
import sys
import time

import requests
from requests import RequestException

import config.config as CONFIG
from sec_levels.DefconHandler import DefconHandler
from server.server import start_flask_server
from util.utils import setup_logging

ips_to_check = []
number_of_subsystems = -1
defcon_handler = DefconHandler()
in_SoS_Mode = False


def switch_to_sos_mode(ip):
    global in_SoS_Mode
    logging.warning(f"Could not reach ip: {ip}")
    if not in_SoS_Mode:
        # perform meta-adaptation scale down to smaller SoS subsystem
        logging.info("Switching to SoS mode")
        in_SoS_Mode = True
        init_ip_tree()


def check_adaptations():
    """
    Checks all the related subsystems for criticality
    :return: void
    """
    global ips_to_check
    logging.info('Checking adaptations...')
    current_own_sec_level = defcon_handler.get_current_security_level().value
    ip_sec_levels = []
    for ip in ips_to_check:
        try:
            response = requests.get(f"http://{ip}:5000/get_security_level", timeout=3)
            if response.status_code == 200:
                criticality_to_check = int(json.loads(response.text)['criticality'])
                ip_sec_levels.append(criticality_to_check)
            else:
                switch_to_sos_mode(ip)
                break
        except RequestException:
            switch_to_sos_mode(ip)
            break

    max_criticality = -1
    if len(ip_sec_levels) > 0:
        max_criticality = max(ip_sec_levels)

    if max_criticality > current_own_sec_level:
        defcon_handler.increase_security_level(max_criticality)
        logging.warning(f"Checked adaptations: New criticality: {max_criticality}")
    else:
        logging.info("Checked adaptations: no adaptations required.")


def traverse_parent_ips(parent_ip):
    global ips_to_check
    # add ips to the list
    try:
        response = requests.get(f"http://{parent_ip}:5000/get_parent_ip", timeout=3)
        if response.status_code == 200:
            ips_to_check.append(parent_ip)
            new_parent_ip = json.loads(response.text)['parent_ip']
            traverse_parent_ips(new_parent_ip)
        elif response.status_code == 404:
            ## reached the top
            ips_to_check.append(parent_ip)
        else:
            logging.error(f"Unknown statuscode: {response.status_code}")
    except RequestException:
        # Handle any request-related errors
        logging.error(f"{parent_ip} is currently unreachable")


def traverse_child_ips(child_ip):
    # add ips to the list
    try:
        global ips_to_check
        response = requests.get(f"http://{child_ip}:5000/get_child_ips", timeout=3)
        if response.status_code == 200:
            ips_to_check.append(child_ip)
            new_child_ip_list = json.loads(response.text)['child_ips']
            for child_ip in new_child_ip_list:
                traverse_child_ips(child_ip)
        elif response.status_code == 404:
            ## reached the leaf
            ips_to_check.append(child_ip)
        else:
            logging.error(f"Unknown statuscode: {response.status_code}")
    except RequestException:
        # Handle any request-related errors
        logging.error(f"{child_ip} is currently unreachable")


def init_ip_tree(is_first_init=False):
    """
    Traverses once through the hierarchy and gets the ip addresses to check for adaptation
    :return: void
    """
    global ips_to_check, number_of_subsystems
    ips_to_check = []

    if CONFIG.parent_ip != '':
        traverse_parent_ips(parent_ip=CONFIG.parent_ip)

    if len(CONFIG.child_ips) > 0:
        for child_ip in CONFIG.child_ips:
            traverse_child_ips(child_ip=child_ip)

    if is_first_init:
        logging.info(f"Initializing IP tree with following IP addresses:{ips_to_check}")
        number_of_subsystems = len(ips_to_check)


def setup():
    #### SETUP
    # logging
    setup_logging()
    # log ips
    logging.info(f"MY-IP={CONFIG.my_ip}")
    logging.info(f"PARENT-IP={CONFIG.parent_ip}")
    logging.info(f"CHILDREN-IP={CONFIG.child_ips}")
    # flask
    start_flask_server()


if __name__ == "__main__":
    setup()
    # just in case wait for the other systems to come up
    time.sleep(30)
    # parse entire hierarchy once
    init_ip_tree(True)
    if len(ips_to_check) == 0:
        logging.error('Did not find any ips to check for adaptation. ABORTING')
        sys.exit(0)

    while True:
        check_adaptations()

        # to iteratively check to get back to normal mode every minute
        if in_SoS_Mode:
            init_ip_tree()
            if len(ips_to_check) == number_of_subsystems:
                # connection back to all the relevant systems is possible -> adapt back to normal
                in_SoS_Mode = False
                logging.info("Left SoS mode")
            else:
                logging.info(f"Adapting within SoS mode with following IPs: {ips_to_check}")

        time.sleep(10)
