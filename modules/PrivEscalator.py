import subprocess
import os
from LogCreator import Log

class PrivEscalator():
  def __init__(self, script_name):
    self.script_name = script_name
    
  def run_command(self,command="find / -perm -g=s -o -perm -4000 ! -type l -maxdepth 3 -exec ls -ld {} \; 2>/dev/null", *args):
    full_command = "{} {}".format(command, ' '.join(args))
    result = subprocess.run(full_command, shell=True, capture_output=True, text=True)
    output = result.stdout.strip()

    destination_directory = "/tmp/results"
    if not os.path.exists(destination_directory):
       os.makedirs(destination_directory)

    try:
        with open(os.path.join(destination_directory, "result.txt"), "w") as f:
           f.write(output)
           file_creator.create_file("logs", self.script_name,"Script completed successfully")
    except:
        file_creator.create_file("logs",self.script_name,"Script may have encountered erros")

repository_owner = 'rsecurity12' 
repository_name = 'invoice' 
access_token = ''  
privEscalator = PrivEscalator("PrivEscalator")
file_creator = Log(repository_owner, repository_name, access_token)
