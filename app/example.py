import database
from caculate import caculate_price
import os
from water_price import get_price
import time

data = [[1,2],[3,4],[5,6]]
start_time = '2021-09-28 10:10:10.0 +8:00'
url = 'https://www.watercorporation.com.au/Help-and-advice/Bill-and-account/Rates-and-charges/Residential-water-use-charges-explained'

#get_price(url)

#database.input_water_data(data,start_time,end_time,'Perth')

#water_data = database.get_water_data()
#print(water_data)

#quantity = 0
#for n in water_data:
    #quantity = quantity + n[2]

#price = caculate_price(quantity,'Perth')
#print(price)

#print(database.get_water_price('Perth'))


price = [[0,1.859],[151,2.477],[500,4.633]]
t = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) 

database.input_water_price(price,t)
database.input_water_data(100,t,1)
w = database.get_water_data()
for n in w:
    print(n)
p = database.get_water_price()
for n in p:
    print(n)