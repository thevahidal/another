import json
from enum import Enum

from .request import Request
from .response import Response
from .status import Status

GLOBAL_ORDER = 0

class Verb(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"
    OPTIONS = "OPTIONS"
    HEAD = "HEAD"

HANDLERS = {
    Verb.GET.value: {},
    Verb.POST.value: {},
    Verb.PUT.value: {},
    Verb.PATCH.value: {},
    Verb.DELETE.value: {},
    Verb.OPTIONS.value: {},
    Verb.HEAD.value: {},
}

MIDDLEWARES = []


class Another():
    def __init__(self) -> None:
        pass
    
    async def __call__(self, scope, receive, send):
        assert scope['type'] == 'http'
        
        try:
            method = scope['method']
            url = scope['path']
            handler, order = HANDLERS[method][url]
            
            before_middlewares = [_middleware for _middleware, _order in MIDDLEWARES if _order < order ]
            after_middlewares = [_middleware for _middleware, _order in MIDDLEWARES if _order > order ]
            
            message = await receive()
            request = Request(scope=scope, message=message)
            
            
            for middleware in before_middlewares:
                request = middleware(request, None)
            
            response = handler(request)
            
            for middleware in after_middlewares:
                response = middleware(None, response)
            
            await self.handle_response(send=send, response=response)
        except KeyError:
            await self.handle_response(send=send, response=Response(status=Status.HTTP_400_BAD_REQUEST))
            
        except Exception as e:
            print("error", e)
            await self.handle_response(send=send, response=Response(status=Status.HTTP_400_BAD_REQUEST))
            
       
    
    def use(self):
        global GLOBAL_ORDER
        GLOBAL_ORDER += 1
        def wrapped(callback):
            MIDDLEWARES.append((callback, GLOBAL_ORDER))
            return callback
        
        return wrapped
    
    def get(self, route):
        global GLOBAL_ORDER
        GLOBAL_ORDER += 1
        def wrapped(callback):
            HANDLERS[Verb.GET.value][route] = (callback, GLOBAL_ORDER)
            return callback
        
        return wrapped

    def post(self, route):
        global GLOBAL_ORDER
        GLOBAL_ORDER += 1
        def wrapped(callback):
            HANDLERS[Verb.POST.value][route] = (callback, GLOBAL_ORDER)
            return callback
        
        return wrapped
    
    def put(self, route):
        global GLOBAL_ORDER
        GLOBAL_ORDER += 1
        def wrapped(callback):
            HANDLERS[Verb.PUT.value][route] = (callback, GLOBAL_ORDER)
            return callback
        
        return wrapped
    def patch(self, route):
        global GLOBAL_ORDER
        GLOBAL_ORDER += 1
        def wrapped(callback):
            HANDLERS[Verb.PATCH.value][route] = (callback, GLOBAL_ORDER)
            return callback
        
        return wrapped
    
    def delete(self, route):
        global GLOBAL_ORDER
        GLOBAL_ORDER += 1
        def wrapped(callback):
            HANDLERS[Verb.DELETE.value][route] = (callback, GLOBAL_ORDER)
            return callback
        
        return wrapped
    
    def options(self, route):
        global GLOBAL_ORDER
        GLOBAL_ORDER += 1
        def wrapped(callback):
            HANDLERS[Verb.OPTIONS.value][route] = (callback, GLOBAL_ORDER)
            return callback
        
        return wrapped
    
    def head(self, route):
        global GLOBAL_ORDER
        GLOBAL_ORDER += 1
        def wrapped(callback):
            HANDLERS[Verb.HEAD.value][route] = (callback, GLOBAL_ORDER)
            return callback
        
        return wrapped
    
    async def handle_response(self, send, response: Response):
        await send({
            'type': 'http.response.start',
            'status': response.status,
            'headers': [
                [b'content-type', b'application/json'],
            ],
        })
        await send({
            'type': 'http.response.body',
            'body': json.dumps(response.data or {}).encode(),
        })
    