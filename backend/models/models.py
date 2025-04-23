import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Boolean, Column, String

from backend.models.database import Base


class User(Base):
    """Модель БД с данными пользователей"""

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_verified = Column(Boolean, default=False)