from api import API
from templating import render_template
from response import Response


app = API()
@app.route("/")
def home(request):
    return Response().html_content(render_template("index.html", user="Hasnat", items = ["Apple", "Banana", "Cherry"], show_footer=True, year=2025))

@app.route("/about")
def about(request):
    return "AGARTHA WEB"
    
@app.route("/nigga")
def nigga(request):
    return f"{request.user_agent} you are a nigga"
    
@app.route("/sigma/{name}")
def sigma(request, name):
    return f"{name} Hi! im gonna hack you"