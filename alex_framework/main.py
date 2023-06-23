from .reqs import GetRequests,PostRequests
from quopri import decodestring


class PageNotFound:
    def __call__(self, request):
        return '404 Not Found', '<h1>404</h1>Page Not Found'


class Framework:
    def __init__(self, routes, fronts):
        self.routes = routes
        self.front = fronts

    def __call__(self, environ, start_response):
        addr_url = environ['PATH_INFO']

        if not addr_url.endswith('/'):
            addr_url = f'{addr_url}/'

        if addr_url in self.routes:
            view = self.routes[addr_url]
        else:
            view = PageNotFound()

        request = {}
        method = environ['REQUEST_METHOD']
        request['method'] = method

        print(f'Method - {method}')

        if method == 'GET':
            if 'png' not in environ['PATH_INFO']:
                query_str = environ['QUERY_STRING']
                print(f'Query String - {query_str}')
                request_params = GetRequests.get_params(environ)
                request['Request_params'] = Framework.decode_val(request_params)
                print(f"Get params - {request['Request_params']}")

        if method == 'POST':
            data = PostRequests().get_request(environ)
            request['data'] = Framework.decode_val(data)
            print(f"Post Request - {Framework.decode_val(data)}")

        for item in self.front:
            item(request)

        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]

    @staticmethod
    def decode_val(data):
        decode_data = {}
        for key, value in data.items():
            val = bytes(value.replace('%', '=').replace("+", " "), 'UTF-8')
            val_decode_str = decodestring(val).decode('UTF-8')
            decode_data[key] = val_decode_str
        return decode_data
