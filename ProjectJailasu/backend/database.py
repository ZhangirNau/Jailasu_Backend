# ProjectJailasu/backend/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# URL базы данных (SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///./jailasu.db"

# Подключение к базе
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Сессия для работы с БД
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()


# Зависимость для получения сессии (используется в роутерах)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
