How to use the functions in database.py and calculate.py:

database.py:
  Inlcudes 5 functions:
    1. input_water_data:
       Insert sensor data function into databse. The input should be: quantity( of water), start_time, sensor ID. No return.
       
    2. input_water_price:
       Insert water price data manually. The input should be: price in a list[[Tier1_start,price,class],...], and area. No return.
       
    3. get_water_data:
       Get all data in water table in a list.
       
    4. get_water_price:
       Return price in a list: [[Tier1_start,fee],...]. The input should be: area, class.
       
    5. auto_update_price:
       Update water price by scraper. Using Nara's water_price.py. 
       The scraper returns the price for North area, so this function will update that price.
       
calculate.py
   2 functions:
   1. calculate_price
      Calculate fee. The input should be: quantity, area(North by default), class(1 by default). Return one number.
      
   2. price:
      Calculate fee for a specific period. The input should be: start_time, end_time, sensor(list of sensor IDs, or empty list for all sensors). Return one number.
