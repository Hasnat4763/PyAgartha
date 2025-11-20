from api import API
app = API()
@app.route("/")
def home(request):
    return '''
    <html>
    <head>
    <title>
    Agartha
    </title>
    </head>
    <body>
    <p>
    I am Agartha
    </p>
    </body>
    </html>
    '''


@app.route("/about")
def about(request):
    return "AGARTHA WEB"
    
@app.route("/nigga")
def nigga(request):
    return f"{request.user_agent} you are a nigga"
    
@app.route("/sigma/{name}")
def sigma(request, name):
    return f"{name} Hi! im gonna hack you"