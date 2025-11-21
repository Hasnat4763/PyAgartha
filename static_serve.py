import os
import mimetypes
from response import Response
from templating import render_template

class StaticServe:
    def __init__(self, static_directory = "static"):
        self.static_directory = static_directory
        if not os.path.exists(static_directory):
            os.makedirs(static_directory)
            
            
    def serve_static(self, filepath):
        if filepath.startswith("/static/"):
            filepath = filepath[len("/static/"):]
        full_path = os.path.join(self.static_directory, filepath)
        full_path = os.path.abspath(full_path)
        static_directory_abs = os.path.abspath(self.static_directory)
        
        if not full_path.startswith(static_directory_abs):
            return Response(status=403,
                            content_type="text/plain",
                            content= b"Access forbidden"
                            ).send_to_webob()
        
        try:
            with open(full_path, 'rb') as f:
                content = f.read()
                
            content_type, _ = mimetypes.guess_type(full_path)
            if content_type is None:
                content_type = "application/octet-stream"
                
            response = Response(status=200, content_type=content_type)
            response.content = content
            return response.send_to_webob()
        except Exception as e:
            return Response(status=500).html_content(render_template("500.html", e=e, show_error=True)).send_to_webob()
            