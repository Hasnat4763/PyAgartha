from urllib.parse import parse_qs
from http.cookies import SimpleCookie
import json

class Request:
    def __init__(self, env):
        self.env = env
        self.method = env.get("REQUEST_METHOD", "GET")
        self.path = env.get("PATH_INFO", "/")
        args_parsed = parse_qs(env.get("QUERY_STRING", ""))
        self.args = {k: value[0] for k, value in args_parsed.items()}
        self.form = {}
        self.json = None
        self.headers = {}
        self.cookies = {}
        self._body = None
        for k, v in env.items():
            if k.startswith("HTTP_"):
                header_name = k[5:].replace("_", "-").title()
                self.headers[header_name] = v
            elif k in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
                self.headers[k] = v
        cookie = SimpleCookie()
        cookie.load(env.get('HTTP_COOKIE', ''))
        self.cookies = {k: morsel.value for k, morsel in cookie.items()}
        content_type = env.get('CONTENT_TYPE', '')
        if self.method in ['POST', 'PUT', 'PATCH']:
            content_length = int(env.get('CONTENT_LENGTH', 0))
            if content_length > 0:
                self._body = env['wsgi.input'].read(content_length).decode('utf-8')
        if self._body:
            if 'application/x-www-form-urlencoded' in content_type:
                form_parsed = parse_qs(self._body)
                self.form = {k: value[0] for k, value in form_parsed.items()}
            elif 'application/json' in content_type:
                try:
                    self.json = json.loads(self._body)
                except json.JSONDecodeError:
                    self.json = None