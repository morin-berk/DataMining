import requests
from bs4 import BeautifulSoup
import csv

CSV = 'books.csv'
HOST = 'https://fantlab.ru'
URL = 'https://fantlab.ru/bygenre?wg19=on&wg26=on&lang=&form='
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Mobile Safari/537.36'
}


def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    #r.decoding = 'utf-16'
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('tr')
    books = []

    for item in items[3:-1:]:
        td = item.find('td')
        books.append(
            {
                'link_title': HOST + td.find('a').get('href')
            }
        )
    return books


def save_content(items, path):
    with open(path, 'w', newline='', encoding="utf-8") as file:
    #with open(path, 'w', encoding="utf-16") as file:
        writer = csv.writer(file, delimiter=';')
        for item in items:
            writer.writerow([item['link_title']])


def parser():
    PAGENATION = input('Укажите количество страниц для парсинга: ')
    PAGENATION = int(PAGENATION.strip())
    html = get_html(URL)
    if html.status_code == 200:
        books = []
        for page in range(1, PAGENATION + 1):
            print(f'Парсим страницу: {page}')
            html = get_html(URL, params={'page': page})
            books.extend(get_content(html.text))
        save_content(books, CSV)
    else:
        print("Error")


parser()

#html = get_html(URL)
#print(get_content(html.text))




