import feedparser
from dateutil import parser as date_parser
from celery import Celery
from celery_worker import process_news_article
import logging

# Configure logging
logging.basicConfig(filename='news_parser.log', level=logging.INFO)



# Celery configuration
broker_url = 'amqp://guest:guest@localhost:5672'
result_backend = 'rpc://'
# Define a Celery application
celery = Celery('news_parser')
celery.config_from_object({'broker_url': broker_url, 'result_backend': result_backend})

# List of RSS feeds
rss_feeds = [
    "http://rss.cnn.com/rss/cnn_topstories.rss",
    "http://qz.com/feed",
    "http://feeds.foxnews.com/foxnews/politics",
    "http://feeds.reuters.com/reuters/businessNews",
    "http://feeds.feedburner.com/NewshourWorld",
    "https://feeds.bbci.co.uk/news/world/asia/india/rss.xml",
]

# Function to parse and extract data from an RSS feed
def parse_rss_feed(feed_url):
    try:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries:
            # Extract relevant information from each news article
            title = entry.title
            content = entry.get("summary", entry.get("description", ""))
            publication_date_str = entry.get("pubDate", "")
            source_url = entry.link

            # Try to convert the publication date string to a datetime object
            try:
                publication_date = date_parser.parse(publication_date_str)
            except ValueError as e:
                # Log parsing errors
                logging.error(f"Error parsing publication date for article: {title}. Error: {str(e)}")
                publication_date = None  # Handle the case where the date string is not in the expected format

            # Send the article to the Celery task for further processing
            process_news_article.delay(title, content, publication_date, source_url)
    except Exception as e:
        # Log general errors
        logging.error(f"Error parsing RSS feed: {feed_url}. Error: {str(e)}")

# Parse and extract data from each RSS feed
for feed_url in rss_feeds:
    parse_rss_feed(feed_url)
