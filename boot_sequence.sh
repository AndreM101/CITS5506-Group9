#!/bin/bash

networks=$(iwlist wlan0 scan)
sleep 10
connected=$(arp)
device_mode=$(cat device_mode.txt)
echo "started boot" | tee /home/pi/Desktop/boot_log.txt
echo $connected | tee /home/pi/Desktop/boot_log2.txt

# PRECONNECT SEQUENCE
if [[ $networks == *"CITS5506project1"* ]];
then	echo "client" | tee /home/pi/Desktop/device_mode.txt
	echo "preconnect"
sudo /HOME/pi/Desktop/sensor/preconnect_sequence.sh

# LONE DEVICE, NO NETWORK
elif [[ "$(arp)" == "" ]];
then	echo "server" | tee /home/pi/Desktop/device_mode.txt
        echo "not connected" | tee /home/pi/Desktop/boot_log.txt
#	/home/pi/Desktop/start_network.sh
	/home/pi/Desktop/start_server.sh
        echo "0,127.0.0.1" | tee /home/pi/Desktop/sensor/sensor_settings.txt
	echo "server + not connected + sensor"
python3 /HOME/pi/Desktop/sensor/start_sensor.py &

#ALREADY CONNECTED
else	echo "connected + sensor" | tee /home/pi/Desktop/boot_log.txt
python3 /HOME/pi/Desktop/sensor/start_sensor.py &
	#CONNECTED SERVER
	if [[ $device_mode == "server" ]];
	then	echo "server"
               python3 -c "from server.app import wifi; wifi.saveServerMode()"
               /HOME/pi/Desktop/start_server.sh
	fi
fi
