from flask import Flask, render_template, request, jsonify
import sqlite3
import os 

app = Flask(__name__,template_folder="templates")

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
db_path = os.path.join(BASE_DIR, "database.db")

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

# rending the water usage
@app.route('/get_water', methods=["GET"])
def get_water():
  con = sqlite3.connect("database.db")
  cur = con.cursor()
  cur.execute('select * from water where sensor_id =1')
  rows = cur.fetchall()
  return jsonify(rows)


if __name__=="__main__":
  app.run(debug=True)