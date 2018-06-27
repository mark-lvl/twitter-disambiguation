from twipy import TwiPy
from bagofwords import BagOfWords
from sklearn.feature_extraction import DictVectorizer
from sklearn.naive_bayes import BernoulliNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
from sklearn.externals import joblib
import numpy as np
import pandas as pd
import os
import errno


def set_pipeline():
    return Pipeline([('bag-of-words', BagOfWords()),
                    ('vectoring', DictVectorizer()),
                    ('naive-bayes', BernoulliNB())])


def export_model(phrase, model_context):
    # Check for directory existence
    model_filename = os.path.join(os.path.curdir, 'output', 'models', phrase + '_model.pkl')
    if not os.path.exists(os.path.dirname(model_filename)):
        try:
            os.makedirs(os.path.dirname(model_filename))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

    joblib.dump(model_context, model_filename)


def import_model(phrase):
    model_filename = os.path.join(os.path.curdir, 'output', 'models', phrase + '_model.pkl')

    if not os.path.exists(model_filename):
        return False
    else:
        return joblib.load(model_filename)


def build_model(phrase, export=False):
    twipy = TwiPy()

    tweets_df = twipy.get_tweets(phrase)

    if tweets_df.isnull().values.any():
        return False

    pipeline = set_pipeline()

    if export:
        model = pipeline.fit(tweets_df['Tweet'],
                             tweets_df['Label'])
        export_model(phrase, model)

    scores = cross_val_score(pipeline,
                             tweets_df['Tweet'],
                             tweets_df['Label'],
                             scoring='f1')

    return np.mean(scores)


def list_top_words(phrase):
    model = import_model(phrase)
    
    # if model isn't exist then build and export the model
    if not model:
        model = build_model(phrase, True)

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