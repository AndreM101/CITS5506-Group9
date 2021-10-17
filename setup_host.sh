cp /etc/wpa_supplicant/wpa_supplicant.conf /home/pi/Desktop/wifi_conf/connect.conf
sudo cp /home/pi/Desktop/wifi_conf/host.conf /etc/wpa_supplicant/wpa_supplicant.conf

sudo wpa_cli -i wlan0 reconfigure

sudo reboot
