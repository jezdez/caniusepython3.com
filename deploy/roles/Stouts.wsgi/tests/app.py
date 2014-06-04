""" Simplest wsgi application. """


def application(environ, start_response):
    """ Hello world. """
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return ['Hello world!\n']
