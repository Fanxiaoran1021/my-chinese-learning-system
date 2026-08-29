from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

SQLALCHEMY_DATABASE_URL = "sqlite:///./chinese_learn.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    password = Column(String(100))
    create_time = Column(DateTime, default=datetime.utcnow)

class Vocabulary(Base):
    __tablename__ = "vocabularies"
    id = Column(Integer, primary_key=True, index=True)
    word = Column(String(100))
    pinyin = Column(String(100))
    meaning = Column(Text)
    example = Column(Text)

class LearnRecord(Base):
    __tablename__ = "learn_records"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    vocab_id = Column(Integer)
    study_time = Column(DateTime, default=datetime.utcnow)
    status = Column(String(20))

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()