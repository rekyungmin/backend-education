import json
from itertools import chain
from collections import defaultdict

from aiohttp import web

"""
3. json 형식으로 순위 출력 
"""

server = {
    "host": "localhost",
    "port": 8080,
    "message": "server on 8080 port"
}
routes = web.RouteTableDef()


@web.middleware
async def error_middleware(request, handler):
    try:
        resp = await handler(request)

    except KeyError:
        return web.json_response({"status": "Failed", "reason": "keyword=<입력할 내용> 를 사용해주세요.", "status_code": 400})
    except ValueError:
        return web.json_response({"status": "Failed", "reason": "제목을 자세히 입력해주세요.", "status_code": 400})
    except web.HTTPNotFound as e:
        return web.json_response({"status": "Failed", "reason": "/book 경로로 접속해주세요.", "status_code": e.status_code})

    else:
        return web.json_response({"status": "success", "content": resp})


@routes.get('/book')
async def handle_book(request):
    data = request.query
    if data['keyword'] == "":
        raise ValueError
    elif not data['keyword']:
        raise KeyError
    else:
        everytime_result = await get_everytime_book(data['keyword'])
        aladin_result = await get_aladin_book(data['keyword'])

    result = defaultdict(dict)

    print(everytime_result)
    print(aladin_result)

    for key, value in chain(everytime_result.items(), aladin_result.items()):
        result[key] = value

    return result

app = web.Application(middlewares=[error_middleware])
app.add_routes(routes)

if __name__ == '__main__':
    print(server["message"])
    if __package__ is None:
        import sys
        from os import path

        file_dir = path.dirname(path.dirname(path.abspath(__file__)))
        sys.path.append(file_dir)

        from scraper import get_everytime_book, get_aladin_book

    web.run_app(app, port=server["port"], host=server["host"])
