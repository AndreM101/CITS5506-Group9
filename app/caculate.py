from database import get_water_price

def caculate_price(quantity,area):
    price = get_water_price(area)
    if quantity > price[2][1]:
        sum = (quantity - price[2][1]) * price[2][2] + price[0][1] * price[0][2] + price[1][1] * price[1][2]
    else:
        if quantity > price[1][1]:
            sum =  (quantity - price[1][1]) * price[1][2] + price[0][1] * price[0][2]
        else:
            sum = quantity * price[0][2]
    return sum