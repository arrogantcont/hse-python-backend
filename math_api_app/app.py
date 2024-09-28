from handlers import handle_factorial, handle_fibonacci, handle_mean

async def app(scope, receive, send):
    if scope['type'] != 'http':
        return

    method = scope['method']
    path = scope['path']

    if method == 'GET' and path ==  '/factorial':
        await handle_factorial(scope, receive, send)
    elif method == 'GET' and path.startswith('/fibonacci/'):
        await handle_fibonacci(scope, receive, send)
    elif method == 'GET' and path == '/mean':
        await handle_mean(scope, receive, send)
    else:
        response_headers =[(b'content-type', b'text/plain')]
        await send({
            'type': 'http.response.start',
            'status': 404,
            'headers': response_headers,
        })
        await send({
            'type': 'http.response.body',
            'body': b'Not Found',
        } )
