import os
import traceback
from .request import Request
import parse
from .response import Response
from .sessions import SessionManager
from .templating import render_template
from .middleware import Middleware
from .templating import template_path, render_template
from .static_serve import StaticServe
class API:
    def __init__(self):
        self.routes = {}
        self.static_handler = None
        self.middleware = Middleware()
        self.sessions = SessionManager()
        
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
            
            convert_path = path.replace("<", "{").replace(">", "}")
            
            parse_result = parse.parse(convert_path, reqpath)
            if parse_result is not None:
                return handler, parse_result.named
        return None, None
    
    
    def handle_request(self, request):
        try:
            
            # Before Middleware
            
            early_response = self.middleware.execute_b4(request)
            if early_response is not None:
                    return early_response

            
            #Static File Serving
            
            if self.static_handler and request.path.startswith("/static/"):
                result = self.static_handler.serve_static(request.path)
                return result.send_to_webob()

            
            # Session Management
            
            cookie = request.cookies.get("session_id")
            session = self.sessions.get(cookie)
            if session is None:
                cookie = self.sessions.create_session()
                session = self.sessions.get(cookie)

            if session is not None:
                request.session = session["data"]
            else:
                request.session = {}

            # Routing
            
            handler, kwargs = self.find_handler(request.path, request.method)
            if handler is None:
                response = Response(status=404)
                if os.path.exists("templates/404.html"):
                    response.html_content(render_template("404.html", show_error=False))
                else:
                    response.text_content("404 Not Found")
                    
                response.set_cookie("session_id", cookie)
                return response.send_to_webob()
        
            # user Handler calling
        
            result = handler(request, **(kwargs or {}))
            if isinstance(result, Response):
                result = result.send_to_webob()
            elif isinstance(result, str):
                result = Response(result).send_to_webob()
                            
            # After Middleware    
                
            for fn in self.middleware.after_req:
                after = fn(request, result)
                if after:
                    return after

            result.set_cookie("session_id", cookie)
            return result
        except Exception as e:
            tracebackinfo = traceback.format_exc()
            print(tracebackinfo)
            response = Response(status=500)
            if os.path.exists("templates/500.html"):
                response.html_content(render_template("500.html", e=e, show_error=True))
            else:
                response.text_content("500 Internal Server Error \n\n" + str(e))
            return response.send_to_webob()
    def static_route(self, static_directory="static"):
        self.static_handler = StaticServe(static_directory)
    
    def template_path(self, name):
        template_path(name)
    
    def render_template(self, template_name, **context):
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
        return Response(content=content, status=status, content_type=content_type, headers=headers).send_to_webob()
    
    
    def json(self, data, status=200):
        response = Response(status=status)
        response.json_content(data)
        return response.send_to_webob()
    
    def html(self, html, status=200):
        response = Response(status=status)
        response.html_content(html)
        return response.send_to_webob()
    
    def text(self, text, status=200):
        response = Response(status=status)
        response.text_content(text)
        return response.send_to_webob()
    
    def redirect(self, url, status=303):
        response = Response()
        response.redirect(url, status=status)
        return response.send_to_webob()