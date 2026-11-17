"""
Network Sniffer Service: Uses Scapy to capture live packets in a background thread.
"""
import threading
import logging
from typing import Optional
from app.services.detector import detection_engine

logger = logging.getLogger(__name__)

class NetworkSniffer:
    def __init__(self, interface: Optional[str] = None):
        self.interface = interface
        self.is_running = False
        self.thread = None
        self.callbacks = []

    def register_callback(self, callback):
        """Register a callback function to receive alerts."""
        self.callbacks.append(callback)

    def _packet_handler(self, packet):
        try:
            alert = detection_engine.process_packet(packet)
            if alert:
                for cb in self.callbacks:
                    cb(alert)
        except Exception as e:
            logger.error(f"Error processing packet: {e}")

    def _run_sniff(self):
        try:
            from scapy.all import sniff
            print(f"Starting Scapy packet capture on interface: {self.interface or 'default'}...")
            sniff(
                iface=self.interface,
                prn=self._packet_handler,
                store=False,
                stop_filter=lambda x: not self.is_running
            )
        except Exception as e:
            logger.error(f"Failed to start sniffer: {e}")
            self.is_running = False

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.thread = threading.Thread(target=self._run_sniff, daemon=True)
            self.thread.start()

    def stop(self):
        self.is_running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2.0)
        print("Packet sniffer stopped.")

sniffer_service = NetworkSniffer()
