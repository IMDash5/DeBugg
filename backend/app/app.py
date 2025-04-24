from fastapi import FastAPI, Depends, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.parser_pdf import pdf_parser

from backend.app.authentication.auth import register, get_user, cookie_check, cookies, auth, logout, verification, verification_request
from backend.app.authentication.token import decodeJWT
from backend.models import schemas
from backend.models.database import get_session


app = FastAPI()

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

# Эндпоинт для регистрации пользователя
@app.post("/account/register", status_code=201)
async def register_user(
    user_data: schemas.UserCreate,
    db: AsyncSession = Depends(get_session),
    check=Depends(cookie_check),
):
    if check:
        data = await register(db=db, user_data=user_data)
        return cookies(data)

# Эндпоинт для получения информации о пользователе через JWT-токен
@app.get("/get_user_info_by_token")
async def get_user_info(token=Depends(get_user)):
    try:
        return decodeJWT(token)
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Эндпоинт для логина пользователя
@app.post("/account/login")
async def login_user(
    user_data: schemas.UserLogin,
    db: AsyncSession = Depends(get_session),
    check=Depends(cookie_check),
):
    if check:
        return await auth(db, user_data)

# Эндпоинт для разлогинивания пользователя
@app.get("/account/logout")
async def logout_user(result=Depends(logout)):
    return result

@app.post("/account/register/verify-request")
async def verify_request(user_data: dict = Depends(get_user_info)):
    user_email = user_data["email"]
    await verification_request(user_email)
    return {"status": "verification_code_sent"}

@app.post("/account/register/verify")
async def verify_user(
    code: str,
    user_data: dict = Depends(get_user_info),
    db: AsyncSession = Depends(get_session)
):
    user_email = user_data["email"]
    return await verification(user_email, db, code)