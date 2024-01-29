
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter
import re

# Download NLTK resources (you only need to do this once)
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')



def preprocess_content(content):
    # Remove invalid characters
    valid_characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,!?'"
    content_cleaned = ''.join(char for char in content if char in valid_characters)
    content_cleaned = re.sub(r'\.', '', content_cleaned)
    content_cleaned = re.sub(r'[^a-zA-Z\s]', '', content_cleaned)
    return content_cleaned

def classify_article(content):
    try:
        # Preprocess content to remove invalid characters
        content_cleaned = preprocess_content(content)
        
        # Tokenize the cleaned text
        tokens = word_tokenize(content_cleaned.lower())

        # Remove stopwords
        stopwords_en = set(stopwords.words('english'))
        tokens = [token for token in tokens if token not in stopwords_en]

        # Lemmatize the tokens
        lemmatizer = WordNetLemmatizer()
        lemmatized_tokens = [lemmatizer.lemmatize(token) for token in tokens]

        # Extract features (for simplicity, we'll use word counts)
        features = Counter(lemmatized_tokens)

        # Define category classifiers based on keywords or other criteria
        terrorism_keywords = {'terrorism', 'protest', 'political', 'unrest', 'riot'}
        positive_keywords = {'positive', 'uplifting'}
        natural_disaster_keywords = {'natural', 'disaster', 'earthquake', 'hurricane', 'flood', 'wildfire'}

        # Classify into categories based on keywords
        category = 'Others'
        if any(keyword in features for keyword in terrorism_keywords):
            category = 'Terrorism / Protest / Political Unrest / Riot'
        elif any(keyword in features for keyword in positive_keywords):
            category = 'Positive/Uplifting'
        elif any(keyword in features for keyword in natural_disaster_keywords):
            category = 'Natural Disasters'

        return category
    except Exception as e:
        # Handle other exceptions and return an error message
        return f'Error: {str(e)}'
