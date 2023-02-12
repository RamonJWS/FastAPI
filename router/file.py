import shutil

from fastapi import APIRouter, File, UploadFile
from fastapi.responses import FileResponse

router = APIRouter(
    prefix='/file',
    tags=['file']
)

@router.post('/lines')
def get_file(file: bytes = File(...)):
    content = file.decode('utf-8')
    lines = content.split('\n')
    lines = [line.replace('\r', '') for line in lines]
    return {'lines': lines}

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

@router.get('/download', response_class=FileResponse)
def download_files(name: str):
    path = f'files/{name}'
    return path
