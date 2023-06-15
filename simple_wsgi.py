def application(environ, start_response):
    """
    For start run in console:  uwsgi --http :8000 --wsgi-file simple_wsgi.py
    """
    start_response('200 OK', [('Content-Type', 'text/html')])
    return [b'This is test uWSGI!']
