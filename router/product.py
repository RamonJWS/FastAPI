import time

from fastapi import APIRouter, Header, Cookie, Form
from fastapi.responses import Response, HTMLResponse, PlainTextResponse
from typing import Optional, List, Union

from logs.logging import log

router = APIRouter(
    prefix="/product",
    tags=["product"]
)


# dummy data
products = ['watch', 'camera', 'phone']


async def time_consuming_functionality():
    time.sleep(5)


@router.get('/all')
async def get_all_products():
    await time_consuming_functionality()
    log('myapi', 'call to get all products')
    data = ' '.join(products)
    return Response(content=data, media_type='text/plain')


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

@router.get('/withheader/')
def get_products(custom_header: Optional[List[str]] = Header(default=None)):
    return products


@router.get('/withheader121/')
def get_products(response: Response,
                 custom_header: Optional[List[str]] = Header(default=None)):
    response.headers['response_custom_header'] = ', '.join(custom_header)
    return products

@router.get('/createcookie/')
def create_cookie(response: Response):
    response.set_cookie(key='custom_cookie', value='cookie_value')
    return products

@router.get('/getcookie/')
def get_cookie(custom_cookie: Union[str, None] = Cookie(None)):
    return {'my_cookie': custom_cookie}

@router.post('/new')
def create_product(name: str = Form(...)):
    products.append(name)
    return products
