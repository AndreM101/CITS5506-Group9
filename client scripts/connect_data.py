#!/usr/bin/env python
import ExpanderPi
import time
import datetime
import requests
import sqlite3

#connect database
dbname='database.db'
sampleFreq = 1*60 # time in 60 seconds == 1 min

io = ExpanderPi.IO()
io.set_port_direction(0, 0x01)
io.set_port_pullups(0, 0x01)

last_sent_time = datetime.datetime.now()
last_recorded_time = datetime.datetime.now()
interval = 30 #seconds
recordings = []
raw_signal = io.read_pin(1)
frequency = 0
#set this
server_address = ""
# get data from sensor
def getData():
	#print(recordings)
	#seconds = (datetime.datetime.now() - last_sent_time).seconds
	if seconds >= interval:
		period_frequency = recordings[-1]
		period_flow_rate = period_frequency/2
		payload = {"period_flow_rate": period_flow_rate, "seconds": interval, "real": datetime.datetime.now()-last_sent_time, 'litres': period_frequency/7.5}
		# This is a placeholder payload, will likely be changed over the next week
		# Don't necessarily make the webserver based on that

#		requests.post(server_address, data=payload)
		print("Sending",payload)
		recordings=[]
		#last_sent_time = datetime.datetime.now()
		frequency=0

	if (datetime.datetime.now() - last_recorded_time).seconds >= 0.1:
		previous_signal = raw_signal
		raw_signal = io.read_pin(1)
		#t = datetime.datetime.now()-last_sent_time
		#print(f"F: {frequency}, P: {previous_signal}, R: {raw_signal}, t: {datetime.datetime.now()-last_sent_time}")
		if raw_signal != previous_signal:
			frequency += 0.5
		recordings.append(frequency)
		#last_recorded_time = datetime.datetime.now()
	logData(frequency)

# log sensor data on database
def logData (frequency):
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	curs.execute("INSERT INTO water values(datetime('now'), (?), (?))", (send_id, frequency))
	conn.commit()
	conn.close()
	
# display database data
def displayData():
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	print ("\nEntire database contents:\n")
	for row in curs.execute("SELECT * FROM water"):
		print (row)
	conn.close()

# main function
def main():
	for i in range (0,3):
		getData()
		time.sleep(sampleFreq)
	displayData()

# Execute program 
main()  
