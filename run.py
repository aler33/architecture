from wsgiref.simple_server import make_server
from alex_framework.main import Framework
from urls import routes, fronts

application = Framework(routes, fronts)

with make_server('', 8000, application) as server:
    print('server start on port 8000')
    server.serve_forever()
