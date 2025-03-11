import uvicorn
from models.database import Base, engine


def start():
    # Создание таблиц в БД (если их нет)
    Base.metadata.create_all(bind=engine)
    uvicorn.run("app.app:app", host="localhost", port=80, reload=True)


if __name__ == "__main__":
    start()
