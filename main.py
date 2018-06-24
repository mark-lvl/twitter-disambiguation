from twipy import TwiPy
import pandas as pd
from bagofwords import BagOfWords
from sklearn.feature_extraction import DictVectorizer
from sklearn.naive_bayes import BernoulliNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score,cross_val_predict
import numpy as np
from sklearn.model_selection import GridSearchCV

if __name__ == '__main__':

    twipy = TwiPy()
    # raw_tweets = twipy.search_tweets('python')
    # twipy.export_tweets(raw_tweets)
    twipy.import_tweets()
    # twipy.set_labels()

    tweets = twipy.get_tweets()

    pipeline = Pipeline([('bag-of-words', BagOfWords()),
                         ('vectorizer', DictVectorizer()),
                         ('naive-bayes', BernoulliNB())
                         ])

    scores = cross_val_score(pipeline, tweets['Tweet'], tweets['Label'], scoring='f1')
    print("Score: {:.3f}".format(np.mean(scores)))



