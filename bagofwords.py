from nltk.tokenize import TweetTokenizer
from sklearn.base import TransformerMixin


class BagOfWords(TransformerMixin):

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        tokenizer = TweetTokenizer()
        return [{word: True
                 for word in tokenizer.tokenize(document)}
                for document in X]