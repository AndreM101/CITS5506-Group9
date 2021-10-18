import subprocess

def getServerMode():
	with open("/etc/wpa_supplicant/wpa_supplicant.conf",'r') as file:
		network_configuration = file.read().split("\n")
		if 'network={' in network_configuration:
			return 'preconnect'
	return 'serving'

def saveServerMode():
	ssid,ip,password=None,None,None
	with open("/etc/wpa_supplicant/wpa_supplicant.conf",'r') as file:
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
	with open("network_details.txt",'w'):
		file.write(','.join((ssid,ip,password)))

def loadServerMode():
	with open("network_details.txt",'r'):
		mode = file.read().split(",")
	return mode
