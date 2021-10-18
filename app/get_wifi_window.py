import subprocess 
import re  
import os        

def get_wifi_info(): 

  command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output = True).stdout.decode()

  profile_names = (re.findall("All User Profile     : (.*)\r", command_output))

  profile_info = subprocess.run(["netsh", "wlan", "show", "profile", profile_names[0]], capture_output = True).stdout.decode()
      
  ssid = profile_names[0]
      
  return ssid 

def get_password(ssid):
  command = os.system('netsh wlan show profiles {0} key=clear'.format(ssid))
  password = command["password"]
  return password 
  