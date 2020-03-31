import requests
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials

urls = [
    'https://www.amazon.ca/HATCHBOX-3D-PLA-1KG1-75-YLW-Filament-Dimensional/dp/B00J0GRREW/ref=sr_1_9?crid=3KYWEGJGL634Q&keywords=hatchbox+pla&qid=1585666095&sprefix=hatchbo%2Caps%2C198&sr=8-9'
]


def shorten_url(url):
    url = url.split('/')
    cleaned_url = '/'.join(url[:-1])
    return cleaned_url


def get_converted_price(price_text):
    price = price_text.strip()
    price = price.split('\xa0')[-1]
    price = float(price)
    return price


scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}


if __name__ == '__main__':
    creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open('Printing Prices').worksheet('Data')
    items = sheet.col_values(1)[1:]
    for item in items:
        cell = sheet.find(item)
        page = requests.get(cell.value, headers=headers)
        soup = BeautifulSoup(page.content, "html5lib")
        price = soup.find(id='priceblock_ourprice').text
        title = soup.find(id='productTitle').text.strip()
        converted_price = get_converted_price(price)
        sheet.update_cell(cell.row, 2, title)
        sheet.update_cell(cell.row, 3, converted_price)
