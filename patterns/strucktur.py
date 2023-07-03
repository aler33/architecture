from time import time


class AppRoute:
    def __init__(self, routes, url):
        self.routes = routes
        self.url = url

    def __call__(self, cls):
        if isinstance(self.url, list):
            for ur in self.url:
                self.routes[ur] = cls()
        else:
            self.routes[self.url] = cls()


class Debug:

    def __init__(self, name):
        self.name = name

    def __call__(self, cls, *args, **kwargs):

        def timeit(func):

            def timed(*args, **kwargs):
                time_start = time()
                result = func(*args, **kwargs)
                time_end = time()
                time_result = time_end - time_start
                print(f'Run time function {self.name} --- {time_result}')
                return result
            return timed
        return timeit(cls)
