from webob import Request
import parse
from response import Response
from templating import render_template


class API:
    def __init__(self):
        self.routes = {}
        self.static_handler = None

    def __call__(self, env, start_response):
        request = Request(env)
        response = self.handle_request(request)
        if isinstance(response, Response):
            response = response.send_to_webob()
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
        try:
            if self.static_handler and request.path.startswith("/static/"):
                return self.static_handler.serve_static(request.path)
            handler, kwargs = self.find_handler(request.path, request.method)
            if handler is None:
                return Response(status=404).html_content(render_template("404.html", show_error=False)).send_to_webob()

            result = handler(request, **(kwargs or {}))
            if isinstance(result, Response):
                return result.send_to_webob()
            else:
                return Response(str(result)).send_to_webob()
        except Exception as e:
            import traceback
            tracebackinfo = traceback.format_exc()
            print(tracebackinfo)
            return Response(status=500).html_content(render_template("500.html", e=e, show_error=True)).send_to_webob()
    def static_route(self, static_directory="static"):
        from static_serve import StaticServe
        self.static_handler = StaticServe(static_directory)

    
    def route(self, path, method="GET"):
        def wrapper(handler):
            self.routes[(path, method)] = handler
            return handler
        return wrapper
