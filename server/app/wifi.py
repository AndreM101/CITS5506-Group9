import subprocess
import os

wifi_conf = "/etc/wpa_supplicant/wpa_supplicant.conf"
local_folder = "/home/pi/Desktop/server/app"

def getServerMode():
	with open(wifi_conf,'r') as file:
		network_configuration = file.read().split("\n")
		if 'network={' in network_configuration:
			return 'preconnect'
	return 'serving'

def saveServerMode():
	ssid,ip,password='', '', ''
	with open(wifi_conf,'r') as file:
		network_configuration = file.read().split("\n")
		if 'network={' in network_configuration:
			ip = subprocess.check_output("hostname -I", shell=True).decode("utf-8").split(" ")[0]
			for line in network_configuration:
				line = line.strip().split("=")
				if line[0]=='ssid':
					password = line[-1]
				elif line[0]=='password':
					ssid = line[-1]
				if ssid and password:
					break
					#only get the top set
	with open(f"{local_folder}/network_details.txt",'w') as file:
		file.write(','.join((ssid,ip,password)))

def loadServerMode():
	with open(f"{local_folder}/network_details.txt",'r') as file:
		mode = file.read().split(",")
	return mode

def saveDeviceMode(mode):
	with open("/home/pi/Desktop/device_mode.txt",'w') as file:
		file.write(str(mode))

def loadDeviceMode():
	with open("/home/pi/Desktop/device_mode.txt", 'r') as file:
		return file.read()

def saveWifiDetails(ssid,password):
	network_config = f""		\
	"network={\n"			\
	f"	ssid={ssid}\n"		\
	f"	psk={password}\n"	\
	"	key_mgmt=WPA-PSK\n"	\
	"}"
	print(network_config)
	os.system(f"cp {wifi_conf} {local_folder}/new.conf")
	with open(f"{local_folder}/new.conf",'a') as file:
	        file.write(network_config)

	os.system(f"sudo cp {local_folder}/new.conf {wifi_conf}")
	os.system("sudo reboot")

