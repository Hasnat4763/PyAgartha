from api import API
from templating import render_template


app = API()
@app.route("/")
def home(request):
    return render_template("index.html", user="Hasnat", items = ["Apple", "Banana", "Cherry"], show_footer=True)

@app.route("/about")
def about(request):
    return "AGARTHA WEB"
    
@app.route("/nigga")
def nigga(request):
    return f"{request.user_agent} you are a nigga"
    
@app.route("/sigma/{name}")
def sigma(request, name):
    return f"{name} Hi! im gonna hack you"