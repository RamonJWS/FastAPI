from fastapi import FastAPI

app = FastAPI()
# the operation is GET
# the endpoint is <http.../home>
@app.get("/home")
def index():
    return {"message": "Hello World!"}
