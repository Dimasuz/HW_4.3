# Необходимо парсить страницу со свежими статьями (вот эту) и выбирать те статьи, в которых встречается хотя бы одно из ключевых слов (эти слова определяем в начале скрипта). Поиск вести по всей доступной preview-информации (это информация, доступная непосредственно с текущей страницы). Вывести в консоль список подходящих статей в формате: <дата> - <заголовок> - <ссылка>.
# Улучшить скрипт так, чтобы он анализировал не только preview-информацию статьи, но и весь текст статьи целиком. Для этого потребуется получать страницы статей и искать по тексту внутри этой страницы.



# определяем список ключевых слов
KEYWORDS = ['дизайн', 'фото', 'web', 'python']


import requests
from bs4 import BeautifulSoup
import re

headers = {
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
'Accept-Encoding': 'gzip, deflate, br',
'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,sv;q=0.6',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
'Cookie': '_ym_uid=1661790138398573269; _ym_d=1661790138; habr_web_home_feed=/all/; hl=ru; fl=ru; _ym_isad=1; _ga=GA1.2.1864422457.1661790139; _gid=GA1.2.2059705457.1661790139; _gat_gtag_UA_726094_1=1',
'DNT': '1',
'Host': 'habr.com',
'Referer': 'https://yandex.ru/',
'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
'sec-ch-ua-mobile': '?0',
'sec-ch-ua-platform': '"Windows"',
'Sec-Fetch-Dest': 'document',
'Sec-Fetch-Mode': 'navigate',
'Sec-Fetch-Site': 'same-origin',
'Sec-Fetch-User': '?1',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'
}

url = 'https://habr.com'

responce = requests.get(url+'/ru/all', headers=headers)
text = responce.text

soup = BeautifulSoup(text, 'html.parser')

articles = soup.find_all(class_='tm-articles-list__item')

for article in articles:
  
    link = url + article.find(class_='tm-article-snippet__title tm-article-snippet__title_h2').find('a').attrs['href']
    responce = requests.get(link, headers=headers)
    text = responce.text
    soup_1 = BeautifulSoup(text, 'html.parser')
    article_text = soup_1.find(class_='tm-article-body').text

    preview = article.find(class_=['article-formatted-body article-formatted-body article-formatted-body_version-2', 'article-formatted-body article-formatted-body article-formatted-body_version-1']).text

    for i in KEYWORDS:
        if re.search(i, preview) or re.search(i, article_text):
            data = article.find(class_='tm-article-snippet__datetime-published').find('time').attrs['title']
            print(f'Дата: {data}')
            title = article.find(class_='tm-article-snippet__title-link').text.strip()
            print(f'Заголовок: {title}')
            print(f'Ссылка: {link}')
            print()

