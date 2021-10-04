from database import get_water_price

def caculate_price(quantity,area):
    price = get_water_price(area)
    tiers = len(price)
    s = 0
    q = quantity
    for i in range(tiers,0,-1):
        if quantity > price[0]:
            q = q - price[0]
            s = s + q * price[1]
    return s