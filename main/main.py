# Created on 06.12.2024
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
    print("Response from /:", response.text)
    pass


def init_ip_tree():
    """
    Traverses once through the hierarchy and gets the ip addresses to check for adaptation
    :return: void
    """
    if CONFIG.parent_ip != '':
        traverse_parent_ips(parent_ip=CONFIG.parent_ip)



if __name__ == "__main__":
    setup_logging()
    init_ip_tree()
    while True:
        check_adaptations()
