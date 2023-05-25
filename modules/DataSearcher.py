import os

class DataSearcher:
    def __init__(self, script_name):
        self.script_name = script_name
        self.file_extensions = ['.txt', '.xlsx', '.docx', '.key', '.db', '.json','.pdf','.pem','.ssh','.jpg','.png','.gif','.mp4','.avi', '.mov']

    def run_data_searcher(self):
        '''Beschrijving'''
        search_path = 'C:\\Users\\rodri\\Desktop'  # Update the search path as per your requirement
        found_files = []

        data_path = r"C:\Users\Public\data"
        if not os.path.exists(data_path):
            os.makedirs(data_path)

        for dirpath, dirnames,filenames in os.walk(search_path):
            for filename in filenames:
                file_extension = os.path.splitext(filename)[1]
                if file_extension in self.file_extensions:
                    file_path = os.path.join(dirpath, filename)
                    found_files.append(file_path)

        if found_files:
            with open(os.path.join(data_path, 'found_data.txt'), 'w') as f:
                for file_path in found_files:
                    f.write(file_path + '\n')
        else:
            pass

data_searcher = DataSearcher('DataSearcher')
data_searcher.run_data_searcher()
