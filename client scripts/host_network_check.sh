if ! echo "SSID=\"Unifi\"" | grep "Unifi" /etc/wpa_supplicant/wpa_supplicant.conf; 
	then /home/pi/Desktop/start_network.sh &
fi
