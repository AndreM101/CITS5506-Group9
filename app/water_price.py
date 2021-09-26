from bs4 import BeautifulSoup 
import requests
import pandas as pd 

url = 'https://www.watercorporation.com.au/Help-and-advice/Bill-and-account/Rates-and-charges/Residential-water-use-charges-explained'

contents = requests.get(url, headers = {'User-Agent':'Mozilla/5.0'}).text
soup = BeautifulSoup(contents, 'lxml')

title = []


sections = soup.find_all("section",class_="tabs__content-panel")
for section in sections:
  titles = section.find_all("h4")
  for ti in titles:
    title.append(ti.text)
    
    
tables = sections = soup.find_all('table')

for i in range(0,len(tables)):
  print(title[i])
  df=pd.read_html(str(tables[i]))[0]
  print(df)
  # print(df.to_dict("records"))
  
  


      
      
      
      

      
      
      
      




    




