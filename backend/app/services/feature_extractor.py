"""
Feature Extraction Service: Aggregates captured network packets into flow-level statistics
compatible with the XGBoost Intrusion Detection Model.
"""
from collections import defaultdict
import time
import numpy as np

class FlowFeatureExtractor:
    def __init__(self, flow_timeout: float = 10.0):
        self.flow_timeout = flow_timeout
        self.flows = defaultdict(lambda: {
            "start_time": time.time(),
            "last_time": time.time(),
            "fwd_packets": [],
            "bwd_packets": [],
            "flags": defaultdict(int),
        })

    def process_packet(self, packet) -> tuple:
        """
        Processes a raw Scapy packet, groups into bi-directional flow,
        and returns (flow_key, feature_vector) if flow is ready for classification.
        """
        try:
            from scapy.layers.inet import IP, TCP, UDP
        except ImportError:
            return None, None

        if not packet.haslayer(IP):
            return None, None

        ip_layer = packet.getlayer(IP)
        src_ip = ip_layer.src
        dst_ip = ip_layer.dst
        proto = "TCP" if packet.haslayer(TCP) else ("UDP" if packet.haslayer(UDP) else "OTHER")

        src_port = 0
        dst_port = 0
        flags_str = ""

        if packet.haslayer(TCP):
            tcp = packet.getlayer(TCP)
            src_port = tcp.sport
            dst_port = tcp.dport
            flags_str = str(tcp.flags)
        elif packet.haslayer(UDP):
            udp = packet.getlayer(UDP)
            src_port = udp.sport
            dst_port = udp.dport

        flow_key = (min(src_ip, dst_ip), max(src_ip, dst_ip), min(src_port, dst_port), max(src_port, dst_port), proto)
        is_forward = (src_ip <= dst_ip)

        flow = self.flows[flow_key]
        pkt_len = len(packet)
        now = time.time()
        flow["last_time"] = now

        if is_forward:
            flow["fwd_packets"].append((now, pkt_len))
        else:
            flow["bwd_packets"].append((now, pkt_len))

        for f in flags_str:
            flow["flags"][f] += 1

        # Check if flow has enough packets or time to classify
        total_pkts = len(flow["fwd_packets"]) + len(flow["bwd_packets"])
        if total_pkts >= 5 or (now - flow["start_time"] >= self.flow_timeout):
            features = self._calculate_features(flow)
            # Reset flow window
            del self.flows[flow_key]
            metadata = {
                "src_ip": src_ip,
                "dst_ip": dst_ip,
                "src_port": src_port,
                "dst_port": dst_port,
                "protocol": proto,
                "packet_count": total_pkts
            }
            return metadata, features

        return None, None

    def _calculate_features(self, flow: dict) -> list:
        duration = max(flow["last_time"] - flow["start_time"], 0.0001)
        fwd_lens = [p[1] for p in flow["fwd_packets"]] or [0]
        bwd_lens = [p[1] for p in flow["bwd_packets"]] or [0]
        all_lens = fwd_lens + bwd_lens

        total_fwd = len(flow["fwd_packets"])
        total_bwd = len(flow["bwd_packets"])
        sum_fwd = sum(fwd_lens)
        sum_bwd = sum(bwd_lens)
        total_bytes = sum_fwd + sum_bwd

        return [
            duration,
            total_fwd,
            total_bwd,
            sum_fwd,
            sum_bwd,
            max(fwd_lens),
            min(fwd_lens),
            float(np.mean(fwd_lens)),
            total_bytes / duration,
            (total_fwd + total_bwd) / duration,
            float(np.mean(all_lens)),
            float(np.std(all_lens)),
            flow["flags"]["F"],
            flow["flags"]["S"],
            flow["flags"]["R"],
            flow["flags"]["P"],
            flow["flags"]["A"],
            flow["flags"]["U"],
            (total_bwd / total_fwd) if total_fwd > 0 else 0,
            float(total_bytes / max(total_fwd + total_bwd, 1))
        ]
