import json

from urllib.parse import parse_qs
from typing import Any, Union, List, Dict, Awaitable, Callable

from utils.functions import factorial, fibonacci, mean
from utils.checks import is_number


UNPROCESSABLE_ENTITY = b"422 Unprocessable Entity"
BAD_REQUEST = b"400 Bad Request"
NOT_FOUND = b"404 Not Found"

def get_response(code: int = 404, 
                 body: Union[bytes, str] = b'404 Not Found'
                 ) -> List[Dict[str, Union[int, bytes, List[tuple[bytes, str]]]]]:
    return [{
        'type': 'http.response.start',
        'status': code,
        'headers': [(b'content-type', 'text/plain')],
    },
    {
        'type': 'http.response.body',
        'body': body,
    }]


async def application(scope: dict[str, Any], 
                      receive: Callable[[], Awaitable[dict[str, Any]]], 
                      send: Callable[[dict[str, Any]], Awaitable[None]]) -> None:


    if scope["path"] == "/factorial": 

        query_params = parse_qs(scope["query_string"].decode("utf-8"), keep_blank_values=True)
        params = query_params.get("n")

        if ("n" not in query_params.keys()) or (not is_number(params[0])): 
            for x in get_response(code=422, body=UNPROCESSABLE_ENTITY): await send(x)

        elif is_number(params[0]):
            if int(params[0]) < 0:
                    for x in get_response(code=400, body=BAD_REQUEST): await send(x)
            else: 
                answer = factorial(int(params[0]))
                line = json.dumps({"result": answer}).encode("utf-8")
                for x in get_response(code=200, body=line): await send(x)
    
    elif "/fibonacci" in scope["path"]: 
        params = scope["path"].split("/fibonacci/")
        params = params[1] if len(params) == 2 else None

        if not is_number(params):
            for x in get_response(code=422, body=UNPROCESSABLE_ENTITY): await send(x) 

        elif is_number(params):

            if int(params) < 0:
                for x in get_response(code=400, body=BAD_REQUEST): await send(x)
            else: 
                answer = fibonacci(int(params))
                line = json.dumps({"result": answer}).encode("utf-8")
                for x in get_response(code=200, body=line): await send(x)

    
    elif "/mean" in scope["path"]: 
        try:
            body = await receive()
            data = json.loads(body['body'].decode('utf-8'))

            if not isinstance(data, list) or not all(is_number(i) for i in data):
                for x in get_response(code=422, body=UNPROCESSABLE_ENTITY): await send(x)

            elif len(data) == 0:
                for x in get_response(code=400, body=BAD_REQUEST): await send(x)

            else:
                line = json.dumps({'result': mean(data)}).encode('utf-8')
                for x in get_response(code=200, body=line): await send(x)
                        
        except (ValueError, KeyError):
            for x in get_response(code=422, body=UNPROCESSABLE_ENTITY): await send(x)

    else: 
        for x in get_response(code=404, body=NOT_FOUND): await send(x)