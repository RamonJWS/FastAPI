# Learning FastAPI

## <ins>Debug</ins>
To debug fastapi we need to add the following code:
```python
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
```

`__name__ == "__main__"` will run when calling the module from the command line but not on import.
We can then put a break point where ever and debug as normal!

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
- Often used to share database connections, enforce security, authentication, and roles.
- A way to allow a function to depend on another function.
- Allows for seamless import functionality (write function once) 
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
from router.blog_posts import required_functionality


@router.get("/all")
def get_all_blogs(page=1, page_size: Optional[int] = None, req_parameters: dict = Depends(required_functionality)):
    return {"messages": f"All {page_size} blogs on page {page}", "req": req_parameters}
```
An example of where this is used in the wild is for endpoint authentication.

### Databases in FastAPI
FastAPI can work with any relational database (MySQL, Oracle, etc.). </br>
With these databases I'm going to use a ORM (object relational mapper) this allows me to convert SQL to a more pythonic
syntax (it also requires less code), SQLAlchemy will be used for this.

![My Image](/rm_images/system.PNG)
The above is a diagram of a user creating a profile on our application.
- Schema is the accepted/required data the user will pass to us (email, password, username)
- Model is our conversion of this data into a usable/secure form that our ORM can use for inserting into the database.

### Create Databases and Tables
To create a database and create a connection to this database we can use the boiler plate code in `database.py` </br>
Once this has been created we can define models that our database will use (I'm using sqllite here with TablePlus
as a viewer). Below is an example of a model for creating user information:
```python
from db.database import Base
from sqlalchemy import Column
from sqlalchemy.sql.sqltypes import Integer, String

