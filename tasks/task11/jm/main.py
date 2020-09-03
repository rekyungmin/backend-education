from aiohttp import web
from biblebot import IntranetAPI

user_info = {
    "cookie": "",
    "iat": ""
}

login_result = 0

routes = web.RouteTableDef()


@routes.post('/login')
async def login_intranet(request):
    try:
        global login_result
        data = await request.json()

        resp = await IntranetAPI.Login.fetch(data["id"], data["pw"])
        if resp.status == 200:
            return web.Response(text="ID와 PW를 확인해주세요.", status=200)
        login_result = IntranetAPI.Login.parse(resp)
        user_info["cookie"] = login_result.data["cookies"]
        user_info["iat"] = login_result.data["iat"]

        return web.Response(text="로그인에 성공했습니다.", status=302)

    except KeyError:
        return web.Response(text="json 데이터의 key가 잘못되었습니다.", status=400)

    except Exception:
        return web.Response(text="데이터 형식이 잘못되었습니다.", status=400)


@routes.get('/chapel')
async def get_chapel_info(request):
    try:
        global login_result
        data = request.query

        if user_info["iat"] == login_result.data["iat"]:
            resp = await IntranetAPI.Chapel.fetch(
                cookies=user_info["cookie"], semester=data["semester"])
            result = IntranetAPI.Chapel.parse(resp)

            return web.Response(text=str(result), status=200)

    except Exception:
        return web.Response(text="로그인 후 이용 가능합니다.", status=401)



@routes.get('/timetable')
async def get_timetable_info(request):
    try:
        global login_result
        data = request.query

        if user_info["iat"] == login_result.data["iat"]:
            resp = await IntranetAPI.Timetable.fetch(
                cookies=user_info["cookie"], semester=data["semester"])
            result = IntranetAPI.Timetable.parse(resp)

            return web.Response(text=str(result), status=200)

    except Exception:
        return web.Response(text="로그인 후 이용 가능합니다.", status=401)


@routes.get('/course')
async def get_course_info(request):
    try:
        global login_result
        data = request.query

        if user_info["iat"] == login_result.data["iat"]:
            resp = await IntranetAPI.Course.fetch(
                cookies=user_info["cookie"], semester=data["semester"])
            result = IntranetAPI.Course.parse(resp)

            return web.Response(text=str(result), status=200)

    except Exception:
        return web.Response(text="로그인 후 이용 가능합니다.", status=401)


app = web.Application()
app.add_routes(routes)
web.run_app(app, port=8080, host="localhost")
