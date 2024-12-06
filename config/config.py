import logging
import socket


def get_local_ip():
    try:
        # Create a socket and connect to a known public IP
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))  # Google DNS
            return s.getsockname()[0]
    except Exception as e:
        return f"Error: {e}"


def determine_parent_ip(ip):
    if ip == "192.168.56.20":
        return ''
    elif "192.168.56.24" or "192.168.56.28":
        return '192.168.56.20'
    else:
        logging.error(f'Could not determine parent IP for {ip}')


def determine_child_ip(ip):
    if ip == "192.168.56.20":
        return ['192.168.56.24', '192.168.56.28']
    else:
        logging.error(f'Could not determine child IPs for {ip}')


my_ip = get_local_ip()
parent_ip = determine_parent_ip(my_ip)
child_ips = determine_child_ip(my_ip)
