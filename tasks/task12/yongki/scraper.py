from collections import defaultdict

import aiohttp
from bs4 import BeautifulSoup


async def get_everytime_book(keyword):
    scroll_page = [0, 40, 80, 120]
    items = defaultdict(list)

    for page in scroll_page:
        async with aiohttp.ClientSession() as session:
            url = f"https://bookstore.everytime.kr/find/itemlist.json?mine=0&keyword={keyword}&campus=0&start={page}"
            async with session.get(url) as resp:
                elements = await resp.json()

        for elem in elements:
            if elem['soldout'] == 0:
                # print(elem)
                items["에브리타임책방"].append([elem['book_title'], f"{elem['price']}원"])

    return items


async def get_aladin_book(keyword):
    search_url = f"https://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=Used&SearchWord={keyword}&x=0&y=0"

    items = defaultdict(list)
    async with aiohttp.ClientSession() as session:
        async with session.get(search_url) as resp:
            html = await resp.text()
            soup = BeautifulSoup(html, 'html.parser')

        books = soup.select('.ss_book_box')

        if len(books) > 1:
            raise ValueError
        else:
            book_url = f"https://www.aladin.co.kr{books[0].select('.ss_book_list li a')[0]['href']}"

            async with session.get(book_url) as resp:
                html = await resp.text()
                soup = BeautifulSoup(html, 'html.parser')

            elements = soup.select('.Ere_usedsell_table tr')
            elements.pop(0)  # thead 역할하는 tr 제거

            for elem in elements:
                title = elem.select('.sell_tableCF2 li')[0].text
                title = title.replace("[중고]", "").lstrip()

                price = elem.select('.sell_tableCF3 .Ere_sub_pink')[0].text
                price = price.replace(",", "")

                items["알라딘"].append([title, price])

    return items
