# PyAgartha

A lightweight web framework inspired from Flask

# Installation



# Usage

It's function and routing is just like Flask

There is a basic demo "TO DO List" app in [Demo](example/todolist/) which you can check out

```python
from pyagartha import API

app = API()

@app.route("/")
def home(request):
    response.text = "Hello, World!
```

# License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details
