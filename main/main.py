# Created on 06.12.2024
import json
import logging
import sys

import requests

import config.config as CONFIG
from util.utils import setup_logging

ips_to_check = []


def check_adaptations():
    # traverses the
    pass


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
    # setup
    setup_logging()

    # parse entire hierarchy once
    init_ip_tree()

    if len(ips_to_check) == 0:
        logging.error('Did not find any ips to check for adaptation. ABORTING')
        sys.exit(0)

    ## ToDo continue with cyclic adaptations here
    while True:
        check_adaptations()
        # todo add timer
        break
