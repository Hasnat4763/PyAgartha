from api import API
from api import render_template
from api import Response


app = API()
app.static_route(static_directory="static")
app.template_path("htmls")

@app.route("/")
def home(request):
    return Response().html_content(render_template("index.html", items = ["<a href=\"/about\">about</a>", 
                                                                                         "<a href=\"/peter\">Sigma</a>",
                                                                                         "<a href=\"/peter\">Sigma</a>"],
                                                   csses=["/static/app.css", "/static/sigma.css"],
                                                   css_available=True,
                                                   show_footer=True,
                                                   year=2025))

@app.route("/about")
def about(request):
    return Response().json_content({
        "app": "PyAgartha",
        "author": "Hasnat4763",
        "version": "0.6.7",
        "description": "A lightweight Python Web Framework"
        
    })

@app.route("/sigma/{name}")
def sigma(request, name):
    return Response().text_content(f"{name} Hi! im gonna hack you")

@app.route("/peter")
def peter(request):
    return Response().html_content('''
                                   <!DOCTYPE html>
                                   <html>
                                    <head>
                                        <title>Peter Page</title>
                                        <meta charset="UTF-8">
                                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                                        <link rel="stylesheet" href="/static/app.css">
                                        <style>
                                            body {
                                                font-family: Arial, sans-serif;
                                                background-color: #f0f0f0;
                                                margin: 20px;
                                                padding: 20px;
                                                border-radius: 8px;
                                                }
                                        </style>
                                    </head>
                                    <body>
                                    <h1>Welcome to Peter's Page</h1>
                                    </body>
                                   </html>
                                   '''
                                   )