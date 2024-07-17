import numpy as np
import pandas as pd
import re
import nltk				# Natural Language Toolkit
import spacy			# NLP library in Python
import string
from nltk.corpus import stopwords

# Download stopwords if not already downloaded. For stopwords, reference
# Reference https://www.kaggle.com/code/sudalairajkumar/getting-started-with-text-preprocessing
nltk.download('stopwords')

PUNCT_TO_REMOVE = string.punctuation
STOPWORDS = set(stopwords.words('english'))

def remove_punctuation(text: str) -> str:
    return text.translate(str.maketrans('', '', PUNCT_TO_REMOVE))

def remove_stopwords(text: str) -> str:
    return ' '.join([word for word in text.split() if word.lower() not in STOPWORDS])

def preprocess_text(df: pd.DataFrame) -> pd.DataFrame:
    df['description_lower'] = df['description'].str.lower()
    df['description_wo_punct'] = df['description_lower'].apply(remove_punctuation)
    df['description_clean'] = df['description_wo_punct'].apply(remove_stopwords)
    
    # Dropping intermediate columns
    df.drop(['description_lower', 'description_wo_punct'], axis=1, inplace=True)
    
    # Renaming the final cleaned column to 'description'
    df.rename(columns={'description_clean': 'description'}, inplace=True)
    
    return df