import feedparser
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from sqlalchemy import VARCHAR
import mysql.connector

# MySQL database configuration
DATABASE_URL = "mysql+mysqlconnector://root:root@localhost:3306/news_database"
# Define SQLAlchemy model for news articles
Base = declarative_base()


class NewsArticle(Base):
    __tablename__ = "news_articles"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(VARCHAR(255), index=True)  # Specify the length here
    content = Column(VARCHAR(10000))
    publication_date = Column(DateTime, default=datetime.utcnow)
    source_url = Column(VARCHAR(255), unique=True)
    is_duplicate = Column(Boolean, default=False)
    category=Column(VARCHAR(255))


# Create database tables
engine = create_engine(DATABASE_URL,echo=True)
Base.metadata.create_all(bind=engine)

# Create a session to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

