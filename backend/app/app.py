from typing import Union
from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, status
from sqlalchemy.orm import Session
from models.database import SessionLocal
from models.crud import create_user, get_user
from models.parser_pdf import pdf_parser


app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

# Эндпоинт для загрузки одного файла
@app.post("/upload_file/")
async def upload_file(uploaded_file: UploadFile):
    filename = f"1_{uploaded_file.filename}"
    with open(filename, "wb") as f:
        f.write(await uploaded_file.read())
    
    parsed_text = pdf_parser(filename)
    return {"parsed_text": parsed_text}

# Эндпоинт для загрузки нескольких файлов
@app.post("/multiple_upload_files/")
async def upload_files(uploaded_files: list[UploadFile]):
    results = []
    for uploaded_file in uploaded_files:
        filename = f"1_{uploaded_file.filename}"
        with open(filename, "wb") as f:
            f.write(await uploaded_file.read())
        
        parsed_text = pdf_parser(filename)
        results.append({
            "filename": filename,
            "parsed_text": parsed_text
        })
    return {"files": results}
