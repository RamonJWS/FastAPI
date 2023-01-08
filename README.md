# Learning FastAPI

## <ins>Parameters</ins>
### Request Body
**POST** </br>
This is when data is sent to the API, the API must then be able to retrieve this information or use it
appropriately. </br>
More of the information is sent in the request body rather than the query parameters.
FastAPI uses ```Pydantic BaseModel``` to convert the data between ```json``` and the model. e.g. below the request body will
be converted from ```json``` type to ```BlogModel``` type.
```python
class BlogModel(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True
```
The model will expect a json file in the following format (this can be seen in the request body of swagger docs):
```json
{
  "title": "string",
  "content": "string",
  "published": true
}
```
**Nice Things**
- request body as json.
- automatic data validation using typing.
- automatic data conversion using pydantic models.
- output json schema. 

### Path and Query Parameters

### Parameter Metadata

### Validators

### Multiple Values

### Number Validators

### Complex Subtypes

## <ins>Routers</ins>
Routers are used to structure API code into different files and components. e.g. in Routers/main.py I have split
the get and post requests into different files ```blog_post.py``` and ```blog_get.py```. Inside both files instead
of importing ```FastAPI``` I import ```APIrouter```. Within ```APIrouter``` a prefix can be defined which adds a path
to the endpoint, a tag can also be added to better organise methods in the documentation.

```python
router = APIRouter(
    prefix="/blog",
    tags=["blog"]
)
```

```@router.get(...)``` is then the decorator instead of ```@app.get(...)```. Inside of ```main.py``` ```blog_post.py```
and ```blog_get.py``` need to have the router imported:

```python
from fastapi import FastAPI
from router import blog_get, blog_posts

app = FastAPI()
app.include_router(blog_get.router)
app.include_router(blog_posts.router)
```