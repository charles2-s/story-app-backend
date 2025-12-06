from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Create a SQLite database file named app.db
DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


# SessionLocal creates a new DB session for each request
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base is the class all our models will inherit from
Base = declarative_base()