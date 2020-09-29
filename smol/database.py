from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DB_URL = "sqlite:///./jobs.db"
SQLALCHEMY_DB_URL_TEST = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DB_URL, connect_args={"check_same_thread": False})
engine_test = create_engine(SQLALCHEMY_DB_URL_TEST, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)
SessionLocalTest = sessionmaker(autocommit=False, autoflush=True, bind=engine_test)

Base = declarative_base()
