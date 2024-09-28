# handlers.py
from urllib.parse import parse_qs
import json
from math_utils import factorial, fibonacci, mean

async def handle_factorial(scope, receive, send):
    query_string = scope['query_string'].decode()
    query_params = parse_qs(query_string)

    n_values = query_params.get('n')
    if not n_values or len(n_values) == 0:
        status = 422
        response_body = b'Unprocessable Entity'
    else:
        n_str = n_values[0]
        try:
            n = int(n_str)
            if n < 0:
                status = 400
                response_body = b'Bad Request'
            else:
                result = factorial(n)
                response_body = json.dumps({"result": result}).encode()
                status = 200
        except  ValueError:
            status = 422
            response_body = b'Unprocessable Entity'

    response_headers = [(b'content-type', b'application/json')]
    await send({
        'type': 'http.response.start',
        'status': status,
        'headers': response_headers,
    })
    await send({
        'type': 'http.response.body',
        'body': response_body,
    })

async  def handle_fibonacci(scope, receive, send):
    path = scope['path']
    n_str = path[len('/fibonacci/'):]
    try:
        n = int(n_str)
        if n < 0:
            status = 400
            response_body = b'Bad Request'
        else:
            result = fibonacci(n)
            response_body = json.dumps({"result": result}).encode()
            status = 200
    except ValueError:
        status = 422
        response_body = b'Unprocessable Entity'

    response_headers = [(b'content-type', b'application/json')]
    await send({
        'type': 'http.response.start',
        'status': status,
        'headers': response_headers,
    })
    await send({
        'type': 'http.response.body',
        'body': response_body,
    })

async def handle_mean(scope, receive, send):
    body = b''
    more_body = True
    while more_body:
        message = await receive()
        body += message.get('body', b'')
        more_body = message.get('more_body', False)
    try:
        data = json.loads(body)
        if not isinstance(data, list):
            raise ValueError
        if len(data) == 0:
            status = 400
            response_body = b'Bad Request'
        else:
            floats = []
            for item in data:
                if isinstance(item, (int, float)):
                    floats.append(float(item))
                else:
                    raise ValueError
            mean_value = mean(floats)
            response_body = json.dumps({"result": mean_value}).encode()
            status = 200
    except (ValueError, json.JSONDecodeError):
        status = 422
        response_body = b'Unprocessable Entity'

    response_headers = [(b'content-type', b'application/json')]
    await send({
        'type': 'http.response.start',
        'status': status,
        'headers': response_headers,
    })
    await send({
        'type': 'http.response.body',
        'body': response_body,
    })
