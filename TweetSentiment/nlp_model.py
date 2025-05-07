#!/usr/bin/python
import pandas as pd
import _pickle as cPickle
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score

def make_model():
    model_builder = ModelBuilder(TrainDataProvider().df)
    model_builder.serialize_model()

class ModelBuilder:
    def __init__(self, df):
        self.model_tfidf = None
        self.build_tfidf(self.get_train_tweets(df), df)

    def get_train_tweets(self, df):
        tweets = []
        for i in df['Tweet']:
            tweets.append(' '.join(map(str,i)))
        return tweets

    def build_tfidf(self, tweets, df):
        x_train, x_test, y_train, y_test = train_test_split(tweets, df['Sentiment'], test_size=0.3, random_state=12, stratify=df['Sentiment'])
        vectorizer_tfidf = TfidfVectorizer(max_features=1500, ngram_range=(1,2))
        vectorizer_tfidf.fit(x_train)
        classifier_tfidf = LogisticRegression(max_iter=200)

        self.model_tfidf = Pipeline([("vectorizer", vectorizer_tfidf), ("classifier", classifier_tfidf)])
        self.model_tfidf.fit(x_train, y_train)

        #predicted_train_tfidf = self.model_tfidf.predict(x_train)
        #accuracy_train_tfidf = accuracy_score(y_train, predicted_train_tfidf)
        #predicted_test_tfidf = self.model_tfidf.predict(x_test)
        #accuracy_test_tfidf = accuracy_score(y_test, predicted_test_tfidf)
        #print('Accuracy Training data: {:.3%}'.format(accuracy_train_tfidf))
        #print('Accuracy Test data: {:.1%}'.format(accuracy_test_tfidf))        
    
    def serialize_model(self):
        with open('Resources/tfidf_model.pk', 'wb') as fin:
            cPickle.dump(self.model_tfidf, fin)

class TrainDataProvider:
    def __init__(self):
        self.df = pd.DataFrame()
        self.read_train_data()
        self.tokenize_train_data()
        self.clean_train_data()
        self.lemmatize_train_data()

    def read_train_data(self):
        self.df = pd.read_csv("Resources/fifa_world_cup_2022_tweets.csv")
        self.df = self.df[['Tweet', 'Sentiment']]
        self.df.dropna()
    
    def tokenize_train_data(self):
        for idx, i in enumerate(self.df['Tweet']):
            self.df['Tweet'][idx] = word_tokenize(self.df['Tweet'][idx])

    def clean_train_data(self):
        chars_to_remove = ['!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', ']', '^', '_', '`', '{', '|', '}', '~']
        stop_words = set(stopwords.words("english"))
        for i in self.df['Tweet']:
            for idx, j in enumerate(i):
                i[idx] = j.translate({ord(x): '' for x in chars_to_remove})
                i[idx] = str(i[idx]).lower()
                if ((i[idx] == '') | (i[idx] == ' ') | (i[idx] in stop_words)):
                    i.remove(i[idx])
        
    def lemmatize_train_data(self):
        lemmatizer = WordNetLemmatizer()
        for i in (self.df['Tweet']):
            for idx, j in enumerate(i):
                i[idx] = lemmatizer.lemmatize(j)
