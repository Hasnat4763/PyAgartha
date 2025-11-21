from response import Response
from webob import Response as WebobResponse
from wsgiref.util import FileWrapper
import os, mimetypes
from templating import render_template

class StaticServe:
    def __init__(self, static_directory="static"):
        self.static_directory = static_directory
        os.makedirs(static_directory, exist_ok=True)

    def serve_static(self, filepath):
        if filepath.startswith("/static/"):
            filepath = filepath[len("/static/"):]
        full_path = os.path.join(self.static_directory, filepath)
        full_path = os.path.abspath(full_path)
        static_dir_abs = os.path.abspath(self.static_directory)
        if not full_path.startswith(static_dir_abs):
            return Response(
                status=403,
                content_type="text/plain",
                content=b"Access forbidden"
            )
        if not os.path.isfile(full_path):
            return Response(
                status=404,
                content=render_template("404.html")
            )

        try:
            content_type, _ = mimetypes.guess_type(full_path)
            if content_type is None:
                content_type = "application/octet-stream"
            with open(full_path, "rb") as f:
                data = f.read()

            return Response(
                status=200,
                content_type=content_type,
                content=data
            )

        except Exception as e:
            return Response(
                status=500,
                content=render_template("500.html", e=e, show_error=True)
            )
