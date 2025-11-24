import sys
import requests
from bs4 import BeautifulSoup
import pandas as pd

rawData = []

try:
    sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass

url = "https://funpay.com/lots/478/"
response = requests.get(url)

if response.status_code == 200:
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.title.text.strip() if soup.title else ''
    cards = soup.find_all('a', class_='tc-item', limit = 25)
    for card in cards:
        title = card.find('div', class_='tc-desc-text').text 
        cost = card.find('div', class_='tc-price').text
        cost = cost.replace('\n', '').replace(' ', '').replace('\xa0', '')
        numericCost = ''.join(filter(str.isdigit, cost))
    
    rawData.append({
            'title': title,
            'cost': numericCost
        })
    df = pd.DataFrame(rawData)

    df.to_csv('funpay_data.csv', index=False, sep=';')

    print("Data has been successfully written to funpay_data.csv")

    # print("Request was successful!")
    
else:
    print(f"Request failed: {response.status_code}")