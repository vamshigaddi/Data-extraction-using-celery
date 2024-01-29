from celery import Celery
from celery.utils.log import get_task_logger
from dateutil import parser as date_parser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import NewsArticle  # Import the NewsArticle model
from classify import classify_article

# Celery configuration for Redis
broker_url = 'amqp://guest:guest@localhost:5672'
result_backend = 'rpc://'

# Define a Celery application
celery = Celery('news_parser')
celery.config_from_object({'broker_url': broker_url, 'result_backend': result_backend})

# Set up SQLAlchemy engine and session
DATABASE_URL = "mysql+mysqlconnector://root:root@localhost:3306/news_database"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Logger for the Celery task
logger = get_task_logger(__name__)

# Celery task to process news articles
@celery.task
def process_news_article(title, content, publication_date, source_url):
    try:
        # Classify the article into a category (you can implement this based on your requirements)
        category = classify_article(content)
        
        # Save the article to the database with the assigned category
        db = SessionLocal()
        article = NewsArticle(title=title, content=content, publication_date=publication_date, source_url=source_url, category=category)
        db.add(article)
        db.commit()
        db.close()
        
        # Log the successful processing of the article
        logger.info(f"Processed article: {title}, Category: {category}")
    except Exception as e:
        # Log any errors that occur during processing
        logger.error(f"Error processing article {title}: {str(e)}")
