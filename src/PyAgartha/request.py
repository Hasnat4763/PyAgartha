import cgi
from urllib.parse import parse_qs
from http.cookies import SimpleCookie
import json

class Request:
    def __init__(self, env):
        self.env = env
        self.method = env.get("REQUEST_METHOD", "GET")
        self.path = env.get("PATH_INFO", "/")
        self.args = {k: v[0] for k, v in parse_qs(env.get("QUERY_STRING", "")).items()}
        self.form = {}
        self.files = {}  # store uploaded files
        self.json = None
        self.headers = {}
        self.cookies = {}
        self._body = None

        # parse headers
        for k, v in env.items():
            if k.startswith("HTTP_"):
                header_name = k[5:].replace("_", "-").title()
                self.headers[header_name] = v
            elif k in ("CONTENT_TYPE", "CONTENT_LENGTH"):
                self.headers[k] = v

        # parse cookies
        cookie = SimpleCookie()
        cookie.load(env.get("HTTP_COOKIE", ""))
        self.cookies = {k: morsel.value for k, morsel in cookie.items()}

        content_type = env.get("CONTENT_TYPE", "")
        content_length = int(env.get("CONTENT_LENGTH", 0) or 0)

        if self.method in ["POST", "PUT", "PATCH"] and content_length > 0:
            # handle multipart/form-data (file uploads)
            if "multipart/form-data" in content_type:
                fs = cgi.FieldStorage(fp=env["wsgi.input"], environ=env, keep_blank_values=True)
                for key in fs:
                    field_item = fs[key]
                    if field_item.filename:  # file
                        self.files[key] = field_item
                    else:
                        self.form[key] = field_item.value
            else:
                # read as text for form-urlencoded or JSON
                self._body = env["wsgi.input"].read(content_length).decode("utf-8")
                if "application/x-www-form-urlencoded" in content_type:
                    parsed = parse_qs(self._body)
                    self.form = {k: v[0] for k, v in parsed.items()}
                elif "application/json" in content_type:
                    try:
                        self.json = json.loads(self._body)
                    except json.JSONDecodeError:
                        self.json = None
