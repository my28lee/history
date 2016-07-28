class HTTPMethodOverrideMiddleware(object):
    allowed_methods = frozenset([
        'GET',
        'POST',
        'DELETE',
        'PUT'
    ])

    bodyless_methods = frozenset([
        'GET'
    ])

    def __init__(self,app):
        self.app = app

    def __call__(self, environ,start_response):
        method = environ.get('HTTP_X_HTTP_METHOD_OVERRIDE','').upper()
        #print 'method',environ
        if method in self.allowed_methods:
            method = method.encode('ascii','replace')
            environ['REQUEST_METHOD'] = method

        if method in self.bodyless_methods:
            environ['CONTENT_LENGTH'] = '0'

        return self.app(environ,start_response)