import nltk
from sklearn.base import TransformerMixin


class BagOfWords(TransformerMixin):

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return [{word: True
                 for word in nltk.word_tokenize(document)}
                for document in X]