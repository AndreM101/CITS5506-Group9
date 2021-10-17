server_ip=$""
until [[ $server_ip != "" ]]
do
        server_ip=$(arp -a | cut -f 2 -d "(" | cut -f 1 -d ")")
done

sudo python3 /home/pi/Desktop/sensor/preconnect_request.py $server_ip