class DbUser(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
```
### Write Data
We have created a db, the db connection, and the model. We now need to create the schema, the ORM functionality,
and the API functionality. </br>
**How it works**:
- The router connects the user endpoint to the main app (user requests found in `user.py`)
```python
# user.py
@router.post('/', response_model=UserDisplay)
def create_user(request: UserBase,
                db: Session = Depends(get_db)):
    return db_user.create_user(db, request)
```
- Inside `user.py` a POST method is used with the request body that is of type `UserBase`, this is a schema that tells
FastAPI what format the request body should be in:
```python
# schemas.py
class UserBase(BaseModel):
    username: str
    email: str
    password: str
```
- Inside `create_user` function there is also a db argument which is mainly boilerplate code for creating a sqlalchemy
session and opening and closing the db connection (see `database.py` for more details).
- The user now creates an account with the following credentials:
```json
{
  "username": "EvilerEarth",
  "email": "email@gmail.com",
  "password": "password123"
}
```
- This is converted into a pydantic model `UserBase` and then passed to the `db_user.create_user(db, request)` function:
```python
# db_user.py
def create_user(db: Session, request: UserBase):
    # dont need id as this is auto generated as primary key in models.py
    new_user = DbUser(
        username=request.username,
        email=request.email,
        password=Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    # need to refresh because of id being primary key which is auto created for us.
    db.refresh(new_user)
    return new_user
```
- The pydantic model is then converted to sqlalchemys ORM model `DbUser`:
```python
# models.py
class DbUser(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
```
- This model creates the table with name "users" and assigns the pydantic models values to respective columns in the db
. Note that `id` was not in the pydantic model, it is automatically generated here as a primary key.
- Back to `db_user.py`. `password` is encrypted using hash (boilerplate code for this). The new_user (ORM model) is then
passed to the db, committed, and then the db is refreshed (refresh only needed due to `id` column).
- The new_user is then retured from `db_user.py` as an ORM model. In `user.py` in the POST decorator we have specified an
argument `response_model=UserDisplay`. This is used to dictate what is passed back in the response body:
```python
# schemas.py
class UserDisplay(BaseModel):
    username: str
    email: str

    class Config:
        orm_mode = True
```
- `class Config` is pydantic code that allows us to convert from ORM model to pydantic (which then converts to json).
The following response body is returned:
```json
{
  "username": "EvilerEarth",
  "email": "email@gmail.com"
}
```
Inside the database we can now see the information with the hashed password! Im using **TablePlus** to view the sqlite
db.

![My Image](/rm_images/create_user.PNG)

### Read
- Going to read data from an entire table and a single row of data. </br>

To read **ALL** users: We first create a query on the database model 
```python
# db_user.py
def get_all_users(db: Session):
    return db.query(DbUser).all()
```
We can then define the endpoint: here we dont want to return all user information just account name and email so we use 
`UserDisplay` response, this will be a list of json. We pass the db session to the `get_all_users` function defined in
`db_user.py`.
```python
# user.py
@router.get("/", response_model=List[UserDisplay])
def get_all_users(db: Session = Depends(get_db)):
    return db_user.get_all_users(db)
```
Easy! </br>

To read **ONE** user: we query the same table but filter it on id and return the first row found.
```python
# db_user.py
def get_one_user(id: int, db: Session):
    return db.query(DbUser).filter(DbUser.id == id).first()
```
Same as before we define the endpoint: No need for `List` as we return only one element. A path parameter is used for 
selection of users.
```python
# user.py
@router.get("/{id}", response_model=UserDisplay)
def get_one_user(id: int, db: Session = Depends(get_db)):
    return db_user.get_one_user(id, db)
```

### Update and Delete
**Update**</br>
To update a value in the database we need to use a `PUT` request. We also need to define the function that will handle
the db functionality: Below the functionality is we want to be able to update any or all of the users
data, we do this by filtering on the id.
```python
# db_user.py
def update_user(request: UserBase, db: Session, id: int):
    user = db.query(DbUser).filter(DbUser.id == id)
    user.update({
        DbUser.username: request.username,
        DbUser.email: request.email,
        DbUser.password: Hash.bcrypt(request.password)
    })
    db.commit()
    return db.query(DbUser).filter(DbUser.id == id).first()
```
We pass in the fastapi model `UserBase` which is a pydantic model, db which is the database connection, and the id of 
the user. We get the data from the correct table and store it in the `user` variable. Next we update `user`'s values 
with our request body from fastapi (dont forget to hash the new/old password!). Then commit this to the db, and finally
return the new users information to fastapi which will create the request response:
```python
# user.py
@router.put("/{id}/update", response_model=UserDisplay)
def update_username(request: UserBase, id: int, db: Session = Depends(get_db)):
    return db_user.update_user(request, db, id)
```
**Delete**</br>
To delete a user from the db (we should probably check auth, more on that later) its a similar process just using 
fastapis delete method and some new but simple db methods:
```python
# db_user.py
def delete_user(db: Session, id: int):
    user = db.query(DbUser).filter(DbUser.id == id).first()
    db.delete(user)
    db.commit()
    return f"User with id: {id} has been deleted!"
```
```python
# user.py
@router.delete("/{id}/delete")
def delete_user(id: int, db: Session = Depends(get_db)):
    return db_user.delete_user(db, id)
```

### Relationships
In this section I created a one to many relationship between the users and articles tables. Using sqlalchemy we define 
a foriegn key in the child database (the db with many) pointing to the primary key in the parent db (the db with
one). The relationship connection is then created: </br>
```python
class DbUser(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    items = relationship("DbArticle", back_populates="user")

class DbArticle(Base):
    __tablename__ = "articles"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    published = Column(Boolean)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("DbUser", back_populates="items")
```
We want to be able to create an article that is associated with a user. When we create an article (POST) the response 
body should contain information about the article and the user:
```python
# request body:
{
  "title": "The end",
  "content": "This is the end of things! I will not pay my bills any longer.",
  "published": true,
  "creator_id": 1
}

# response body:
{
  "title": "The end",
  "content": "This is the end of things! I will not pay my bills any longer.",
  "published": true,
  "user": {
    "id": 1,
    "username": "EvilerEarth"
  }
}
```
The response body for GET article will be the same as above. We also want this to work when we call users, where
all the articles created by the user will also be returned.
GET user:
```python
# parameter id = 1
{
  "username": "EvilerEarth",
  "email": "ee@gmail.com",
  "items": [
    {
      "title": "The end",
      "content": "This is the end of things! I will not pay my bills any longer.",
      "published": true
    }
  ]
}
```
I'm not going to go into detail about the backend sql queries (seen in `db_article.py`) because they're very similar to 
`db_users.py`. The main difference however is in the pydantic schemas, as these can now take into account the
relationships between the tables, cool right! </br> </br>
**Articles**: 
```python
# schemas.py
class ArticleBase(BaseModel):
    title: str
    content: str
    published: bool
    creator_id: int
    
class User(BaseModel):
    id: int
    username: str
    class Config:
        orm_mode = True

class ArticleDisplay(BaseModel):
    title: str
    content: str
    published: bool
    user: User
    class Config:
        orm_mode = True
```
The request body expects an article which has a title, content (the text), if its published, and the creator_id. This 
can all be seen in the `ArticleBase` class. The response body from this article creation then includes the title, 
content, published, and `user`. Here `user` is part of the relationship we set up in the sqlalchemy models, and allows
for the `User` class to be used which returns information about the user who created the article. Note how we're
only returning one user not a list, this is because there is only one user (one-to-many)</br> </br>
**User**:
```python
# schemas.py
class Article(BaseModel):
    title: str
    content: str
    published: bool
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str
    email: str
    password: str

class UserDisplay(BaseModel):
    username: str
    email: str
    items: List[Article] = []
    class Config:
        orm_mode = True
```
Above is a very similar but now we could return many articles (one-to-many). See the `List[Article]` part of 
the code.

## <ins>General API Knowledge</ins>
### Exceptions: </br>
HTTP status Codes:
- 1XX: Informational
- 2XX: Success
- 3XX: Redirection
- 4XX: Client Error
- 5XX: Server Error
<br/>\
To raise exceptions in the app we can use fastapi's built in `HTTPException`:
```python
# db_article.py
def get_article(db: Session, id: int):
    article = db.query(DbArticle).filter(DbArticle.id == id).first()
    if not article:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Article with id: {id} not found")
    return article
```
### Custome Exceptions </br>
Its also possible to create custom exceptions e.g. stop people putting emails into their articles.
- create a simple class to store the exception message
- raise the custom exception is content of article being created contains emails (simple regex for emails).
- Just doing the two above points would raise a 500 error which is unspecific.
- create an app exception handler in the main app module.
```python
# exceptions.py
class EmailException(Exception):
    def __init__(self, message: str):
        self.message = message
```
```python
# db_article.py
def create_article(db: Session, request: ArticleBase):
    list_of_emails = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', request.content)
    if list_of_emails:
        raise EmailException(f"Content contains email(s): {', '.join(list_of_emails)}")
    ...
```
```python
# main.py
@app.exception_handler(EmailException)
def email_exception_handler(request: Request, exc: EmailException):
    return JSONResponse(
        status_code=418,
        content={'detail': exc.message}
    )
```
```python
# request body:
{
  "title": "string",
  "content": "email@gmail.com, another one: hello@yahoo.com",
  "published": true,
  "creator_id": 0
}
        
# response body: 418 Error: I'm a Teapot
{
  "detail": "Content contains email(s): email@gmail.com, hello@yahoo.com"
}

```
### Custom Response:
The response is just what the request returns e.g. a pydantic model, a database model, dict, etc. </br>
We can create custom response objects to meet more specific needs, the downside of this is that there is not automatic
data conversion. </br>
**Why use Custom Responses**: </br>
- add meta data e.g. headers and cookies.
- can return different types of responses (not just json) e.g. images, plain text, html, files, streaming!
- complex decisional logic, the response can depend on multiple factors. e.g. return a xml or csv depending on the 
situation.
- better documentation, more information about the data. </br>

Below is an example where depending on a condition different datatypes can be returned, html or plain text.
```python
# product.py
from fastapi.responses import Response, HTMLResponse, PlainTextResponse
products = ['watch', 'camera', 'phone']

@router.get('/{id}')
def get_product(id: int):
    if id > len(products):
        out = "product not available"
        return PlainTextResponse(status_code=404, content=out, media_type='text/plain')
    else:
        product = products[id]
        out = f'''
        <head>
           '{product}'
        </head>
        '''
        return HTMLResponse(content=out, media_type='text/html')
```
If id is out of range then we return a plain text response with status code 404, else we return the product as a html
header. The issue with the above is that the documentation isn't clear, the **Code** section of the docs will not have
the right information:

![My Image](/rm_images/custom_response_bad.PNG)

To get the correct info we need to add an argument into the `router`:
```python
# product.py
@router.get('/{id}', responses={
    200: {
        'content': {
            'text/html': {
                'example': '<div>Product</div>'
                    }
               },
        'description': 'returns the html for an object'
        },

    404: {
        'content': {
            'text/plain': {
                'example': 'product not available'
                    }
               },
        'description': 'a clear text error message'
        }
})
def get_product(id: int):
...
```
This now give the correct documentation in the docs:

![My Image](/rm_images/custom_response_good.PNG)

### Headers
Headers are used to keep meta data about the request and response body of an API. We can create custom headers in
fastapi:
```python
from fastapi import Header

@router.get('/withheader/')
def get_products(custom_header: Optional[List[str]] = Header(default=None)):
    return products
```
![My Image](/rm_images/header.PNG)

In the swagger docs we can now provide a list of header information which will be added to the response body and request.
However, we wont be able to see this in header info in the curl and not in the response header... </br>
To get this info in the response header we need to use `Response` built in model:
```python
@router.get('/withheader121/')
def get_products(response: Response,
                 custom_header: Optional[List[str]] = Header(default=None)):
    response.headers['response_custom_header'] = ', '.join(custom_header)
    return products
```
![My Image](/rm_images/header_response.PNG)

### Cookies
- create custom cookies
- return custom cookies in response body

Cookies store information on the browser, this information can be user identification e.g. usernames and passwords. 
They can accept almost any data type. </br></br>
**Create custom cookie**:
```python
# product.py
@router.get('/createcookie/')
def create_cookie(response: Response):
    response.set_cookie(key='custom_cookie', value='cookie_value')
    return products
```
Looking in a cookie manager we can see the cookie:

![My Image](/rm_images/cookie.PNG)

**Return custom cookie**:
```python
# product.py
from fastapi import Cookie

@router.get('/getcookie/')
def get_cookie(custom_cookie: Union[str, None] = Cookie(None)):
    return {'my_cookie': custom_cookie}
```
Response body:
```json
{
  "my_cookie": "cookie_value"
}
```

NOTE: the query parameter (`custom_cookie`) must match the key value of the custom cookie, which is set in
`reponse.set_cookie(key=...)`

### Form Data
Forms are HTML data that is collected from the users input. `<form>...</form>` </br>
We need to handle this data differently because its in a special encoding format (not JSON) </br>
**Form POST**:
```python
# product.py
from fastapi import Form

@router.post('/new')
def create_product(name: str = Form(...)):
    products.append(name)
    return products
```
the Curl `Content-type` will change:
```
curl -X 'POST' \
  'http://127.0.0.1:8000/product/new' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d 'name=test'
```
Response Body:
```
[
  "watch",
  "camera",
  "phone",
  "test"
]
```
### CORS - Cross Origin Resource Sharing
Used when we're creating an API and an application on your local machine, where the api access the application. </br>
E.g:
- running a react frontend on localhost:8080
- We then try to access the frontend with fastapi at endpoint localhost:8000
- This will result in: **CORS ERROR**

Essentially the endpoints don't match up </br>
**FIX**:
We need to add a CORS middleware to the `main.py` file:
```python
# main.py
from fastapi.middleware.cors import CORSMiddleware

...

origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)
```
inside origins we specify the endpoint of our local react (or another frontend framework) app. 
- `allow_credentials` allows cross-origin cookies.
- `allow_methods` allows all methods e.g. GET, POST.
- `allow_headers` allows all headers

## <ins>Authentication</ins>

The aim of this section is to allow for users to login from the front end, providing username and password, they will
then have access to all the endpoints and resources their permissions will allow. They will only have to login once
per session (or remain logged in for specific time period before being asked to re-enter credentials).

This works but the front end holding a payload containing an JWT encoded oAuth2 access token which is linked to the
username and has an associated expiration data (for other example this could be linked to other bits of unique string
data).

### JWT Side Note:
https://jwt.io/

JWT stands for Json Web Token and takes the following three encodings:
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```
The first encoding gives us information about the type and algorithm used to encode it
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```
The second is the payload:
```json
{
  "sub": "1234567890",
  "name": "John Doe",
  "iat": 1516239022
}
```
The verification signature (handled by oAuth2 in our case)
```json
HMACSHA256(
  base64UrlEncode(header) + "." +
  base64UrlEncode(payload),
  OAUTH_SECRET_KEY
)
```

### Back to Authentication!

Once logged in the user can access resources without having to constantly authenticate. The API does this by sending
the authentication payload with each of these requests. The JWT payload can then be verified in the backend by decoding 
it and matching the usernames. Once authenticated the request operation can continue as normal, e.g. get blog post,
create new post, delete old post, etc. Its important to note that each request will require this payload username 
verification before performing its function.

**The general process can be shown below**

![My Image](/rm_images/oAuth2_and_JWT.jpg)
The above maps out exactly what is done here: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/

### What does this look like in code:

Starting from the client website login, the user will enter their password and username:

```python
# oauth2.py
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

load_dotenv()
SECRET_KEY = os.getenv("OAUTH_SECRET_KEY")
ALGORITHM = os.getenv("OAUTH_ALGO")
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt, expire


# authentication.py
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

@router.post('/token')
def get_token(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(models.DbUser).filter(models.DbUser.username == request.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='invalid credentials')
    if not Hash.verify(user.password, request.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='incorrect password')

    access_token, expire = outh2.create_access_token(data={"sub": user.username})

    return {'access_token': access_token,
            'token_expires': expire,
            'token_type': 'bearer',
            'user_id': user.id,
            'user_name': user.username}
```
The username and password is handled by `OAuthPasswordRequestForm`, and a db session is created. We then check to see
if the user exists in the database, returning exceptions if not, we check that the hashed password matches the hashed
password found in the db. `create_access_token` is then used to create the JWT encoded payload and the expiry date, 
finally we turn this as well as other meta data as the payload to the authentication process.

**Now that the user has logged in, lets make sure that they can access different endpoints through this login:**

To allow this process to work we'll use the token payload available to the frontend. As we can see from the above code
the token is liked with the username, so we need to verify the authenticated token username with our db before completing
any operations. To do this the `get_current_user` function is used.

```python
# oauth2.py
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Couldn't validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db_user.get_user_by_username(db, username)

    if user is None:
        raise credentials_exception

    return user
```

In our CRUD operations we can now add the `current_user: UserBase = Depends(get_current_user)` dependency to enforce 
this authentication. E.g. getting articles by id now required authentication:

```python
# article.py
@router.get("/{id}", response_model=ArticleUserDisplay)
def get_article(id: int,
                db: Session = Depends(get_db),
                current_user: UserBase = Depends(get_current_user)):
    return {
        'data': db_article.get_article(db, id),
        'current_user': current_user
    }
```

with any of these responses we can now see the JWT token in the curl authentication command:
```curl
curl -X 'GET' \
  'http://127.0.0.1:8000/articles/1' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhdXRodGVzdCIsImV4cCI6MTY3NjEzNDYwNn0.rrAX-GQGvbdFMJcEOgGa4rJFGITRLbJN1tVCpQ0xX9o'
```
The payload part of the JWT is:
```json
{
  "sub": "authtest",
  "exp": 1676134606
}
```

## <ins>Work with Files</ins>

Its possible to create an endpoint that takes in a file and gives back a response.

```python
# file.py
from fastapi import APIRouter, File

@router.post('/lines')
def get_file(file: bytes = File(...)):
    content = file.decode('utf-8')
    lines = content.split('\n')
    lines = [line.replace('\r', '') for line in lines]
    return {'lines': lines}
```

From the docs we can now select a text file to be passed to our server, we can then process the info
however we want and return info.

The issue with this method is that the files are stored in memory!

To fix this issue we cant use `UploadFile` which stores a certain size in memory and then the rest on disk. this 
works well for video data.

```python
# file.py
@router.post('/uploadfile')
def get_upload_file(upload_file: UploadFile = File(...)):
    path = f"files/{upload_file.filename}"
    # w+b is wright or create
    with open(path, 'w+b') as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    return {
        'filename': path,
        'type': upload_file.content_type
    }
```

Above the frontend will upload a file e.g. a dog picture, and we'll save it locally into the files
directory. The response body will be the path the image was save on the server and the 
type of file.

The issue is that if the file has the same name it will be overwritten!

### Make files statically available online:

First install `pip install aiofiles`

Then in we can add the following code in `main.py`:

```python
from fastapi.staticfiles import StaticFiles

app.mount('/files', StaticFiles(directory='files'), name='files')
```

If we then go to our docs URL `http://127.0.0.1:8000/files/dogo.jpg` we can see the picture we previously
uploaded.

This is very useful when making a static websites!

### Downloading Files:

We've just seen how we cant access files through the endpoint statically, but what if our user wants to download files?

Why do we want to do this? 
- allows for more logic around file access.
- provide security, e.g. only authenticated users to access certain files.

To do this we use the `FileResponse` response body type:

```python
# file.py
from fastapi.responses import FileResponse

@router.get('/download', response_class=FileResponse)
def download_files(name: str):
    path = f'files/{name}'
    return path
```

In the docs we can now see the returned image which can be used dynamically in our frontend.

![My Image](/rm_images/dogo.PNG)

## <ins>Deployment on Deta</ins>

To do this we need to create an account and install Deta locally.

to install deta on a machine use (for windows):

`iwr https://get.deta.dev/cli.ps1 -useb | iex`

Once installed login via the terminal using: `space login`.

Create an access token and save it somewhere safe. Use this to login.

The in the directory of the API project type: `space push` then `space release`

my code is live here!: `https://learningfastapi-3-p9223010.deta.app/docs`

## <ins>Testing</ins>

As I have learnt from Powervault testing is SUPER important to stop code degrading and allowing for maintainable code.
Strive for 100% coverage, but often this is very difficult and probably only possible at big companies.

This can be done easily using the requests and unittest libraries (or pytest). See the code for more details, its pretty
simple.

## <ins>Async Await</ins>

This allows for processes that have async await to run concurrently and allow for other less intensive processes
to be run at the same time. If we didnt use this then the server would get 'blocked' by these large tasks.

The `await` part means that the process can be paused, `async` defines a function with suspendable points.

Imagine that we have a backend process that takes a long time. We can use `async` and `await` to keep the backend
running with other request while still processing the long one.

```python
# product.py

async def time_consuming_functionality():
    time.sleep(5)


@router.get('/all')
async def get_all_products():
    await time_consuming_functionality()
    log('myapi', 'call to get all products')
    data = ' '.join(products)
    return Response(content=data, media_type='text/plain')
```

We can split out the functionality that takes time and assign `async` to the function. Then inside the main function 
`get_all_products` we can use the `await` special term to tell the function to not return the response until it has 
finished.

## <ins>Templates</ins>

This is when we return a html/css object as our response. e.g. facebook market place people upload productions
they want to sell, this is then hosted on the website in a format. This can be done through templates. This html 
returned is integrated into the page and served to the user.

The templating engine will be `jinja2`. To do this we need to create a template on our server, we create a endpoint
, the user will pass us information which will populate the template and will be served back to them.

**Building a new product template response with css:**

- create a new directory with a python module for the POST operation
- a html template where our data will be inserted from the POST.
- a static directory containing a styles css file that will format the html.

```python
# templates.py

from fastapi.routing import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from schemas import ProductBase

router = APIRouter(
    prefix='/templates',
    tags=['templates']
)

templates = Jinja2Templates(directory='templates')

@router.post('/products/{id}', response_class=HTMLResponse)
def create_new_product(id: str, request: Request, product: ProductBase):
    return templates.TemplateResponse(
        'product.html',
        {
            'request': request,
            'id': id,
            'title': product.title,
            'description': product.description,
            'price': product.price
        }
    )
```

Here we'll use Jinja2 as our reponse model. The user will provide an id as a path parameter, and then a product title,
 description, and price as the request body. This request body is determined by the pydantic base model `ProductBase`.
The `templates.TemplateResponse` points to our html temple which intern points to the css file.

To keep our website static we need to make the css files statically available to page. This is done in `main.py`:

```python
# main.py

app.mount('/templates/static',
          StaticFiles(directory='templates/static'),
          name='static')
```

The response from the POST request will be the html template where the header will reference the static css file:

```html
<head>
    <link href="http://127.0.0.1:8000/templates/static/styles.css" rel="stylesheet"/>
</head>
<body>
    <div class="tpl_product">
        <div class="tpl_title">Mac Mini Pro</div>
        <div class="tpl_description">an incredible mac for almost half price!</div>
        <div class="tpl_price">1349.99</div>
    </div>
</body>
```

putting this into a html editor we can see the style!:

![My Image](/rm_images/templates.PNG)

## <ins>Logs as background tasks</ins>

background tasks are run after returning a response. This is useful when we want to do something after a request but the
client doesn't have to be waiting around for the operation to complete e.g. logging, email notifications, processing data.

```python
# templates
from fastapi import BackgroundTasks
from logs.logging import log

@router.post('/products/{id}', response_class=HTMLResponse)
def create_new_product(id: str,
                       request: Request,
                       product: ProductBase,
                       bt: BackgroundTasks):
    bt.add_task(log_template_call, "creating a new product template")

def log_template_call(message: str):
    log("MyAPI", message)
```

Simply add an argument to the CRUD method with type `BackgroundTasks` and then use the method `add_task` this expects a 
function as the first argument and the arguments of the function as the remaining arguments. Because `add_task` is
expecting a function we need to create one just to house our log function.

## <ins>WebSockets</ins>

Websockets are a protocal that allow for two-way communication over TCP ip. We can send and receive messages dynamically
and will stay open as long as we require them.

Websockets would normally be used with a modern framework like React, but for this example im going to use simple html 
and javascript, see the full code in `client.py` (the javascript part can be seen below):

```html
...
        <script>
            var ws = new WebSocket("ws://localhost:8000/endpoint");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
...
```
Note how the websocket endpoint has been defined, `'/endpoint'` is arbitrary.

The following python code is used to allow for the messaging script to use fastapi:

```python
# main.py
from client import html
from fastapi.websockets import WebSocket
from fastapi.responses import HTMLResponse

@app.get("/")
async def get():
    return HTMLResponse(html)


@app.websocket("/endpoint")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Message: {data}")
```

We can now open up multiple tabs and write messages that will populate all the pages at once! The message below was only
typed in one browser but appears in both.

![My Image](/rm_images/websockets.PNG)

## <ins>Dependencies</ins>

"Dependency Injection" means, in programming, that there is a way for your code (in this case, your path operation functions) to declare things that it requires to work and use: "dependencies".

And then, that system (in this case FastAPI) will take care of doing whatever is needed to provide your code with those needed dependencies ("inject" the dependencies).

This is very useful when you need to:

- Have shared logic (the same code logic again and again).
- Share database connections.
- Enforce security, authentication, role requirements, etc.
- And many other things...

For details on dependencies look at `router/dependencies.py`

### Class Dependencies:

We can use dependencies for classes, the arguments before the `Depends` will be passed into the class:

```python
# dependencies.py

class Account:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email

# account: Account = Depeneds() is the same as account: Account = Depends(Account)
@router.post('/user')
def create_new_user(name: str, email: str, password: str, account: Account = Depends()):
    return {
        'name': account.name,
        'email': account.email
    }

```

Response body:

```json
{
  "name": "kek",
  "email": "kek@kekw.com"
}
```

### Multi level dependencies:

This is relatively simple, inside the `Depends` function we can use another `Depends`:

```python
# dependencies.py

def convert_params(request: Request, separator: str):
    query = []
    for key, value in request.query_params.items():
        query.append(f"{key} {separator} {value}")
    return query

def convert_headers(request: Request, spacing: str, query=Depends(convert_params)):
    out_header = []
    for key, value in request.headers.items():
        out_header.append(f"{key} {spacing} {value}")
    return {
        'headers': out_header,
        'query': query
    }


@router.get('')
def get_item_show_header(spacing: str = '**', headers=Depends(convert_headers)):
    return {
        'item': 'hat',
        'headers': headers
    }
```

We then have parameters `spacing` and `separator` in the documentation.

response:

```json
{
  "item": "hat",
  "headers": {
    "headers": [
      "host spacing 127.0.0.1:8000",
      "connection spacing keep-alive",
      "sec-ch-ua spacing \"Chromium\";v=\"110\", \"Not A(Brand\";v=\"24\", \"Google Chrome\";v=\"110\"",
      "accept spacing application/json",
      "sec-ch-ua-mobile spacing ?0",
      "user-agent spacing Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
      "sec-ch-ua-platform spacing \"Windows\"",
      "sec-fetch-site spacing same-origin",
      "sec-fetch-mode spacing cors",
      "sec-fetch-dest spacing empty",
      "referer spacing http://127.0.0.1:8000/docs",
      "accept-encoding spacing gzip, deflate, br",
      "accept-language spacing en-GB,en-US;q=0.9,en;q=0.8"
    ],
    "query": [
      "spacing separator spacing",
      "separator separator separator"
    ]
  }
}
```

### Global dependencies:

We can add globally dependencies to different endpoints without having to individual add them into the functions. These
apply to ALL endpoints, we can apply this to either the router or app.

A good example of when we might want to do this is with a logger:

```python
# dependencies.py

router = APIRouter(
    prefix='/dependencies',
    tags=['dependencies'],
    dependencies=[Depends(log)]
)

# logging.py

from fastapi.requests import Request

def log(tag='MyApp', message='no message', request: Request = None):
    with open('logs/log.txt', 'a+') as log:
        log.write(f'{tag}: {message}\n')
        log.write(f'\t{request.url}\n')
```

Now all the endpoints in 'dependencies' will depend on the logger! 

example: Using `get_item_show_header`:

```txt
# log.txt

MyApp: no message
	http://127.0.0.1:8000/dependencies?spacing=%20&tag=MyApp&message=no%20message&separator=--
```

To do this for all endpoints add it into the app arguments:

```python
# main.py

app = FastAPI(dependencies=[Depends(log)])
```