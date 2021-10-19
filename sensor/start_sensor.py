import ExpanderPi
import time
import datetime
import requests

io = ExpanderPi.IO()
io.set_port_direction(0, 0x01)
io.set_port_pullups(0, 0x01)

last_sent_time = datetime.datetime.now()
last_recorded_time = datetime.datetime.now()
interval = 5#seconds
raw_signal = io.read_pin(1)
frequency = 0
#set this
with open("/home/pi/Desktop/sensor/sensor_settings.txt",'r') as file:
	settings = file.read().split(",")
	sensor_id = settings[0]
	server_address = 'http://'+settings[1].strip() + ':5000/updateData'

while True:
	#print(recordings)
	seconds = (datetime.datetime.now() - last_sent_time).seconds
	if seconds >= interval:
		period_litres = frequency/2
		payload = {"period_litres": period_litres, "start_time": last_sent_time, 'sensor': sensor_id}

		try:
			requests.post(server_address, data=payload)
		except Exception as e:
			if type(e) == type(requests.exceptions.ConnectionError()):
				print(str(e))
#		print("Sending",payload)
		last_sent_time = datetime.datetime.now()
		frequency=0

	if (datetime.datetime.now() - last_recorded_time).seconds >= 0.1:
		previous_signal = raw_signal
		raw_signal = io.read_pin(1)
		print(f"F: {frequency}, P: {previous_signal}, R: {raw_signal}, t: {datetime.datetime.now()-last_sent_time}")
		if raw_signal != previous_signal:
			frequency += 0.5
		last_recorded_time = datetime.datetime.now()
