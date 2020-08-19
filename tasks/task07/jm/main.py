from typing import Dict, List, Optional
from dataclasses import dataclass
import asyncio
import urllib.request
import urllib.parse
import http.cookiejar
import aiohttp

import requests
from bs4 import BeautifulSoup

@dataclass
class SemesterData:
    year: int
    semester: int



async def get_courses(semester: Optional[SemesterData] = None) -> Dict[str, List[str]]:
    lecture_url = f"https://lms.bible.ac.kr/local/ubion/user/?year={semester}&semester={semester}"
    result = {}

    async with aiohttp.ClientSession() as session:
        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        opener.add_headers = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)')]
        urllib.request.install_opener(opener)
        login_form = {"username": "chojam301", "password": "durrkdcp0398"}
        url = "https://lms.bible.ac.kr/login.php"

        login_req = urllib.parse.urlencode(login_form).encode('ascii')
        request = urllib.request.Request(url, data=login_req)
        login_res = urllib.request.urlopen(request)
        login_res.read().decode('utf-8')

        async with session.get(lecture_url) as response:
            html = await response.text()

    soup = BeautifulSoup(html, 'html.parser')
    lec_list = soup.select('#page-content-wrap .my-course-lists')

    for item in lec_list:
        lecture = item.select_one('.course_label_re_02 a').get_text()
        professor = item.select_one('tr td')[2].get_text()
        num_member = item.select_one('tr td')[3].get_text()

        result[lecture] = [professor, num_member]

    return result


async def main():
    print("default")
    print(await get_courses(SemesterData(2020, 20)))
    print("-" * 30)
    print(await get_courses(SemesterData(2020, 10)))  # 2020학년도 1학기 데이터 조회


asyncio.run(main())