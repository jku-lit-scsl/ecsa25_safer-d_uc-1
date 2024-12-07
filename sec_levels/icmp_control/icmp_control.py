import logging
import threading
import time

from scapy.all import sniff
from scapy.layers.inet import IP, ICMP


class ICMPLogThread(threading.Thread):
    def __init__(self):
        super().__init__()
        self._pause_event = threading.Event()  # Used to pause the thread
        self._pause_event.set()  # Initially not paused
        self._stop_event = threading.Event()  # Used to stop the thread

    def run(self):
        """Starts the packet sniffing process."""

        def process_packet(packet):
            """Callback to handle each sniffed packet."""
            if packet.haslayer(IP) and packet.haslayer(ICMP) and packet[ICMP].type == 8:  # Type 8 is echo request
                src_ip = packet[IP].src
                logging.info(f"Ping from {src_ip}")

        while not self._stop_event.is_set():
            # Check if the thread is paused
            if not self._pause_event.is_set():
                time.sleep(0.1)  # Wait until resume
                continue

            # Sniff with a timeout to allow for state checks
            sniff(filter="icmp", prn=process_packet, store=False, timeout=1)

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
