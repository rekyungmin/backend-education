import time
import unicodedata
from typing import List
from concurrent.futures import ProcessPoolExecutor

import requests
from bs4 import BeautifulSoup

def get_notice_articles(page):
    request = requests.get(page).text
    soup = BeautifulSoup(request, 'html.parser')

    title = soup.select_one('.header > h5').get_text()
    title = title.strip()

    name = soup.select_one('.name span[data-role="name"]').get_text()
    date = soup.select_one('time').get_text()

    article = soup.select_one('.content').get_text()
    article = article.strip()
    article = unicodedata.normalize("NFKD", article)

    return [title, name, date, article]

def get_notice_articles_process(page_num: int = 1) -> List[List[str]]:
    page = f"https://www.bible.ac.kr/ko/life/notice/list/{page_num}"

    request = requests.get(page).text
    soup = BeautifulSoup(request, 'html.parser')
    lists = soup.select('ul li.tbody')

    result = []
    futures = []
    base_page = "https://www.bible.ac.kr"

    with ProcessPoolExecutor() as executor:
        for links in lists:
            target_page = base_page + links.select_one('div ul.black a')['href']
            result.append(executor.submit(get_notice_articles, target_page))

        for future in futures:
            result.append(future.result())
    return result

if __name__ == '__main__':
    start = time.time()

    item = get_notice_articles_process()

    for i in item:
        print(i.result())

    end = time.time()
    print(f'걸린 시간: {end - start}초')