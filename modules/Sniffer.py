import os
from scapy.all import *

class Sniffer():
    def __init__(self, script_name):
        self.script_name = script_name
        self.packets = []

    def packet_handler(self, packet):
        destination_directory = "/tmp/results"
        if not os.path.exists(destination_directory):
           os.makedirs(destination_directory)
            
        if packet.haslayer(IP):
            src_ip = packet[IP].src
            dst_ip = packet[IP].dst
            output = f"Source IP: {src_ip}  Destination IP: {dst_ip}\n"

            if packet.haslayer(TCP):
                src_port = packet[TCP].sport
                dst_port = packet[TCP].dport
                output += f"Source Port: {src_port}  Destination Port: {dst_port}\n"

                data = packet[TCP].payload
                output += f"Data: {repr(data)}\n"
            
            new_packet = IP(src=src_ip, dst=dst_ip) / TCP(sport=src_port, dport=dst_port) / Raw(load=str(data))

            self.packets.append(new_packet)    
            wrpcap("/tmp/results/output.pcap", self.packets)
                
    def Run_Sniffer(self):
        sniff(filter="tcp", prn=self.packet_handler)
        
sniffer = Sniffer('Sniffer')
sniffer.Run_Sniffer()
