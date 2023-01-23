from fastapi import APIRouter
from fastapi.responses import Response, HTMLResponse, PlainTextResponse
from schemas import ArticleBase, ArticleDisplay
from sqlalchemy.orm.session import Session
from db import db_article
from db.database import get_db

router = APIRouter(
    prefix="/product",
    tags=["product"]
)


# dummy data
products = ['watch', 'camera', 'phone']

@router.get('/all')
def get_all_products():
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
