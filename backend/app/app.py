import os
import shutil
import logging
import tempfile

from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.parser_pdf import pdf_parser
from backend.app.authentication.auth import register, get_user, cookie_check, cookies, auth, logout, verification, verification_request
from backend.app.authentication.token import decodeJWT
from backend.models import schemas
from backend.models.database import get_session
from ML.main import ResumeAnalyzer
from config import GIGACHAT_API

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
GIGACHAT_API_KEY = GIGACHAT_API

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # адрес фронта
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

analyzer = ResumeAnalyzer(gigachat_api_key=GIGACHAT_API)


# Эндпоинт для загрузки одного файла
@app.post("/upload_file/")
async def upload_file(uploaded_file: UploadFile):
    filename = f"1_{uploaded_file.filename}"
    try:
        with open(filename, "wb") as f:
            f.write(await uploaded_file.read())
        parsed_text = pdf_parser(filename)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ошибка при обработке файла: {str(e)}")
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
        await verification_request(user_data.email)
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
    code: str = Form(...),
    user_data: dict = Depends(get_user_info),
    db: AsyncSession = Depends(get_session)
):
    user_email = user_data["email"]
    return await verification(user_email, db, code)

# Эндпоинт для загрузки одного файла
@app.post("/analyze-resume/")
async def analyze_resume(file: UploadFile = File(...), query: str = Form(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Пожалуйста, загрузите PDF файл")

    temp_path = None
    try:
        # Создаем временный файл
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            temp_path = tmp.name
            # Копируем содержимое файла
            await file.seek(0)
            shutil.copyfileobj(file.file, tmp)

        await file.close()  # Закрываем UploadFile

        # Теперь анализируем файл
        resume_text = analyzer.extract_text_from_pdf(temp_path)
        result = analyzer.analyze_resume(resume_text, query)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при обработке файла: {str(e)}")

    finally:
        # Удаляем временный файл
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except PermissionError:
                import time
                time.sleep(0.1)  # Небольшая пауза и повторная попытка
                try:
                    os.remove(temp_path)
                except Exception as e:
                    # Логируем ошибку, но не падаем
                    logger.error(f"Не удалось удалить временный файл {temp_path}: {e}")

    return JSONResponse(content={"result": result})
