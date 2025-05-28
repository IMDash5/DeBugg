import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Boolean, Column, String, Integer, JSON, TIMESTAMP, VARCHAR, ForeignKey
from sqlalchemy.orm import relationship

from backend.models.database import Base


class User(Base):
    """Модель БД с данными пользователей"""

    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_verified = Column(Boolean, default=False)

    resumes = relationship("Resume", back_populates="user")

class Resume(Base):
    """Модель резюме пользователя"""

    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), unique=True)
    skills = Column(JSON)
    experience = Column(JSON)
    education = Column(JSON)
    filename = Column(VARCHAR)
    file_path = Column(VARCHAR)

    user = relationship("User", back_populates="resumes")