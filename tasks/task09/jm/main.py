import asyncio

from biblebot import LmsAPI

async def main():
    #LmsAPI.Login
    resp = await LmsAPI.Login.fetch("chojam301", "durrkdcp0398")
    result = LmsAPI.Login.parse(resp)
    cookie = result.data["cookies"]
    print(result)

    #LmsAPI.Profile
    resp = await LmsAPI.Profile.fetch(cookies=cookie)
    profile = LmsAPI.Profile.parse(resp)
    print(profile)

    #LmsAPI.CourseList
    resp = await LmsAPI.CourseList.fetch(cookies=cookie, semester="20202")
    result = LmsAPI.CourseList.parse(resp)
    print(result)

    #LmsAPI.Attendance
    resp = await LmsAPI.Attendance.fetch(cookies=cookie, course_code="1697")
    result = LmsAPI.Attendance.parse(resp)
    print(result)


asyncio.run(main())