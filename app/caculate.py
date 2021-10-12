from database import get_water_price
# Input: Quantity (Water), area, class
# Returns: water price for given input

def caculate_price(quantity,area,cls):
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
