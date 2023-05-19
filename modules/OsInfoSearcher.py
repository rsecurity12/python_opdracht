import ctypes
import platform
import subprocess
import os

class OperationalSystemInfo():
    def gather_windows_info():  
        ## beschrijving ##
        output_file = r"C:\Users\Public\gather_info.txt"
        screenshot_path = r"C:\Users\Public\gather_info"
        if not os.path.exists(screenshot_path):
            os.makedirs(screenshot_path)   
    
        output_file = open(r"C:\Users\Public\gather_info\windows_info.txt", "w")
       
        os_name = platform.system()
        os_version = platform.release()
        os_details = platform.version()
        gather_admin_result = subprocess.run(["net", "localgroup", "administrators"], capture_output=True, text=True)
        gather_user_result = subprocess.run(["net", "users"], capture_output=True, text=True)

        try:
            ctypes.windll.shell32.IsUserAnAdmin() != 0
            output_file.write("User has administrative privileges\n\n")
        except:
            output_file.write("User does not have administrative privileges\n\n")
    
        output_file.write(f"OS Name: {os_name}\n\n")
        output_file.write(f"OS Version: {os_version}\n\n")
        output_file.write(f"OS Details: {os_details}\n\n")
        output_file.write(f"Admin group: {gather_admin_result.stdout}\n\n")    
        output_file.write(f"Users in the target: {gather_user_result.stdout}\n\n") 

        output_file.close()

  
    def gather_windows_info():
        ## beschrijving ##
        output_file = "/tmp/linux_info.txt"
        destination_directory = "/tmp/linux_info"
        if not os.path.exists(destination_directory):
            os.makedirs(destination_directory)
       
        output_file = open("/tmp/linux_info/linux_info.txt", "w")
    
        os_name = subprocess.check_output(['uname', '-s']).decode().strip()
        os_version = subprocess.check_output(['uname', '-r']).decode().strip()
        os_details = subprocess.check_output(['uname', '-a']).decode().strip()
        gather_user_result = subprocess.run(['cat', '/etc/passwd'], capture_output=True, text=True)
        gather_admin_result = subprocess.run(['getent', 'group', 'sudo'], capture_output=True, text=True)
    
        try:
            subprocess.run(['which', 'systemctl'], check=True)
            output_file.write("Systemd is installed\n\n")
        except subprocess.CalledProcessError:
            output_file.write("Systemd is not installed\n\n")

        try:
            subprocess.run(['which', 'ufw'], check=True)
            output_file.write("UFW is installed\n\n")
        except subprocess.CalledProcessError:
            output_file.write("UFW is not installed\n\n")

        try:
            subprocess.run(['which', 'selinuxenabled'], check=True)
            subprocess.run(['selinuxenabled'], check=True)
            output_file.write("SELinux is enabled\n\n")
        except subprocess.CalledProcessError:
            output_file.write("SELinux is not enabled\n\n")

        output_file.write(f"OS Name: {os_name}\n\n")
        output_file.write(f"OS Version: {os_version}\n\n")
        output_file.write(f"OS Details: {os_details}\n\n")
        output_file.write(f"Users in the system: {gather_user_result.stdout}\n\n")
        output_file.write(f"Users with sudo privileges: {gather_admin_result.stdout}\n\n")
    
        output_file.close()

