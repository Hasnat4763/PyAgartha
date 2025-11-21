import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from api import API
app = API()
app.static_route(static_directory="example/todolist/static")
app.template_path("example/todolist/templates")

TODOS = [
    {
        "id":1, "task": "Making a Basic Web Framework", "completed": True
    },
    {
        "id":2, "task": "Creating Demo App", "completed": False
    },
    {
        "id":3, "task": "Write Documentation", "completed": False
    },
    {
        "id":4, "task": "Submit to PyPI", "completed": False
    },
    {
        "id":5, "task": "Submit to Siege", "completed": False
    }

]


@app.get("/")
def home(request):
    return app.render_template("index.html", todos=TODOS)

@app.post("/add")
def add_todo_items(request):
    task = request.form.get("task", "").strip()
    if task:
        new_id = max([t["id"] for t in TODOS], default=0) + 1
        TODOS.append({"id": new_id, "task": task, "completed": False})
        
    return app.redirect("/")


@app.post("/complete/{todo_id}")
def mark_completed(request, todo_id):
    todo_id = int(todo_id)
    for todo in TODOS:
        if todo["id"] == todo_id:
            todo["completed"] = not todo["completed"]
            break
    return app.redirect("/")

@app.post("/delete/{todo_id}")
def delete_todo(request, todo_id):
    todo_id = int(todo_id)
    global TODOS
    for todos in TODOS:
        if todos["id"] == todo_id:
            TODOS.remove(todos)
            break
    return app.redirect("/")

@app.get("/api/todos")
def get_todo_api(request):
    return app.json(
        {
            "todos": TODOS,
            "total": len(TODOS),
            "completed": len([t for t in TODOS if t['completed']]),
            "pending": len([t for t in TODOS if not t['completed']])
        }
    )
    
    
if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    server = make_server("localhost", 8080, app)
    server.serve_forever()