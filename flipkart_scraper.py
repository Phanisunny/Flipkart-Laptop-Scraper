import pandas as pd
from bs4 import BeautifulSoup
import requests
from datetime import datetime
def flipkart(search,pages):
    url='https://www.flipkart.com/search?q='
    for i in search.split():
        url+=i
        url+='+'
    url=url[:len(url)-1]
    lap='laptops' in search.lower()
    name=[]
    price=[]
    rating=[]
    reviews=[]
    processor=[]
    for i in range(1,pages+1):
        index='&page='+str(i)
        laptops=requests.get(url+index)
        soup=BeautifulSoup(laptops.content,'html.parser')
        laptop_cards=soup.select('div.slAVV4' if(lap) else 'div.tUxRFH')
        for j in laptop_cards:
            name_tag = j.find('a' if(lap) else 'div', class_='wjcEIp' if(lap) else "KzDlHZ")
            price_tag = j.find('div', class_='Nx9bqj' if(lap) else 'Nx9bqj _4b5DiR')
            rating_tag = j.find('div', class_='XQDdHH')
            review_tag = j.find('span', class_='Wphh3N')
            processor_tag = j.find('li', class_='J+igdf')
    
            name.append(name_tag.text if name_tag else "N/A")
            prices=price_tag.text if price_tag else "N/A"
            prices=prices.replace('₹','')
            prices=prices.replace(',','')
            price.append(int(prices))
            rating.append(rating_tag.text if rating_tag else "N/A")
            reviews.append(review_tag.text if review_tag else "N/A")
            processor.append(processor_tag.text if processor_tag else "N/A")
    lap50=pd.DataFrame({'Laptop_name':name,'Price':price,'Rating':rating,'Reviews':reviews,'Processor':processor})
    return lap50
search=input("Which type of laptops data do you want?")
pages=int(input("Number of pages you want to extract data from:"))
timestamp=datetime.now().strftime('%Y%m%d_%H%M%S')
filename=f'flipkart_laptops_{timestamp}.csv'
result=flipkart(search,pages)
result.to_csv(filename,index=False)
print(filename)
print(result)
