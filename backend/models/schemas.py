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

class UserName(BaseModel):
    """Схема данных имени и фамилии пользователя"""

    name: str
    surname: str