from typing import Union
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from models.database import SessionLocal
from models.crud import create_user, get_user

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
