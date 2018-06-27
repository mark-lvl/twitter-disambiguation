from twipy import TwiPy
from bagofwords import BagOfWords
from sklearn.feature_extraction import DictVectorizer
from sklearn.naive_bayes import BernoulliNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
import numpy as np
import pandas as pd


def set_pipeline():
    return Pipeline([('bag-of-words', BagOfWords()),
                    ('vectoring', DictVectorizer()),
                    ('naive-bayes', BernoulliNB())])


def build_model(phrase):
    twipy = TwiPy()

    tweets_df = twipy.get_tweets(phrase)

    if tweets_df.isnull().values.any():
        return False

    pipeline = set_pipeline()

    scores = cross_val_score(pipeline,
                             tweets_df['Tweet'],
                             tweets_df['Label'],
                             scoring='f1')

    return np.mean(scores)


def list_top_words(phrase):
    twipy = TwiPy()

    tweets_df = twipy.get_tweets(phrase)

    pipeline = set_pipeline()

    model = pipeline.fit(tweets_df['Tweet'],
                         tweets_df['Label'])

    # get the log probability for each feature in NB model
    nb = model.named_steps['naive-bayes']
    feature_probabilities = nb.feature_log_prob_

    # sorting based on probability only for top 20 features
    top_features = np.argsort(-nb.feature_log_prob_[1])[:20]

    # getting the feature value instead of its index
    vector_matrix = model.named_steps['vectoring']

    return pd.DataFrame([{'feature': vector_matrix.feature_names_[feature_index],
                          'prob': np.exp(feature_probabilities[1][feature_index])}
                         for feature_index in top_features])

