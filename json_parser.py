import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json

contents = []
with open('soft-sci-fi.csv', encoding='utf-8', newline='') as csvf:  # Open file in read mode
    urls = csv.reader(csvf)
    for url in urls:
        contents.append(url)  # Add each url to list contents

#print(contents)


books = []

for url in contents:  # Parse through each url in the list.
    page = urlopen(url[0]).read()
    soup = BeautifulSoup(page, "html.parser")
    items = soup.find_all('div', class_='main-info-block-detail')

    for item in items:
        author = item.find('div', id='work-names-unit').find('span')
        title_ru = item.find('div', id='work-names-unit').find('h2')
        title_en = item.find('div', id='work-names-unit').find('p')
        annotation = soup.select("div#annotation-unit div div.responses-list span p")
        annot_0 = []
        for i in range(len(annotation)):
            annot_0.append(annotation[i].string)
        try:
            annot = ''.join(annot_0).replace('\r', '')
        except:
            TypeError
        result_comments = soup.select("div.response-item div.response-body-home p")
        comments_0 = []
        for i in range(len(result_comments)):
            comments_0.append(result_comments[i].string)
        try:
            comments = ''.join(comments_0).replace('\r', '').replace('\n', '')
        except:
            TypeError
        try:
            books.append(
                {
                    'author': author.get_text(strip=True),
                    'title_ru': title_ru.get_text(strip=True),
                    'title_en': title_en.get_text(strip=True),
                    #'date': date,
                    #'original lang': lang.get_text(strip=True),
                    #'avg_score': avg_score.get_text(strip=True),
                    #'num_of_voices': voices.get_text(strip=True),
                    'annotation': annot,
                    'comments': comments
                }
            )
        except:
            AttributeError


with open('soft-sci-fi.json', 'w', encoding='utf-8') as f:
    json.dump(books, f)

#def save_content(content):
 #   with open("antiutopia_1.csv", 'w', newline='', encoding="utf-16") as file:
  #      writer = csv.writer(file, delimiter=';')
   #     writer.writerow(['author', 'title_ru', 'title_en', 'annotation', 'comments'])
    #    for item in items:
     #       writer.writerow([item['author'], item['title_ru'], item['title_en'], item['annotation'],
      #                       item['comments']])


#save_content(books)
