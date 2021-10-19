
from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
import os 
import socket 
import wifi
from sys import platform
from datetime import datetime 
import pandas as pd 
import csv 
import database 

app = Flask(__name__,template_folder="templates")

verify_start = 0

#BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
db_path = "/home/pi/Desktop/server/app/database.db"

# rendering the html 
@app.route("/", methods=["GET"])
def index():
  with open("/home/pi/Desktop/server/app/verify_data.csv",'r') as file:
    calibration = float(file.read())

  con = sqlite3.connect(db_path)
  cur = con.cursor()
  cur.execute('Select w.quantity, t.Fee, ROUND((w.quantity*t.Fee),3) AS Cost \
              from Tiers t JOIN WaterCharge wc USING (tiers_id) JOIN water w ON w.id == wc.water_id')  
  rows = cur.fetchall()
  rows = [[i[0]*calibration, i[1], i[2]*calibration] for i in rows]
#  rows = [[i[0],i[1]*calibration,i[2],i[3]] for i in rows]
  return render_template("index.html",rows=rows)

# rending the price based on region 
@app.route('/get_cost/<region>', methods=["GET"])
def get_price(region):
  con = sqlite3.connect(db_path)
  cur = con.cursor()
  if region=="Perth":
    cur.execute("select * from tiers where Area='{0}'".format(region))  
    rows = cur.fetchall()
  elif region=="South":
    cur.execute("select * from tiers where Area='{0}'".format(region))  
    rows = cur.fetchall()
  elif region=="North":
    cur.execute("select * from tiers where Area='{0}'".format(region))  
    rows = cur.fetchall()
  return jsonify(rows)


@app.route('/get_price/<region>', methods=["GET"])
def get_region_price(region):
  con = sqlite3.connect(db_path)
  cur = con.cursor()
  if region=="Perth":
    cur.execute("SELECT * \
                From Tiers  JOIN WaterCharge USING (tiers_id) \
                WHERE Area='{0}'".format(region))
    rows = cur.fetchall()
  elif region=="South":
    cur.execute("SELECT * \
                From Tiers  JOIN WaterCharge USING (tiers_id) \
                WHERE Area='{0}'".format(region)) 
    rows = cur.fetchall()
  elif region=="North":
    cur.execute("SELECT * \
                From Tiers  JOIN WaterCharge USING (tiers_id) \
                WHERE Area='{0}'".format(region))
    rows = cur.fetchall()
  return jsonify(rows)

# rending the water usage
@app.route('/get_water', methods=["GET"])
def get_water():
  with open("/home/pi/Desktop/server/app/verify_data.csv",'r') as file:
    calibration = float(file.read())

  con = sqlite3.connect(db_path)
  cur = con.cursor()
  cur.execute('select * from water')
  rows = cur.fetchall()
  rows = [[i[0],i[1]*calibration,i[2],i[3]] for i in rows]
  print(rows)
  return jsonify(rows)

@app.route('/sendNetworkInformation', methods=["GET"])
def sendNetworkInformation():
  if ip is None:
    return {} #invalid mode
  headers = request.headers
  auth = headers.get("X-Api-Key")
  # if len(vector) != 0 and auth=="password": 
  os.system("sudo cp /home/pi/Desktop/server/app/new.conf /etc/wpa_supplicant/wpa_supplicant.conf")
  os.system("/home/pi/Desktop/server/app/delayed_reboot.sh &")
  if auth == "password":
    return jsonify({'ip':ip, 'ssid':ssid, 'password':password, 'sensor_id': 1})
  else:
    return "It is invalid"

@app.route('/preconnect', methods=['GET'])
def preconnect():
  wifi.saveServerMode()
  wifi.set_host()

#  ip_address = socket.gethostbyname(socket.gethostname())
#  # get the ssid 
#  if platform=='darwin':
#    ssid=get_wifi.get_wifi_info()
#  elif platform =="win32":
#    ssid= get_wifi_window.get_wifi_info()
#  headers = request.headers
#  auth = headers.get("X-Api-Key")
#  if auth == 'password':
#      return f'Ip address: {ip_address}\nSSID: {ssid}'
#  else:
#      return jsonify({"message": "ERROR: Unauthorized"}), 401
    
# for post connection update the database     
@app.route('/updateData', methods=['POST'])
#<quantity>/<start_time>/<sensor>', methods=['POST'])
def update_database():
   sensor = request.form['sensor']
   start_time = request.form['start_time']
   quantity = request.form['period_litres']
   
   input_water_data(quantity,start_time,sensor)
   return ('',204)
  
@app.route('/connection', methods=["POST"])
def saveNetworkInformation():
#  ip_address = socket.gethostbyname(socket.gethostname())
#  if platform=='darwin':
#    ssid=get_wifi.get_wifi_info()
#    passwords = get_wifi.get_password(ssid)
#  elif platform =="win32":
#    ssid= get_wifi_window.get_wifi_info()
    # need to create a password function for window 
#    passwords = get_wifi_window.get_password(ssid)
  ssid = request.form['ssid']
  password= request.form['password']
  wifi.saveWifiDetails(ssid, password)
  #clientside script saying server will reboot
 
#  with open('./networkInformation.csv', 'w', encoding='utf-8') as f:
#    writer = csv.writer(f)
#    writer.writerow([ssid])
#    writer.writerow([password])
  # call the script for connection mode, return a vector   if ip is None:
#    return jsonify({'ip':ip, 'ssid':ssid, 'password':password})
#  else:
#    return "It is invalid"
    
@app.route('/verify/', methods=["POST"])
def start_verify():
  con = sqlite3.connect(db_path)
  total = 0
  global verify_start
  if request.method == "POST":
    if request.form['verify_button'] == "start":
      start_time = datetime.now()
      verify_start = start_time.strftime("%Y-%m-%d %H:%M:%S")
    elif request.form['verify_button'] == "end":
      end_time = datetime.now()
      end = end_time.strftime("%Y-%m-%d %H:%M:%S")
      # start, record the liters, 
      # result = waterCost(start,end)
      cur = con.cursor()
      sql = 'Select Quantity From water where StartTime BETWEEN "{0}" AND "{1}"'.format(verify_start,end)
      print(sql)
      cur.execute(sql)
      results = cur.fetchall()
      for i in range(len(results)):
        total += results[i][0]
        average = total/len(results)
      volumn = float(request.form['volumn'])
      total = 20
      with open('/home/pi/Desktop/server/app/verify_data.csv', 'w', encoding='utf-8') as f:
        if total != 0:
          calibration = volumn/total
          print(f"Calibration: {calibration}")
          #writer = csv.writer(f)
          #writer.writerow([calibration])
          f.write(str(calibration))
  return ('', 204)





def input_water_data(quantity,start_time,sensor):
    database = sqlite3.connect('/home/pi/Desktop/server/app/database.db')
    c = database.cursor()
    #quantity = 0
    #for n in data:
    #    quantity = quantity + n[0] * n[1] * s     
    c.execute("INSERT INTO water (STARTTIME,SENSOR_ID,QUANTITY)\
        VALUES(?,?,?)",(start_time,sensor,quantity))
    database.commit()
    database.close()





if __name__=="__main__":
  password,ip,ssid = wifi.loadServerMode()
  app.run(host='0.0.0.0', debug=True)
