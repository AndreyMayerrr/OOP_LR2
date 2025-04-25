# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

load_dotenv()  # загружаем переменные окружения из .env

# Строим строку подключения к базе данных
DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASS')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

# Создаем двигатель базы данных
engine = create_engine(DATABASE_URL)

# Создаем фабрику сеансов
SessionLocal = sessionmaker(bind=engine)

# Основу декларативных классов SQLAlchemy
Base = declarative_base()

# Функцию для получения сессии базы данных
def get_db():
    """
    Генерирует новую сессию базы данных и освобождает её после использования.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()