# Learning FastAPI

## <ins>Parameters</ins>
### Request Body
**POST** </br>
This is when data is sent to the API, the API must then be able to retrieve this information or use it
appropriately. </br> </br>
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
Body parameters are our model parameters and query parameters are our more primitive parameters e.g. ```id: int```</br>
```python
@router.post("/new/{id}")
def create_blog(blog: BlogModel, id: int, version: int = 1):
    return {
        "id": id,
        "data": blog,
        "version": version
    }
```
Above there is now a path parameter ```id``` and a query parameter ```version```. If and ```id``` is 1 then the URL
for this endpoint is  ```http://127.0.0.1:8000/blog/new/12?version=1``` and the response body would be:
```json
{
  "id": 12,
  "data": {
    "title": "string",
    "content": "string",
    "published": true
  },
  "version": 1
}
```

### Parameter Metadata
This is about adding information about the data we're working with (data about our data), this data is usually
displayed in the swagger documentation. </br> </br>
```from fastapi import Query, Path, Body``` imports are used to attach this meta data. The example below looks at adding
meta data to the query parameter ```comment_id```:
```python
@router.post("/new/{id}/comment")
def create_comment(blog: BlogModel,
                   id: int,
                   comment_id: int = Query(None,
                                           title="Id of the comment",
                                           description="Some description for comment id",
                                           alias="different_comment_id")):
    return {
        "blog": blog,
        "id": id,
        "comment_id": comment_id
    }
```
In the documentation next to the query parameter ```comment_id``` there will now be a description! ```alias```
is used for renaming the variable in the docs. The first parameter ```None``` is the default value.</br>
The same thing can be doen to ```id``` using ```Path```, and ```Body``` for ```blog```.

### Validators
In the above example the ```Query``` parameter is optional, how do we have metadata with a non-optional parameter?
This can be done by replacing ```None``` with ```Elipsis``` (```== ...```). Below is an example of this for a request
body parameter, so it must be in the request otherwise we'll get ```422 Unprocessable Entity```.</br> </br>
Minimum and maximum length of blog posts can also be validated using the below arguments in ```Body```, finally regex
can be used to ensure only certain message data can be passed, below only lowercase letter and spaces can be used.
```python
@router.post("/new/{id}/comment")
def create_comment(blog: BlogModel,
                   id: int,
                   comment_id: int = Query(None,
                                           title="Id of the comment",
                                           description="Used to identify which comment is which",
                                           alias="commentId"),
                   content: str = Body(Ellipsis,
                                       min_length=10,
                                       max_length=50,
                                       regex="^[a-z\s]*$")):
    return {
        "blog": blog,
        "id": id,
        "comment_id": comment_id,
        "content": content
    }
```

### Multiple Values
Its also possible to have multiple query parameters. This can be done by defining an optional list of whatever we want.
This needs to be optional as query parameters are always optional. This optional value can then be assigned either to 
None or to a list of values:

```python
@router.post("/new/{id}/comment")
def create_comment(blog: BlogModel,
                   id: int,
                   comment_id: ...,
                   content: ...,
                   version: Optional[List[str]] = Query(["1.1", "1.2", "1.2.1"])):
    return {
        "blog": blog,
        "id": id,
        "comment_id": comment_id,
        "content": content,
        "version": version
    }
```
Request URL: ```http://127.0.0.1:8000/blog/new/23/comment?version=1.1&version=1.2&version=1.2.1```

### Number Validators
This is used to validate numbers as either path, body or query parameters. There are 4 main validations for numbers: 
`>=, >, <=, <`, this can be seen using the `Path` parameter below:
```python
@router.post("/new/{id}/comment/{comment_id}")
def create_comment(blog: BlogModel,
                   id: int,
                   comment_title: ...,
                   content: str = ...,
                   version: ...,
                   comment_id: int = Path(None, gt=5, le=10)):
    return {
        "blog": blog,
        "id": id,
        "comment_title": comment_title,
        "content": content,
        "version": version,
        "comment_id": comment_id
    }
```

### Complex Subtypes
This can be used to define the type of data in the request body. The usualy suspects can be used e.g. `Dict, List,
Optional`, more complex structures can be used also like models inside the model:
```python
class Image(BaseModel):
    url: str
    alias: str
    
class BlogModel(BaseModel):
    title: str
    content: str
    published: Optional[bool] = True
    tags: List[str] = []
    metadata: Dict[str, str] = {"key1": "val1"}
    image: Optional[Image] = None
```
The last parameter is an optional one of type Image defined above.

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
## <ins>Database with SQLAlchemy</ins>
### Dependencies
- A way to allow a function to depend on another function.
- Allow for importing of functionality.

Below I have defined a function `required_parameter` in `blog_posts.py`, I can then import this function into
`blog_get.py` and use this as a argument in the functions there with `Depends` from FastAPI.
```python
# blog_post.py
def required_functionality():
    return {"message": "Learning FastAPI is important"}
```
```python
# blog_get.py
from Routers.router.blog_posts import required_functionality

@router.get("/all")
def get_all_blogs(page=1, page_size: Optional[int] = None, req_parameters: dict = Depends(required_functionality)):
    return {"messages": f"All {page_size} blogs on page {page}", "req": req_parameters}
```
An example of where this is used in the wild is for endpoint authentication.

### Databases in FastAPI


### Create Databases and Tables


### Write Data


### Create and Read


### Update and Delete


### Relationships


