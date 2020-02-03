from flask import Flask, render_template, url_for, request
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from nltk.stem.porter import PorterStemmer

def remove_pattern(input_text, pattern):
    r = re.findall(pattern, input_text)
    for i in r:
        input_text = re.sub(i, '', input_text)
    return input_text

def count_punct(text):
    count = sum([1 for char in text if char in string.punctuation])
    return round(count/(len(text) -text.count(' ')), 3)*100

app = Flask(__name__)

# Data Collection

data = pd.read_csv('sentiment.tsv', sep='\t')

# Data Cleaning 

data['label'] = data['label'].map({'pos':0, 'neg':1})
data['tidy_text'] = np.vectorize(remove_pattern)(data['text'], r'@[\w]*')
data['tidy_text'] = data['tidy_text'].str.replace(r'[^a-zA-Z#]', ' ')
data['tidy_text'] = data['tidy_text'].apply(lambda x: x.split())

# Apply Stemming
stemmer = PorterStemmer()
stemmed_text = data['tidy_text'].apply(lambda x: [stemmer.stem(i) for i in x]) 
for text_index in range(len(stemmed_text)):
    stemmed_text[text_index] = ' '.join(stemmed_text[text_index])
data['tidy_text'] = stemmed_text
data['body_len'] = data['tidy_text'].apply(lambda x: (len(x)- x.count(' ')))
data['body_len'].replace(0, np.nan, inplace=True)
data.dropna(inplace=True)
data['punc%'] = data['tidy_text'].apply(lambda x: count_punct(x))

# Apply Scaling

x = data['tidy_text']
y = data['label']
t_vect = TfidfVectorizer()
x = t_vect.fit_transform(x)
data = pd.concat([
    data['body_len'],
    data['punc%'],
    pd.DataFrame(x.toarray()
    data['label']
)], axis=1)

# Initialize Classifier
x = data.drop('label', axis=1)
y = data['label']
classifier = SVC(kernel='rbf', gamma=1, C=0.1)
classifier.fit(x, y)

