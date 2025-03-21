from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """Схема данных которые вводит пользователь при регистрации"""

    email: EmailStr
    password: str
    username: str


class UserLogin(BaseModel):
    """Схема данных которые вводит пользователь при логине"""

    email: EmailStr
    password: str