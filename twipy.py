# import libraries
import twitter
import config
import os
import json
import re
import errno
from collections import defaultdict
import pandas as pd


class TwiPy:

    def __init__(self):
        # config the twitter api
        self.api = twitter.Api(consumer_key=config.TWITTER_CONFIG['consumer_key'],
                               consumer_secret=config.TWITTER_CONFIG['consumer_secret'],
                               access_token_key=config.TWITTER_CONFIG['access_token_key'],
                               access_token_secret=config.TWITTER_CONFIG['access_token_secret'])

    def fetch_tweets(self, phrase, count=100, export=True):
        # format the query phrase
        phrase = re.findall("[a-zA-Z0-9-]+", phrase)
        phrase = phrase[0].lower()

        # fetch tweets from twitter api
        raw_tweets = self.api.GetSearch(term=phrase,
                                        count=count,
                                        result_type="recent",
                                        lang='en')

        processed_tweets = {int(tweet.id): tweet.text for tweet in raw_tweets if tweet.text != ""}

        # if export set to false means return recent fetched tweets
        if not export:
            # set None for filename if export is off
            return processed_tweets, None

        # set file names
        tweets_filename, labels_filename, tweets, labels = self.file_loader(phrase)

        # Append recent fetched tweets to the tweets file
        with open(tweets_filename, 'w') as output_file:
            tweets.update(processed_tweets)

            # Convert all keys to int before encoding in json - it helps following sort
            tweets = {int(k): v for k, v in tweets.items()}

            output_file.write(json.dumps(tweets,
                                         sort_keys=True,
                                         indent=4))

            return tweets, tweets_filename

    def file_loader(self, phrase):
        if not phrase:
            return False

        # Check for directory existence
        tweets_filename = os.path.join(os.path.curdir, 'output', 'data', phrase + '_tweets.json')
        if not os.path.exists(os.path.dirname(tweets_filename)):
            try:
                os.makedirs(os.path.dirname(tweets_filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        # dictionary of all existing and recent fetched tweets
        tweets = defaultdict()
        # Load the current file in case of existence and having content
        if os.path.isfile(tweets_filename) and (os.path.getsize(tweets_filename) > 0):
            with open(tweets_filename, 'r') as tweet_file:
                # First append existing tweets to the tweet dictionary
                tweets = dict(json.load(tweet_file))

        # Loading the label file and convert contents to dictionary
        labels_filename = os.path.join(os.path.curdir, 'output', 'data', phrase + '_labels.json')
        labels = defaultdict(int)
        if os.path.exists(labels_filename):
            with open(labels_filename, 'r') as label_file:
                labels = json.load(label_file)

        return tweets_filename, labels_filename, tweets, labels

    def disambiguate_tweets(self, phrase):

        tweets_filename, labels_filename, tweets, labels = self.file_loader(phrase)

        for tweet_idx in tweets.keys():
            # following statement means the tweet was already labels so we can jump over it
            if tweet_idx in labels:
                continue

            print("Set the relevance to the topic for this tweet: [0: Not relevant, 1: Relevant]\n")
            print('=' * 40)
            print(tweets[tweet_idx])
            print('=' * 40, '\n')
            # Getting value from terminal input and evaluate
            while True:
                picked_label = input("Enter 0 or 1:")
                if picked_label not in ["0", "1"]:
                    print("Bad input, choose between [0: Not relevant, 1: Relevant]\n")
                else:
                    break
            labels[tweet_idx] = int(picked_label)

            os.system('clear')

            with open(labels_filename, 'w') as labels_file:
                labels_file.write(json.dumps(labels,
                                             sort_keys=True,
                                             indent=4))

    def get_tweets(self, phrase):

        tweets_filename, labels_filename, tweets, labels = self.file_loader(phrase)

        tweets_df = pd.DataFrame.from_dict(tweets,
                                           orient='index',
                                           columns=['Tweet'])

        labels_df = pd.DataFrame.from_dict(labels,
                                           orient='index',
                                           columns=['Label'])

        full_df = pd.concat([tweets_df, labels_df], axis=1, sort=False)

        return full_df

