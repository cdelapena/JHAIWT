import numpy as np
import pandas as pd
import re
import nltk  # Natural Language Toolkit
import spacy  # NLP library in Python
import string
from nltk.corpus import stopwords

# Download stopwords if not already downloaded. For stopwords, reference
# Reference: https://www.kaggle.com/code/sudalairajkumar/getting-started-with-text-preprocessing
nltk.download('stopwords')

# Download spaCy model if not already downloaded
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    from spacy.cli import download
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

PUNCT_TO_REMOVE = string.punctuation
STOPWORDS = set(stopwords.words('english'))

def remove_punctuation(text: str) -> str:
    return text.translate(str.maketrans('', '', PUNCT_TO_REMOVE))

def remove_stopwords(text: str) -> str:
    return ' '.join([word for word in text.split() if word.lower() not in STOPWORDS])

def preprocess_text(data) -> list:
    # Check if the input is a list and convert it to a DataFrame
    if isinstance(data, list):
        df = pd.DataFrame(data)
    else:
        df = data

    df['description_lower'] = df['description'].str.lower()
    df['description_wo_punct'] = df['description_lower'].apply(remove_punctuation)
    df['description_clean'] = df['description_wo_punct'].apply(remove_stopwords)
    
    # Dropping intermediate columns
    df.drop(['description_lower', 'description_wo_punct'], axis=1, inplace=True)
    
    # Renaming the final cleaned column to 'description'
    df.rename(columns={'description_clean': 'description'}, inplace=True)

    # Replace NaN values with None
    df = df.where(pd.notnull(df), None)
    
    return df.to_dict(orient='records')