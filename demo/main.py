import logging

from another import Another, Status, Request, Response


app = Another()


@app.use()
def log_request_middleware(req: Request, res: Response):
	print("LOGGER", req.method, req.path)
	return req

@app.get("/route")
def get_route(req: Request):
	return Response({"message": "hello world"}, status=Status.HTTP_200_OK)


@app.post("/route")
def post_route(req: Request):
	return Response({**req.body, **req.query}, status=Status.HTTP_200_OK)