from typing import Union
from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, status
from sqlalchemy.orm import Session
from models.database import SessionLocal
from models.crud import create_user, get_user
from models.parser_pdf import pdf_parser


app = FastAPI()


# Зависимость для получения сессии БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}


# Эндпоинт для создания пользователя
@app.post("/users/")
def create_new_user(username: str, password: str, db: Session = Depends(get_db)):
    return create_user(db=db, username=username, password=password)


# Эндпоинт для получения пользователя
@app.get("/users/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


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
