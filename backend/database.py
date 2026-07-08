from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv
import os
import time

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

Base = declarative_base()

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(100))
    ip = Column(String(50))
    severity = Column(String(20))
    message = Column(String(255))

def create_engine_with_retry(retries=10, delay=5):
    for attempt in range(retries):
        try:
            engine = create_engine(DATABASE_URL, echo=True)
            Base.metadata.create_all(bind=engine)
            print("✅ Database connected successfully")
            return engine
        except Exception as e:
            print(f"⏳ Database not ready, retrying in {delay}s... (attempt {attempt + 1}/{retries})")
            time.sleep(delay)
    raise Exception("❌ Could not connect to database after multiple attempts")

engine = create_engine_with_retry()
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)