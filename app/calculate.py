from database import get_water_price
from database import get_water_data
# Input: Quantity (Water), area, class
# Returns: water price for given input

def calculate_price(quantity,area = 'Perth',cls = 1):
    price = get_water_price(area,cls)
    tiers = len(price) - 1
    s = 0
    q = quantity
    for i in range(tiers,-1,-1):
        if quantity > price[i][0]:
            t = q - price[i][0]
            s = s + t * price[i][1]
            q = price[i][0]
    return s

def price(start_time,end_time,sensor=[]):
    water = get_water_data()
    quantity = 0
    if len(sensor) == 0:
        for n in water:
            if n[0] >= start_time and n[0] <= end_time:
                quantity = quantity + n[1]
        else:
            for n in water:
                if n[0] >= start_time and n[0] <= end_time and n[2] in sensor:
                    quantity = quantity + n[1]
    price = calculate_price(quantity)
    return price
        