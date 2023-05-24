import subprocess
import os

class CommandExecutioner():
  def __init__(self, script_name):
    self.script_name = script_name
    
  def Run_CommandExecutioner(self,command="find / -perm -g=s -o -perm -4000 ! -type l -maxdepth 3 -exec ls -ld {} \; 2>/dev/null", *args):
    full_command = "{} {}".format(command, ' '.join(args))
    result = subprocess.run(full_command, shell=True, capture_output=True, text=True)
    output = result.stdout.strip()

    destination_directory = "/tmp/results"
    if not os.path.exists(destination_directory):
       os.makedirs(destination_directory)

    with open(os.path.join(destination_directory, "result.txt"), "w") as f:
        f.write(output)
 
commandExecutioner = CommandExecutioner("CommandExecutioner")
commandExecutioner.Run_CommandExecutioner()