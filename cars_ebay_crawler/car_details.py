import requests
from bs4 import BeautifulSoup
import pandas as pd

def searchvin(itemURL):
    r = requests.get(itemURL)
    soup = BeautifulSoup(r.text, 'html.parser')
    vin = ''
    bottom = soup.find('div', {'id': 'BottomPanel'}) 
    itemDetails = bottom.find('div', {'class': 'vim x-about-this-item'})
    layout = itemDetails.find('div', {'data-testid': 'ux-layout-section-module'})
    features = layout.find('div', {'class': 'ux-layout-section ux-layout-section--features'})
    rows = itemDetails.find_all('div', {'class': 'ux-layout-section__row'})
    # print(rows)
    for row in rows:
        if str(row).__contains__("VIN"):
            # dic = {}
            contents = row.find_all('div', {'class': 'ux-labels-values__labels'})
            values = row.find_all('div', {'class': 'ux-labels-values__values'})
            # print("content = ", contents)
            # print("value = ", values)
            for i in range(len(contents)):
                if str(contents[i]).__contains__("VIN"):
                    vin = values[i].text
                    # print(" VIIIIIIN " , vin.text)
    return vin
    
