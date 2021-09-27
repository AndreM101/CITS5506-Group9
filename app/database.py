import os
import sqlite3

database_dir = '/database/database.db'
#size of pipe
s = 1
#data should be a list: [[flow,time],...]
def input_water_data(data,start_time,end_time,area):
    database = sqlite3.connect(database_dir)
    c = database.cursor()
    quantity = 0
    for n in data:
        quantity = quantity + n[0] * n[1] * s
    c = database.cursor()
    cur = c.execute("SELECT AREACODE FROM AREA WHERE AREANAME = ?",(area,))
    for n in cur:
        id = list(n)[0]        
    c.execute("INSERT INTO water (STARTTIME,ENDTIME,QUANTITY,AREA)\
        VALUES(?,?,?,?)",(start_time,end_time,quantity,id))
    database.commit()
    database.close()

def input_water_charge(date,hour,fee,quantity):
    database = sqlite3.connect(database_dir)
    c = database.cursor()
    c.execute("INSERT INTO WaterCharge (DATE,HOUR,FEE,QUANTITY)\
        VALUES(?,?,?,?)",(date,hour,fee,quantity))
    database.commit()
    database.close()

#price should be a list[[Tier1_start,Tier1_end,fee],...]
def input_water_price(area,price):
    database = sqlite3.connect(database_dir)
    c = database.cursor()
    cur = c.execute("SELECT AREACODE FROM AREA WHERE AREANAME = ?",(area,))
    for n in cur:
        id = list(n)[0]
    tier = 1
    for n in price:
        c.execute("INSERT OR REPLACE INTO Tiers (AREA,TIER,START,END,FEE)\
        VALUES(?,?,?,?,?)",(id,tier,n[0],[1],n[2]))
        tier = tier + 1
    database.commit()
    database.close()

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

def get_water_charge_data(date,hour):
    database = sqlite3.connect(database_dir)
    c = database.cursor()
    cur = c.execute("SELECT fee,quantity FROM WaterCharge WHERE Date = ? & Hour = ?",(date,hour,))
    l = []
    for row in cur:
        l.append(list(row))
    database.commit()
    database.close()
    return l

#return price in a list: [[Tier1_start,Tier1_end,fee],...]
def get_water_price(area):
    database = sqlite3.connect(database_dir)
    c = database.cursor()
    cur = c.execute("SELECT AREACODE FROM AREA WHERE AREANAME = ?",(area,))
    for n in cur:
        id = list(n)[0]
    cur = c.execute("SELECT Start,End,Fee FROM Tiers WHERE AREA = ?",(id,))
    p = []
    for row in cur:
        p.append(list(row))
    database.commit()
    database.close()
    return p