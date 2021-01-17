import secrets
import json

from aiohttp import web
from biblebot import IntranetAPI

server = {
    "host": "localhost",
    "port": 8080,
    "message": "server on 8080 port"
}

INFO = {}

routes = web.RouteTableDef()


@web.middleware
async def error_middleware(request, handler):
    try:
        resp = await handler(request)

    except KeyError:
        return web.json_response({"status": "failed", "reason": "정확한 로그인 정보를 입력하세요", "status_code": 400})
    except json.JSONDecodeError:
        return web.json_response({"status": "failed", "reason": "json 형식에 맞게 입력하세요", "status_code": 400})
    except web.HTTPUnauthorized as e:
        return web.json_response({"status": "failed", "reason": str(e), "status_code": e.status_code})

    else:
        return web.json_response({"status": "success", "content": resp})


@routes.post('/login')
async def handle_login(request):
    key = secrets.token_urlsafe(16)

    while key in INFO:
        key = secrets.token_urlsafe(16)

    data = await request.json()
    resp_login = await IntranetAPI.Login.fetch(data["id"], data["passwd"])

    if resp_login.reason != "Found":
        raise KeyError

    result = IntranetAPI.Login.parse(resp_login)
    INFO[key] = result.data["cookies"]

    return key


@routes.get('/chapel')
async def handle_chapel(request):
    data = request.query
    enter_key = data["key"]

    if enter_key in INFO:
        resp_chapel = await IntranetAPI.Chapel.fetch(
            cookies=INFO[enter_key],
            semester=data["semester"]
        )
        result = IntranetAPI.Chapel.parse(resp_chapel)
        return result.data

    else:
        raise web.HTTPUnauthorized


@routes.get('/timetable')
async def handle_timetable(request):
    data = request.query
    enter_key = data["key"]

    if enter_key in INFO:
        resp_chapel = await IntranetAPI.Timetable.fetch(
            cookies=INFO[enter_key],
            semester=data["semester"]
        )
        result = IntranetAPI.Timetable.parse(resp_chapel)
        return result.data

    else:
        raise web.HTTPUnauthorized


@routes.get('/course')
async def handle_course(request):
    data = request.query
    enter_key = data["key"]

    if enter_key in INFO:
        resp_chapel = await IntranetAPI.Course.fetch(
            cookies=INFO[enter_key],
            semester=data["semester"]
        )
        result = IntranetAPI.Course.parse(resp_chapel)
        return result.data

    else:
        raise web.HTTPUnauthorized

app = web.Application(middlewares=[error_middleware])
app.add_routes(routes)

if __name__ == '__main__':
    print(server["message"])
    web.run_app(app, port=server["port"], host=server["host"])