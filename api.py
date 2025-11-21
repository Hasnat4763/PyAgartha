import os
from request import Request
import parse
from response import Response
from templating import render_template
from middleware import Middleware
class API:
    def __init__(self):
        self.routes = {}
        self.static_handler = None
        self.middleware = Middleware()
        
    def __call__(self, env, start_response):
        import asyncio
        request = Request(env)
        response = asyncio.run(self.handle_request(request))
        if isinstance(response, Response):
            response = response.send_to_webob()
        return response(env, start_response)
    def find_handler(self, reqpath, reqmethod):
        for (path, method), handler in self.routes.items():
            if method != reqmethod:
                continue
            
            convert_path = path.replace("<", "{").replace(">", "}")
            
            parse_result = parse.parse(convert_path, reqpath)
            if parse_result is not None:
                return handler, parse_result.named
        return None, None
    async def handle_request(self, request):
        try:
            early_response = await self.middleware.execute_b4(request)
            if early_response is not None:
                return await early_response.send_to_webob()
            if self.static_handler and request.path.startswith("/static/"):
                return self.static_handler.serve_static(request.path).send_to_webob()
            handler, kwargs = self.find_handler(request.path, request.method)
            if handler is None:
                response = Response(status=404)
                if os.path.exists("templates/404.html"):
                    response.html_content(render_template("404.html", show_error=False))
                else:
                    response.text_content("404 Not Found")
                return response.send_to_webob()
            result = handler(request, **(kwargs or {}))
            if not isinstance(result, Response):
                result =  Response(str(result))
            result = await self.middleware.execute_after(request, result)
            return result.send_to_webob()
        except Exception as e:
            import traceback
            tracebackinfo = traceback.format_exc()
            print(tracebackinfo)
            response = Response(status=500)
            if os.path.exists("templates/500.html"):
                response.html_content(render_template("500.html", e=e, show_error=True))
            else:
                response.text_content("500 Internal Server Error \n\n" + str(e))
            return response.send_to_webob()
    def static_route(self, static_directory="static"):
        from static_serve import StaticServe
        self.static_handler = StaticServe(static_directory)
    
    def template_path(self, name):
        import templating
        templating.template_path(name)
    
    def render_template(self, template_name, **context):
        from templating import render_template
        return render_template(template_name, **context)
    
    def route(self, path, method="GET"):
        def wrapper(handler):
            self.routes[(path, method)] = handler
            return handler
        return wrapper
    
    def get(self, path):
        return self.route(path, method="GET")
    
    def post(self, path):
        return self.route(path, method="POST")
    
    def put(self, path):
        return self.route(path, method="PUT")
    
    def delete(self, path):
        return self.route(path, method="DELETE")
    
    def patch(self, path):
        return self.route(path, method="PATCH")
    
    def add_b4_req(self, func):
        self.middleware.b4_req.append(func)
        
    def add_after_req(self, func):
        self.middleware.after_req.append(func)
    
    def Response(self,content, status, content_type, headers):
        from response import Response
        return Response(content=content, status=status, content_type=content_type, headers=headers)
    
    
    def json(self, data, status=200):
        response = Response(status=status)
        response.json_content(data)
        return response
    
    def html(self, html, status=200):
        response = Response(status=status)
        response.html_content(html)
        return response
    
    def text(self, text, status=200):
        response = Response(status=status)
        response.text_content(text)
        return response
    
    def redirect(self, url, status=302):
        response = Response()
        response.redirect(url, status=status)
        return response