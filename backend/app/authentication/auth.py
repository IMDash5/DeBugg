from fastapi import HTTPException, Request, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST
import time

from backend.app.authentication.security import pwd_context
from backend.app.authentication.token import signJWT
from backend.models.models import User
from backend.models.schemas import UserCreate, UserLogin, UserName

from backend.app.mailer.mail import send_email, verification_codes, confirmation_code

def cookies(user_data):
    """Создание куки"""
    token = signJWT(user_data)
    response = JSONResponse(content=user_data)
    response.set_cookie(key="auth_token", value=token, expires=2592000)
    return response

async def register(db: AsyncSession, user_data: UserCreate):
    """Регистрация пользователя и добавление его данных в БД"""
    if await db.scalar(select(User).where(User.email == user_data.email)):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="User with this email already exists!",
        )
    elif await db.scalar(select(User).where(User.username == user_data.username)):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="User with this username already exists!",
        )
    user = User(email=user_data.email)
    user.hashed_password = pwd_context.hash(user_data.password)
    user.username = user_data.username
    db.add(user)
    await db.commit()
    return {
        "id": str(user.id),
        "username": user.username,
        "email": user.email,
        "hashed_password": user.hashed_password,
        "is_verified": False,
        "name": user.name,
        "surname": user.surname
    }

def get_user(request: Request):
    """Получение куки"""
    return request.cookies.get("auth_token")

def cookie_check(request: Request):
    """Проверка наличия куки"""
    cookie = request.cookies.get("auth_token")
    if cookie is not None:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="User is already logged in")
    else:
        return True

async def auth(db: AsyncSession, user_data: UserLogin):
    """Вход в аккаунт пользователя"""
    user = await db.scalar(select(User).where(User.email == user_data.email))
    if user is None or pwd_context.verify(user_data.password, user.hashed_password) is False:
        raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail="Incorrect email or password")
    else:
        info = {
            "id": str(user.id),
            "username": user.username,
            "email": user.email,
            "hashed_password": user.hashed_password,
            "is_verified": user.is_verified,
            "name": user.name,
            "surname": user.surname 
        }
        return cookies(info)

def logout(response: Response):
    """Разлогинивание пользователя"""
    response.delete_cookie(key="auth_token")
    return {"status": "logged out"}

async def verification_request(user_email):
    code = confirmation_code()
    await send_email(receiver=user_email, code=code)


async def verification(user_email, db: AsyncSession, code: str):
    user = await db.scalar(select(User).where(User.email == user_email))
    record = verification_codes.get(user_email)
    
    if not record or time.time() > record["expires_at"]:
        return {"status": "expired or not found"}

    if record["code"] == code:
        user.is_verified = True
        await db.commit()
        del verification_codes[user_email]
        return {"status": "success"}
    else:
        return {"status": "invalid code"}

async def name(user_email, db: AsyncSession, user_data: UserName):
    """Имя и фамилия пользователя"""
    user = await db.scalar(select(User).where(User.email == user_email))
    user.name = user_data.name
    user.surname = user_data.surname
    db.add(user)
    await db.commit()