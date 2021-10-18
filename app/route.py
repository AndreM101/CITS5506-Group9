from flask import Flask, render_template, request, jsonify, redirect, url_for
import sqlite3
import os 
import socket 
import get_wifi
import get_wifi_window
from sys import platform
# import get_wifi_data
from datetime import datetime 
import pandas as pd 
import csv 
# import database 

from database import input_water_data
from CITS5506-Group9.client scripts.sensor import payload

app = Flask(__name__,template_folder="templates")

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
db_path = os.path.join(BASE_DIR, "database.db")

#update data

def updateData():
    update_water = input_water_data(payload['period_flow_rate'],payload['seconds'],payload['id'])
    return update_water

# rendering the html 
@app.route("/", methods=["GET"])
def index():
  con = sqlite3.connect("database.db")
  cur = con.cursor()
  cur.execute('Select w.quantity, t.Fee, ROUND((w.quantity*t.Fee),3) AS Cost \
              from Tiers t JOIN WaterCharge wc USING (tiers_id) JOIN water w ON w.id == wc.water_id')  
  rows = cur.fetchall()
  return render_template("index.html",rows=rows)

# rending the price based on region 
@app.route('/get_cost/<region>', methods=["GET"])
def get_price(region):
  con = sqlite3.connect("database.db")
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
  con = sqlite3.connect("database.db")
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
  con = sqlite3.connect("database.db")
  cur = con.cursor()
  cur.execute('select * from water where sensor_id =1')
  rows = cur.fetchall()
  return jsonify(rows)

@app.route('/sendNetworkInformation', methods=["GET"])
def sendNetworkInformation():
  ip_address = socket.gethostbyname(socket.gethostname())
  # get the ssid 
  if platform=='darwin':
    ssid=get_wifi.get_wifi_info()
  elif platform =="win32":
    ssid= get_wifi_window.get_wifi_info()
  headers = request.headers
  auth = headers.get("X-Api-Key")
  if auth == 'password':
      return f'Ip address: {ip_address}\nSSID: {ssid}'
  else:
      return jsonify({"message": "ERROR: Unauthorized"}), 401
    
# for post connection update the database     
# @app.route('/updateData/<quantity>/<start_time>/<sensor>', methods=['POST'])
# def update_database(quantity,start_time,sensor):
#   database.input_water_data(quantity,start_time,sensor)
#   return ('',204)
  
@app.route('/connection', methods=["GET"])
def connection():
  ip_address = socket.gethostbyname(socket.gethostname())
  if platform=='darwin':
    ssid=get_wifi.get_wifi_info()
    passwords = get_wifi.get_password(ssid)
  elif platform =="win32":
    ssid= get_wifi_window.get_wifi_info()
    # need to create a password function for window 
    passwords = get_wifi_window.get_password(ssid)
  # ip_address, ssid, password = get_wifi_data.getSeverMode()
  with open('./networkInformation.csv', 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow([ip_address])
    writer.writerow([ssid])
    writer.writerow([passwords])
  # call the script for connection mode, return a vector 
  headers = request.headers
  auth = headers.get("X-Api-Key")
  # if len(vector) != 0 and auth=="password": 
  if auth == "password":
    return ip_address, ssid, password
  else:
    return "It is invalid"
    
@app.route('/verify/', methods=["POST"])
def start_verify():
  con = sqlite3.connect("database.db")
  total = 0
  if request.method == "POST":
    if request.form['verify_button'] == "start":
      start_time = datetime.now()
      start = start_time.strftime("%Y-%m-%d %H:%M:%S")
      with open('./verify_data.csv', 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([start])
    elif request.form['verify_button'] == "end":
      end_time = datetime.now()
      end = end_time.strftime("%Y-%m-%d %H:%M:%S")
      # start, record the liters, 
      # result = waterCost(start,end)
      with open("verify_data.csv", 'r') as file:
        csvreader = csv.reader(file)
        header = next(csvreader)
      start = header[0]
      cur = con.cursor()
      sql = 'Select Quantity From water where StartTime BETWEEN "{0}" AND "{1}"'.format(start,end)
      print(sql)
      cur.execute(sql)
      results = cur.fetchall()
      for i in range(len(results)):
        total += results[i][0]
        average = total/len(results)
      volumn = float(request.form['volumn'])
      calibration = volumn/total
      with open('./verify_data.csv', 'a', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([end])
        writer.writerow([total])
        writer.writerow([average])
        writer.writerow([calibration])
  return ('', 204)
  
if __name__=="__main__":
  app.run(debug=True)