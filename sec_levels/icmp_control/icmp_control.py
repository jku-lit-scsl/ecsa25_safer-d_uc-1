import logging
import threading
import time

from scapy.all import sniff
from scapy.layers.inet import IP, ICMP

from util.utils import setup_logging


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
            self._pause_event.wait()  # Block while paused
            sniff(filter="icmp", prn=process_packet, store=False, stop_filter=lambda p: self._stop_event.is_set())

    def pause(self):
        """Pauses the thread."""
        self._pause_event.clear()

    def resume(self):
        """Resumes the thread."""
        self._pause_event.set()

    def stop(self):
        """Stops the thread."""
        self._stop_event.set()
        self._pause_event.set()  # Ensure thread can exit even if paused


if __name__ == '__main__':
    setup_logging()
    icmp_thread = ICMPLogThread()
    icmp_thread.start()
    time.sleep(20)
    print("pausing now")
    icmp_thread.pause()
    time.sleep(20)
    print("stopped pausing")
    icmp_thread.resume()
