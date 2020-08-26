import asyncio
from pprint import pprint

from biblebot import IntranetAPI, KbuAPI


async def get_intranet_info():
    #IntranetAPI.Login
    resp = await IntranetAPI.Login.fetch("chojam301", "durrkdcp0398")
    result = IntranetAPI.Login.parse(resp)
    cookie = result.data["cookies"]
    print(result)

    #IntranetAPI.StudentPhoto

    #IntranetAPI.Chapel
    resp = await IntranetAPI.Chapel.fetch(cookies=cookie)
    result = IntranetAPI.Chapel.parse(resp)
    print(result)

    #IntranetAPI.Timetable
    resp = await IntranetAPI.Timetable.fetch(cookies=cookie)
    result = IntranetAPI.Timetable.parse(resp)
    pprint(result.data)

    #IntranetAPI.Course
    resp = await IntranetAPI.Course.fetch(cookies=cookie)
    result = IntranetAPI.Course.parse(resp)
    pprint(result.data)


async def get_kbu_info():
    #KbuAPI.MainNotice
    resp = await KbuAPI.MainNotice.fetch(page=1)
    result = KbuAPI.MainNotice.parse(resp)
    pprint(result.data)

    #KbuAPI.ScholarshipNotice
    resp = await KbuAPI.ScholarshipNotice.fetch(page=1)
    result = KbuAPI.ScholarshipNotice.parse(resp)
    pprint(result.data)

    #KbuAPI.IllipNotice
    resp = await KbuAPI.IllipNotice.fetch(page=1)
    result = KbuAPI.IllipNotice.parse(resp)
    pprint(result.data)

asyncio.run(get_intranet_info())
asyncio.run(get_kbu_info())
