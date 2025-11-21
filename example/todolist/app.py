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
    todo_data = []
    for todo in TODOS:
        todo_data.append({
            'task': todo['task'],
            'id': str(todo['id']),
            'completed': 'completed' if todo['completed'] else '',
            'checkbox': '✓' if todo['completed'] else '○'
        })
    
    return app.render_template("index.html", 
                               todos=TODOS,
                               todo_list=todo_data,
                               has_todos='yes' if TODOS else '')

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

@app.get("/api/todos/{todo_id}")
def get_todo_status(request, todo_id):
    todo_id = int(todo_id)
    todo = next((t for t in TODOS if t["id"] == todo_id), None)
    if not todo:
        return app.json({"error": "Not Found"}, status=404)
    return app.json(todo)

@app.post("/api/todos")
def add_todo(request):
    data = request.json
    if not data or "task" not in data:
        return app.json({"error": "Task Required"}, status=400)

    new_id = max([t["id"] for t in TODOS], default=0) + 1
    new_todo = {
        "id": new_id,
        "task": data["task"],
        "completed": False
    }
    TODOS.append(new_todo)
    return app.json(new_todo, status=201)

@app.get("/about")
def get_about(request):
    return app.json({
        "Framework": "PyAgartha",
        "Version": "0.6.7",
        "Author": "Hasnat4763",
        "Description": "A simple and lightweight webn framework for python to be used for small personal projects. Made for learning."
        
    })


if __name__ == "__main__":
    from wsgiref.simple_server import make_server
    server = make_server("localhost", 8080, app)
    server.serve_forever()