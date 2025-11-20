import json
from webob import Response as WebObResponse

class Response:
    def __init__(self, content=None, status=200, content_type="text/html", headers=None):
        self.status = status
        self.content_type = content_type
        self.headers = headers or {}
        self.content = content

    def text_content(self, text):
        self.content_type = "text/plain"
        self.content = text
        return self

    def html_content(self, html):
        self.content_type = "text/html"
        self.content = html
        return self

    def json_content(self, data):
        self.content_type = "application/json"
        self.content = json.dumps(data)
        return self
    def redirect(self, url, status = 302):
        self.status = status
        self.headers["Location"] = url
        self.content = f'Redirecting to {url}'
        return self
    def send_to_webob(self):
        resp = WebObResponse(body=self.content or "", status=self.status)
        resp.content_type = self.content_type
        for key, value in self.headers.items():
            resp.headers[key] = value
        return resp
