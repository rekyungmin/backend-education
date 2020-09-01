from aiohttp import web
from biblebot import IntranetAPI

user_info = {
    "semester": "20202",
    "cookie": ""
}

routes = web.RouteTableDef()


@routes.post('/login')
async def login_intranet(request):
    data = await request.json()

    resp = await IntranetAPI.Login.fetch(data["id"], data["pw"])
    if resp.status == 200:
        return web.Response(text="ID와 PW를 확인해주세요.", status=200)
    result = IntranetAPI.Login.parse(resp)
    user_info["cookie"] = result.data["cookies"]

    return web.Response(text="로그인에 성공했습니다.", status=302)


@routes.get('/chapel')
async def get_chapel_info():
    resp = await IntranetAPI.Chapel.fetch(
        cookies=user_info["cookie"], semester=user_info["semester"])
    result = IntranetAPI.Chapel.parse(resp)

    return web.Response(text=result, status=200)


@routes.post('/timetable')
async def get_timetable_info():
    resp = await IntranetAPI.Timetable.fetch(
        cookies=user_info["cookie"], semester=user_info["semester"])
    result = IntranetAPI.Timetable.parse(resp)

    return web.Response(text=result, status=200)


@routes.post('/course')
async def get_course_info():
    resp = await IntranetAPI.Course.fetch(
        cookies=user_info["cookie"], semester=user_info["semester"])
    result = IntranetAPI.Course.parse(resp)

    return web.Response(text=result, status=200)


app = web.Application()
app.add_routes(routes)
web.run_app(app, port=8080, host="localhost")
