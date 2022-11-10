import requests
from bs4 import BeautifulSoup
import pandas as pd

from car_details import searchvin

searchterm = 'cars+trucks'
zipcode = '52341'

# https://il.ebay.com/b/Cars-Trucks/6001/bn_1865117?rt=nc&_sop=10


def get_data(searchterm):
    print("......... Searching For Cars .......")
    url = f'https://www.ebay.com/sch/i.html?_from=R40&_nkw={searchterm}&_stpos=02453&_fcid=1&_sop=10'
    # url = f'https://www.ebay.com/sch/i.html?_from=R40&_nkw={car_type}&_sacat=6001&_sop=10'
    # https://www.ebay.com/sch/i.html?_from=R40&_nkw=Mazda&_stpos=02453&_fcid=1
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    return soup

# https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2499334.m570.l1313&_nkw=BMW+2020&_sacat=6001

def parse(soup, lastAdded):
    productslist = []
    results = soup.find_all('div', {'class': 's-item__info clearfix'})
    results = results[1:]
    for item in results:
        product = {
            'title': item.find('div', {'class': 's-item__title'}).text,
            'price': item.find('span', {'class': 's-item__price'}).text,
            'published_date': item.find('span', {'class': 's-item__detail s-item__detail--secondary'}).text, 
            'year': item.find('span', {'class': 's-item__dynamic s-item__dynamicAttributes1'}),
            'link': item.find('a', {'class': 's-item__link'})['href'],
        }
        if product["year"]:
            product["year"] = product["year"].text.replace('Year: ', '')
        vin = searchvin(product['link'])
        product['vin'] = vin
        print("......... Car Added TO DB .......", product )
        productslist.append(product)
        if product['published_date'] == lastAdded:
            break
    print(productslist)
    return productslist

def output(productslist, searchterm,last_added):
    productsdf =  pd.DataFrame(productslist)
    productsdf.to_csv('./cars/' + searchterm + '_output_'+ last_added +'.csv', index=False)
    print('Saved to CSV')
    return


