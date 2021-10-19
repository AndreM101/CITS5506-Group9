#!/bin/bash

sleep 30
networks=$(/sbin/iwlist wlan0 scan)
connected=$(ip route)
device_mode=$(cat /home/pi/Desktop/device_mode.txt)
echo "started boot" | tee /home/pi/Desktop/boot_log.txt
echo $connected | tee /home/pi/Desktop/boot_log2.txt

# PRECONNECT SEQUENCE
if [[ $networks == *"CITS5506project1"* ]];
then	echo "client" | tee /home/pi/Desktop/device_mode.txt
	echo "preconnect"
        sudo /home/pi/Desktop/sensor/preconnect_sequence.sh

# LONE DEVICE, NO NETWORK
elif [[ $connected == "" ]];
then	echo "server" | tee /home/pi/Desktop/device_mode.txt
        echo $connected | tee /home/pi/Desktop/boot_log.txt
        echo "updated" | tee /home/pi/Desktop/boot_log2.txt
	/home/pi/Desktop/start_network.sh
	/home/pi/Desktop/start_server.sh
        echo "0,127.0.0.1" | tee /home/pi/Desktop/sensor/sensor_settings.txt
	echo "server + not connected + sensor"
	python3 /home/pi/Desktop/sensor/start_sensor.py &

#ALREADY CONNECTED
else	echo "connected + sensor" | tee /home/pi/Desktop/boot_log.txt
	python3 /home/pi/Desktop/sensor/start_sensor.py &
	#CONNECTED SERVER
	if [[ $device_mode == "server" ]];
	then	echo "server"
               python3 /home/pi/Desktop/server/app/wifi.py
               cp /etc/wpa_supplicant/wpa_supplicant.conf /home/pi/Desktop/wifi_conf/connect.conf
               /home/pi/Desktop/start_server.sh
	fi
fi
