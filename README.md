# Another
"Another" Python backend framework, for fun.

## Installation

```bash
pip install another
```

You also need an ASGI server, such as [Uvicorn](https://github.com/encode/uvicorn) or [Granian](https://github.com/emmett-framework/granian).

```bash
pip install uvicorn
# or
pip install granian
```

## Usage

Create a `main.py` file and copy-paste the following snippet into it.

```python
from another import Another, Status, Request, Response


app = Another()

@app.get("/hello")
def hellow_another(req: Request):
	return Response({
        "message": "Hello!",
        "extra": req.query
    }, status=Status.HTTP_200_OK)
```

And then run the server:

```bash
uvicorn main:app
```

Now open this link [localhost:8000/hello?first_name=Mads&last_name=Mikkelsen](http://localhost:8000/hello?first_name=Mads&last_name=Mikkelsen) in your browser.
