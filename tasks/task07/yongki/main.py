from typing import Dict, List, Optional
from dataclasses import dataclass
import asyncio

import aiohttp
from bs4 import BeautifulSoup


@dataclass
class SemesterData:
    year: int
    semester: int


LOGIN_INFO = {
    'username': '',
    'password': ''
}


async def get_courses(semester: Optional[SemesterData] = None) -> Dict[str, List[str]]:
    login_url = "https://lms.bible.ac.kr/login.php"
    course_url = f"https://lms.bible.ac.kr/local/ubion/user/?year={semester}&semester={semester}"
    print(course_url)
    async with aiohttp.ClientSession(raise_for_status=True) as session:
        await session.post(login_url, data=LOGIN_INFO)

        async with session.get(course_url) as course_req:
            html = await course_req.text()

    soup = BeautifulSoup(html, 'html.parser')

    course_lists = soup.select('.my-course-lists > tr')
    tasks = {}
    for course in course_lists:
        title = course.select_one('.coursefullname').text
        tutor = course.select('td')[2].text
        tutee = course.select('td')[3].text
        tasks.setdefault(title, [tutor, tutee])

    print(type(semester))
    return tasks


async def main():
    print("default")
    print(await get_courses())
    print("-" * 30)
    print(await get_courses(SemesterData(2020, 2)))

asyncio.run(main())
