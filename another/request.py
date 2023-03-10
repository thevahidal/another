import json


class Request():
    method: str 
    query: dict
    body: dict
    params: dict
    path: str
    
    def __init__(self, scope, message) -> None:
        self.query = Request.parse_query(scope['query_string'].decode())
        if message.get('body') != b'':
            body = json.loads(message.get('body').decode())
            self.body = body
        self.path = scope['path']
        self.method = scope['method']
    
    @staticmethod
    def parse_query(raw_query: str):
        if raw_query == '':
            return {}
        
        queries = raw_query.split("&")
        parsed = {}

        for query in queries:
            parsed[query.split("=")[0]] = query.split("=")[1]
            
        return parsed
            