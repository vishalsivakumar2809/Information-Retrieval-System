'''

This file contains the preprocessing that must be used
for this assignment. 

'''

import nltk

from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download('wordnet')

stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

import string

def tokenize(text):
    '''
    Tokenizes text in a document or query. 
    Removes punctuation and returns a list of tokens.
    '''
    assert type(text) == str

    # remove punctuation
    new_text = text.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(new_text)

    return tokens

def normalize(tokens, method = 'stemming'):
    '''
    Normalize a list of tokens by lowercasing and applying 
    stemming or lemmatization.
    '''
    assert type(tokens) == list

    l_cased = [token.lower() for token in tokens]

    if method == 'stemming':
        normalized = [stemmer.stem(token) for token in l_cased]
    else:
        normalized = [lemmatizer.lemmatize(token) for token in l_cased]

    return normalized
