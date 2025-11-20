from api import API
from templating import render_template
from response import Response


app = API()
@app.route("/")
def home(request):
    return Response().html_content(render_template("index.html", user="Hasnat", items = ["<a href=\"/about\">about</a>", 
                                                                                         "<a href=\"/sigma/peter\">Sigma</a>",
                                                                                         "Cherry"],
                                                   show_footer=True,
                                                   year=2025))

@app.route("/about")
def about(request):
    return Response().json_content({
        "app": "PyAgartha",
        "author": "Hasnat4763",
        "version": "0.6.7"
    })

@app.route("/sigma/{name}")
def sigma(request, name):
    return Response().text_content(f"{name} Hi! im gonna hack you")