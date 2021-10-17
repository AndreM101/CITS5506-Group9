sudo pkill -f hostap

cp /etc/wpa_supplicant/wpa_supplicant.conf /home/pi/Desktop/wifi_conf/host.conf
sudo cp /home/pi/Desktop/wifi_conf/connect.conf /etc/wpa_supplicant/wpa_supplicant.conf

sudo reboot
