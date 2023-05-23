import platform

class Invoice():
    def __init__(self):
        self.run_trojan()

    def run_trojan(self):
        system = platform.system()
        while True:
            try:
                if system == 'Windows':     
                    pass #ScreenshotMaker.TakeScreenshot(self)
                elif system == 'Linux':
                    pass ###self.run_in_background_linux()
            except KeyboardInterrupt:
                pass
    
invoice = Invoice()
