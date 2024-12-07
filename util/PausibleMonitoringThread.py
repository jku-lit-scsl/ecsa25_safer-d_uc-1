import logging
import threading
import time

from util.utils import get_monitor_instance


class PausableMonitoringThread(threading.Thread):
    def __init__(self, interval):
        super().__init__()
        self._pause_event = threading.Event()  # Used to pause the thread
        self._pause_event.set()  # Initially not paused
        self._stop_event = threading.Event()  # Used to stop the thread
        self.interval = interval

    def run(self):
        while not self._stop_event.is_set():
            self._pause_event.wait()  # Block while paused
            logging.info(get_monitor_instance())
            time.sleep(self.interval)  # Simulate some work

    def pause(self):
        self._pause_event.clear()  # Clear the pause event to pause the thread

    def resume(self):
        self._pause_event.set()  # Set the pause event to resume the thread

    def stop(self):
        self._stop_event.set()  # Set the stop event to exit the thread
        self._pause_event.set()  # Ensure thread can exit even if paused
