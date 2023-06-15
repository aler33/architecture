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

        for item in self.front:
            item(request)

        code, body = view(request)
        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]
