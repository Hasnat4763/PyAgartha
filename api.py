from webob import Request, Response
import parse
import json


class API:
    def __init__(self):
        self.routes = {}

    def __call__(self, env, start_response):
        request = Request(env)
        response = self.handle_request(request)
        return response(env, start_response)

    def find_handler(self, reqpath, reqmethod):
        for (path, method), handler in self.routes.items():
            if method != reqmethod:
                continue

            parse_result = parse.parse(path, reqpath)
            if parse_result is not None:
                return handler, parse_result.named
        return None, None

    def handle_request(self, request):
        handler, kwargs = self.find_handler(request.path, request.method)

        if handler is None:
            resp = Response()
            resp.status_code = 404
            resp.text = "404 Not Found"
            return resp

        result = handler(request, **(kwargs or {}))

        if isinstance(result, Response):
            return result

        if isinstance(result, dict):
            resp = Response(json_body=result)
            return resp

        resp = Response()
        resp.text = str(result)
        return resp

    def route(self, path, method="GET"):
        def wrapper(handler):
            self.routes[(path, method)] = handler
            return handler
        return wrapper
