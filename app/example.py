import database
from caculate import caculate_price
import os

data = [[1,2],[3,4],[5,6]]
start_time = '2021-09-28 10:10:10.0 +8:00'
end_time = '2021-09-28 10:10:15.0 +8:00'

#database.input_water_data(data,start_time,end_time,'Perth')

water_data = database.get_water_data()
print(water_data)

quantity = 0
for n in water_data:
    quantity = quantity + n[2]

price = caculate_price(quantity,'Perth')
print(price)

print(database.get_water_price('Perth'))

