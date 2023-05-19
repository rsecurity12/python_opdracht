import os
from datetime import datetime
import pyautogui
from time import sleep

class ScreenshotMaker():
    @staticmethod
    def run():    
        '''Beschrijving'''
        screenshot_path = r"C:\Users\Public\screenshots"
        if not os.path.exists(screenshot_path):
                os.makedirs(screenshot_path) 
        while True:
            now = datetime.now()
            filename = f"screenshot_{now.strftime('%Y%m%d_%H%M%S')}.png"    
            filepath = os.path.join(screenshot_path, filename)
            im = pyautogui.screenshot()  
            im = pyautogui.screenshot()   
            im.save(filepath)   
            sleep(1)

ScreenshotMaker.run()