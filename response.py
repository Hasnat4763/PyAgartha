import json
from webob import Response as WebobResponse

class Response:
    def __init__(self, content=None, status=200, content_type=None, headers=None):
        self.status = status
        self.headers = headers or {}
        self.content = content
        self.content_type = content_type or "text/html"

    def text_content(self, text: str):
        self.content_type = "text/plain"
        self.content = text
        return self

    def html_content(self, html: str):
        self.content_type = "text/html"
        self.content = html
        return self

    def json_content(self, data):
        self.content_type = "application/json"
        self.content = json.dumps(data)
        return self

    def redirect(self, url: str, status=302):
        self.status = status
        self.headers["Location"] = url
        self.content = f"Redirecting to {url}, if not automatic, <a href=\"{url}\">click here</a>."
        return self

    def set_cookie(self, name, value, path="/", http_only=True, max_age=None):
        cookie = f"{name}={value}; Path={path}"
        if http_only:
            cookie += "; HttpOnly"
        if max_age is not None:
            cookie += f"; Max-Age={max_age}"
        self.headers["Set-Cookie"] = cookie

    def delete_cookie(self, name, path="/"):
        self.set_cookie(name, "", path=path, max_age=0)

    def send_to_webob(self):
        if isinstance(self.content, bytes):
            resp = WebobResponse(body=self.content, status=self.status)
        else:
            resp = WebobResponse(text=self.content or "", status=self.status)
        resp.content_type = self.content_type

        for key, value in self.headers.items():
            resp.headers[key] = value
        return resp
