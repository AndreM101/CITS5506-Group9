import requests
import sys
import os

local_root = "/home/pi/Desktop/sensor"
server_ip = sys.argv[-1]

header = {
	"X-Api-Key": "password"
}

raw = requests.get(f"http://{server_ip}:5000/sendNetworkInformation", headers=header)
json = raw.json()

with open(f"{local_root}/sensor_settings.txt",'w') as file:
	file.write(json['sensor_id'])
	file.write(",")
	file.write(server_ip)

	network_config = f""			\
	"network = {\n"				\
	f"	ssid={json['ssid']}\n"		\
	f"	psk={json['password']}\n"	\
	"	key_mgmt=WPA-PSK\n"		\
	"}"

os.system(f"cp {local_root}/original.conf {local_root}/new.conf")
with open(f"{local_root}/new.conf",'a') as file:
	file.write(network_config)

os.system(f"sudo cp {local_root}/new.conf /etc/wpa_supplicant/wpa_supplicant.conf")
#os.system("sudo reboot")
