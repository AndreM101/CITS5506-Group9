import os
import sqlite3
import time
from water_price import get_price

database_dir = 'app/database/database.db'
url = 'https://www.watercorporation.com.au/Help-and-advice/Bill-and-account/Rates-and-charges/Residential-water-use-charges-explained'
#size of pipe
s = 1

# Insert sensor data function
def input_water_data(quantity,start_time,sensor):
    database = sqlite3.connect(database_dir)
    c = database.cursor()
    #quantity = 0
    #for n in data:
    #    quantity = quantity + n[0] * n[1] * s     
    c.execute("INSERT INTO water (STARTTIME,SENSOR_ID,QUANTITY)\
        VALUES(?,?,?)",(start_time,sensor,quantity))
    database.commit()
    database.close()

#def input_water_charge(date,hour,fee,quantity):
    #database = sqlite3.connect(database_dir)
    #c = database.cursor()
    #c.execute("INSERT INTO WaterCharge (DATE,HOUR,FEE,QUANTITY)\
        #VALUES(?,?,?,?)",(date,hour,fee,quantity))
    #database.commit()
    #database.close()

# Insert scraped data function
#price should be a list[[Tier1_start,price,class],...]
def input_water_price(price,area):
    database = sqlite3.connect(database_dir)
    c = database.cursor()
    tier = 1
    t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 
    for n in price:
        c.execute("INSERT OR REPLACE INTO TIERS (AREA,TIER,START,FEE,CLASS,TIMESTAMP)\
        VALUES(?,?,?,?,?,?)",(area,tier,n[0],n[1],n[2],t))
        tier = tier + 1
    database.commit()
    database.close()

# Query all from water table
#get all data in water table in a list
def get_water_data():
    database = sqlite3.connect(database_dir)
    c = database.cursor()
    cur = c.execute("SELECT * FROM water")
    price = []
    for row in cur:
        price.append(list(row))
    database.commit()
    database.close()
    return price

#def get_water_charge_data(date,hour):
    #database = sqlite3.connect(database_dir)
    #c = database.cursor()
    #cur = c.execute("SELECT fee,quantity FROM WaterCharge WHERE Date = ? & Hour = ?",(date,hour,))
    #l = []
    #for row in cur:
    #    l.append(list(row))
    #database.commit()
    #database.close()
    #return l

#return price in a list: [[Tier1_start,fee],...]
def get_water_price(area,cls):
    database = sqlite3.connect(database_dir)
    c = database.cursor()
    cur = c.execute("SELECT Start,Fee FROM TIERS WHERE AREA == ? AND class == ?",(area,cls,))
    p = []
    for row in cur:
        p.append(list(row))
    database.commit()
    database.close()
    return p

def auto_update_price():
    l = get_price(url)[1]
    t = []
    for n in l:
        name = list(n)
        del(name[0])
        p = []
        for m in name:
            p.append(float(n[m].strip('$')))
        t.append(p)
    price = []
    usage = [0,351,501,751]
    for cls in range(0,5):
        for i in range(0,4):
            price.append([usage[i],t[i][cls],cls+1])
    return price

