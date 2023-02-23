from fastapi import APIRouter, Depends
from fastapi.requests import Request
from logs.logging import log

router = APIRouter(
    prefix='/dependencies',
    tags=['dependencies'],
    dependencies=[Depends(log)]
)


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


@router.post('/new')
def create_item_show_headers(headers=Depends(convert_headers)):
    return {
        'result': 'new item',
        'headers': headers
    }


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
