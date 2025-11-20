from webob import Request, Response

class API:
    def __call__(self, env, start_response):
        request = Request(env)
        response = Response()
        response.text = "Hello, World!"
        return response(env, start_response)