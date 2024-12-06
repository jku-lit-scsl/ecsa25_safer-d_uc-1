import datetime
import logging
import os.path
import time
import uuid
from pathlib import Path

import psutil
import pytz

import config.config as CONFIG

PROJ_ROOT = proj_root = Path(__file__).parent.parent


def setup_logging():
    # Remove any existing handlers
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    # Create a StreamHandler for console output
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s', '%Y-%m-%d %H:%M:%S')
    console_handler.setFormatter(console_formatter)

    # Create a FileHandler for logging to a file
    log_file_path = os.path.join('logs',
                                 f"{generate_timestamp_for_filename()}_{CONFIG.network_conf['my_ip']}_efficacy_eval.log")
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
    file_handler = logging.FileHandler(log_file_path, mode='w')
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter('%(asctime)s.%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                                       '%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(file_formatter)

    # Add both handlers to the root logger
    logger = logging.getLogger()
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)


def get_cpu_usage() -> float:
    """Returns the CPU usage in percent"""
    return psutil.cpu_percent(interval=None)


def get_virtual_memory() -> float:
    """Returns the memory usage in percent"""
    return psutil.virtual_memory().percent
    # you can calculate percentage of available memory
    # psutil.virtual_memory().available * 100 / psutil.virtual_memory().total


def generate_timestamp_for_filename():
    """
    Generates a timestamp string suitable for use in filenames.

    :return: A string representing the current date and time in a filename-safe format.
    """
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


latency_log_file = f"{generate_timestamp_for_filename()}_log_file.txt"


def write_latency_log(log_string: str, file_name=os.path.join(PROJ_ROOT, latency_log_file)):
    """
    Appends the given log string to a log file.

    :param log_string: The log message to write to the file.
    :param file_name: The name of the file to which the log will be written. Default is the latency logfile generated with a timestamp
    """
    with open(file_name, "a") as file:
        file.write(f'{generate_timestamp_for_filename}    {log_string}\n')


def get_current_time_in_millis() -> int:
    """Returns the current time in milliseconds"""
    return time.time_ns() // 1_000_000


def singleton(class_):
    """Introduces a singleton decorator"""

    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


class Singleton(type):
    """Impl. of a singleton design pattern"""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def generate_unique_id():
    """Returns a unique id"""
    return uuid.uuid4().__str__()


def get_current_time():
    """Returns the current time"""
    tz = pytz.timezone('Europe/Vienna')
    return datetime.datetime.now(tz).__str__()
