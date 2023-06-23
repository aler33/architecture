class GetRequests:

    @staticmethod
    def parse_data(data):
        result = {}
        if data:
            query_params = data.split('&')
            for item in query_params:
                key, value = item.split('=')
                result[key] = value
        return result

    @staticmethod
    def get_params(environ):
        query_str = environ['QUERY_STRING']
        return GetRequests.parse_data(query_str)


class PostRequests:

    @staticmethod
    def parse_data(data):
        result = {}
        if data:
            query_params = data.split('&')
            for item in query_params:
                key, value = item.split('=')
                result[key] = value
        return result

    @staticmethod
    def get_wsgi_data(environ):
        content_length_data = environ.get('CONTENT_LENGTH')
        content_length = int(content_length_data) if content_length_data else 0
        return environ['wsgi.input'].read(content_length) if content_length > 0 else b''

    def parse_wsgi_data(self, data):
        result = {}
        if data:
            data_str = data.decode(encoding='utf-8')
            print(f'String after coding - {data_str}')
            result = self.parse_data(data_str)
        return result

    def get_request(self, environ):
        data = self.get_wsgi_data(environ)
        return self.parse_wsgi_data(data)
