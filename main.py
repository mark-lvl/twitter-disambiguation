from twipy import TwiPy
import argparse
from colorama import Fore, Back, Style, init
from bagofwords import BagOfWords
from sklearn.feature_extraction import DictVectorizer
from sklearn.naive_bayes import BernoulliNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score
import numpy as np


if __name__ == '__main__':
    # reset color changes
    init(autoreset=True)

    parser = argparse.ArgumentParser(prog='main',
                                     usage='%(prog)s func [options]',
                                     description='Disambiguating the use of the given term  on Twitter stream.')
    parser.add_argument(
        'func',
        choices=['fetch_tweets', 'label_tweets'],
        help='The method name to call')
    parser.add_argument(
        '-p',
        '--phrase',
        nargs='?',

        help='The phrase you want to disambiguate in tweets, only alphanumeric and hyphen.')
    parser.add_argument(
        '-c',
        '--count',
        nargs='?',
        const=100,
        default=100,
        help='Number of tweets to return containing the given term'
    )
    # checks arguments dependencies
    args = parser.parse_args()
    if args.func in ['fetch_tweets', 'label_tweets'] and not args.phrase:
        parser.error('For chosen function, -p argument is required.')

    twipy = TwiPy()
    if args.func == 'fetch_tweets':
        twipy.fetch_tweets(args.phrase, args.count)

    if args.func == 'label_tweets':
        twipy.disambiguate_tweets(args.phrase)

    # tweets = twipy.get_tweets()
    #
    # pipeline = Pipeline([('bag-of-words', BagOfWords()),
    #                      ('vectorizer', DictVectorizer()),
    #                      ('naive-bayes', BernoulliNB())
    #                      ])
    #
    # scores = cross_val_score(pipeline, tweets['Tweet'], tweets['Label'], scoring='f1')
    # print("Score: {:.3f}".format(np.mean(scores)))
    #
    # model = pipeline.fit(tweets['Tweet'], tweets['Label'])
    #
    # nb = model.named_steps['naive-bayes']
    # feature_probabilities = nb.feature_log_prob_
    #
    # top_features = np.argsort(-nb.feature_log_prob_[1])[:50]
    #
    # dv = model.named_steps['vectorizer']
    #
    # for i, feature_index in enumerate(top_features):
    #     print(i, dv.feature_names_[feature_index], np.exp(feature_probabilities[1][feature_index]))
    #
