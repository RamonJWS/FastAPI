from fastapi import FastAPI

app = FastAPI()

# path parameters:
# adding in {foo} in the end point allows for information to be passed from the frontend to backend through api
# FastAPI uses pydantic for type checking
@app.get('/blog/{id}')
def get_blog(id: int):
    return {"message": f"The users id is: {id}"}

# the order of arguments is important
# the blow wont work because the /all end point is intercepted by the /{id} first.
# put the below code before /{id} then /all will be used.
@app.get('/blog/all')
def get_all_blogs():
    return {'message': 'get all blogs'}
