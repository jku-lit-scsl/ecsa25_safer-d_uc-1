# Created on 06.12.2024
import json
import logging
import sys
import time

import requests

import config.config as CONFIG
from sec_levels.DefconHandler import DefconHandler
from server.server import start_flask_server
from util.utils import setup_logging

ips_to_check = []
defcon_handler = DefconHandler()


def check_adaptations():
    # traverses the
    current_own_sec_level = defcon_handler.get_current_security_level()
    ip_sec_levels = []
    for ip in ips_to_check:
        response = requests.get(f"http://{ip}:5000/get_security_level")
        if response.status_code == 200:
            criticality_to_check = int(json.loads(response.text)['criticality'])
            ip_sec_levels.append(criticality_to_check)
        else:
            logging.warning(f"Could not reach ip: {ip}")

    max_criticality = max(ip_sec_levels)

    if max_criticality > current_own_sec_level:
        logging.warning(f"Checked adaptations: New criticality: {max_criticality}")
        ## todo: adapt to the more secure

    else:
        logging.info("Checked adaptations: no adaptations required.")


def traverse_parent_ips(parent_ip):
    # add ips to the list
    ips_to_check.append(parent_ip)
    response = requests.get(f"http://{parent_ip}:5000/get_parent_ip")
    if response.status_code == 200:
        new_parent_ip = json.loads(response.text)['parent_ip']
        traverse_parent_ips(new_parent_ip)
    elif response.status_code == 404:
        ## reached the top
        return
    else:
        logging.error(f"Unknown statuscode: {response.status_code}")


def traverse_child_ips(child_ip):
    # add ips to the list
    ips_to_check.append(child_ip)
    response = requests.get(f"http://{child_ip}:5000/get_child_ips")
    if response.status_code == 200:
        new_child_ip_list = json.loads(response.text)['child_ips']
        for child_ip in new_child_ip_list:
            traverse_child_ips(child_ip)
    elif response.status_code == 404:
        ## reached the leaf
        return
    else:
        logging.error(f"Unknown statuscode: {response.status_code}")


def init_ip_tree():
    """
    Traverses once through the hierarchy and gets the ip addresses to check for adaptation
    :return: void
    """
    if CONFIG.parent_ip != '':
        traverse_parent_ips(parent_ip=CONFIG.parent_ip)

    if len(CONFIG.child_ips) > 0:
        for child_ip in CONFIG.child_ips:
            traverse_child_ips(child_ip=child_ip)


if __name__ == "__main__":
    #### SETUP
    # logging
    setup_logging()
    # flask
    start_flask_server()
    # just in case wait for the other systems to come up
    time.sleep(5)
    # parse entire hierarchy once
    init_ip_tree()
    if len(ips_to_check) == 0:
        logging.error('Did not find any ips to check for adaptation. ABORTING')
        sys.exit(0)

    while True:
        check_adaptations()
        time.sleep(10)
