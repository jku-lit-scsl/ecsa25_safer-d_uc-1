import logging
import threading
import time
from collections import defaultdict

from scapy.all import sniff
from scapy.layers.inet import IP, ICMP

from util.utils import setup_logging


def handle_ping(src_ip):
    # here could be further processing, for demonstration purposes, we just log the ping
    logging.info(f"Ping from {src_ip}")


class ICMPThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self._pause_event = threading.Event()  # Used to pause the thread
        self._pause_event.set()  # Initially not paused
        self._stop_event = threading.Event()  # Used to stop the thread

    def pause(self):
        """Pauses the thread."""
        logging.info("Pausing ICMP monitors...")
        self._pause_event.clear()

    def resume(self):
        """Resumes the thread."""
        logging.info("Resuming ICMP monitors...")
        self._pause_event.set()

    def stop(self):
        """Stops the thread."""
        logging.info("Stopping ICMP monitors...")
        self._stop_event.set()
        self._pause_event.set()  # Ensure the thread is not blocked on pause


class ICMPThreadMonitor(ICMPThread):
    def __init__(self):
        super().__init__()

    def run(self):
        """Starts the packet sniffing process."""

        def process_packet(packet):
            """Callback to handle each sniffed packet."""
            if packet.haslayer(IP) and packet.haslayer(ICMP) and packet[ICMP].type == 8:  # Type 8 is echo request
                src_ip = packet[IP].src
                handle_ping(src_ip)

        while not self._stop_event.is_set():
            # Check if the thread is paused
            if not self._pause_event.is_set():
                time.sleep(0.1)  # Wait until resume
                continue

            # Sniff with a timeout to allow for state checks
            sniff(filter="icmp", prn=process_packet, store=False, timeout=1)


class ICMPThreadRateLimiting(ICMPThread):
    def __init__(self, rate_limit_window, max_pings_in_window):
        """

        :param rate_limit_window: sliding window in seconds to check
        :param max_pings_in_window: the amount of pings allowed within the sliding window
        """
        super().__init__()
        self.rate_limiter = defaultdict(list)
        self.rate_limit_window = rate_limit_window
        self.max_pings_in_window = max_pings_in_window

    def is_ip_valid(self, src_ip):
        """Enforce rate limiting"""
        now = time.time()
        self.rate_limiter[src_ip] = [t for t in self.rate_limiter[src_ip] if
                                     now - t < self.rate_limit_window]  # sliding window
        if len(self.rate_limiter[src_ip]) >= self.max_pings_in_window:  # Max pings per second
            return False
        self.rate_limiter[src_ip].append(now)
        return True

    def run(self):
        """Starts the packet sniffing process."""

        def process_packet(packet):
            """Callback to handle each sniffed packet."""
            if packet.haslayer(IP) and packet.haslayer(ICMP) and packet[ICMP].type == 8:  # Type 8 is echo request
                src_ip = packet[IP].src
                if self.is_ip_valid(src_ip):
                    handle_ping(src_ip)
                else:
                    logging.warning(f"Rate limit exceeded for {src_ip}. Dropping packet.")

        while not self._stop_event.is_set():
            # Check if the thread is paused
            if not self._pause_event.is_set():
                time.sleep(0.1)  # Wait until resume
                continue

            # Sniff with a timeout to allow for state checks
            sniff(filter="icmp", prn=process_packet, store=False, timeout=1)


class ICMPThreadBlocker(ICMPThread):
    def __init__(self):
        super().__init__()

    def run(self):
        """Starts the packet sniffing process."""

        def process_packet(packet):
            """Callback to handle each sniffed packet."""
            logging.warning("Blocked ICMP packet.")

        while not self._stop_event.is_set():
            # Check if the thread is paused
            if not self._pause_event.is_set():
                time.sleep(0.1)  # Wait until resume
                continue

            # Sniff with a timeout to allow for state checks
            sniff(filter="icmp", prn=process_packet, store=False, timeout=1)


if __name__ == '__main__':
    setup_logging()
    icmp_thread = ICMPThreadBlocker()
    icmp_thread.start()
