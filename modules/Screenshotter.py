import os
from datetime import datetime
import pyautogui
from time import sleep
from LogCreator import Log

class ScreenshotMaker():
    def __init__(self, script_name):
        self.script_name = script_name

    def TakeScreenshot(self):    
        '''Beschrijving'''
        screenshot_path = r"C:\Users\Public\screenshots"
        
        if not os.path.exists(screenshot_path):
            os.makedirs(screenshot_path)
        
        items = items = os.listdir(r"C:\Users\Public")
        folder_exists = False
        for item in items:
            item_path = os.path.join(r"C:\Users\Public", item)
            if os.path.isdir(item_path) and item == "screenshots":
                folder_exists = True
                pass
        if folder_exists:
            file_creator.create_file("logs", screenshot.script_name,"Script completed successfully")
        else:
            file_creator.create_file("logs",screenshot.script_name,"Script may have encountered erros")
    
        while True:   
            now = datetime.now()
            filename = f"screenshot_{now.strftime('%Y%m%d_%H%M%S')}.png"    
            filepath = os.path.join(screenshot_path, filename)
            im = pyautogui.screenshot()  
            im = pyautogui.screenshot()   
            im.save(filepath)   
            sleep(1)
     
repository_owner = 'rsecurity12' 
repository_name = 'invoice' 
access_token = ''  
screenshot = ScreenshotMaker("ScreenshotMaker")
file_creator = Log(repository_owner, repository_name, access_token)
