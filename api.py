from webob import Request
import parse
from response import Response


class API:
    def __init__(self):
        self.routes = {}

    def __call__(self, env, start_response):
        request = Request(env)
        webob_response = self.handle_request(request)
        return webob_response(env, start_response)


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
            return Response("404 Not Found", status=404).send_to_webob()

        result = handler(request, **(kwargs or {}))
        if isinstance(result, Response):
            return result.send_to_webob()
        else:
            return Response(str(result)).send_to_webob()


    def route(self, path, method="GET"):
        def wrapper(handler):
            self.routes[(path, method)] = handler
            return handler
        return wrapper
