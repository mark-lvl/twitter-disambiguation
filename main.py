# import libraries
import twitter
import os
import json
import errno
from collections import defaultdict


class TwiPy:

    tweets: list

    def __init__(self):
        self.api = twitter.Api(consumer_key="YOUR_CONSUMER_KEY",
                               consumer_secret="YOUR_CONSUMER_SECRET_KEY",
                               access_token_key="ACCESS_KEY",
                               access_token_secret="ACCESS_SECRET")
        self.tweets = []

    def search_tweets(self, query, count=100):
        if query == "":
            return False

        return self.api.GetSearch(term=query, count=count)

    def export_tweets(self, raw_tweets):
        output_filename = os.path.join(os.path.curdir, 'output', 'twitter', 'python_tweets.json')

        if not os.path.exists(os.path.dirname(output_filename)):
            try:
                os.makedirs(os.path.dirname(output_filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        with open(output_filename, 'a') as output_file:

            tweets_list = dict((tweet.id, tweet.text) for tweet in raw_tweets if tweet.text != "")

            output_file.write(json.dumps(tweets_list,
                                         sort_keys=True,
                                         indent=4))

    def import_tweets(self):
        input_filename = os.path.join(os.path.curdir, 'output', 'twitter', 'python_tweets.json')
        labels_filename = os.path.join(os.path.curdir, 'output', 'twitter', 'python_classes.json')

        with open(input_filename) as tweet_json_file:
            self.tweets = json.loads(tweet_json_file.read())

        labels = defaultdict(int)
        if os.path.exists(labels_filename):
            with open(labels_filename, 'r') as label_file:
                labels = json.load(label_file)

        return labels

    def set_labels(self):
        labels_filename = os.path.join(os.path.curdir, 'output', 'twitter', 'python_classes.json')
        labels = self.import_tweets()


        for tweet_idx in self.tweets.keys():
            if tweet_idx in labels:
                continue
            print("Set the relevance to the topic for this tweet: [0: Not relevant, 1: Relevant]\n")
            print(self.tweets[tweet_idx])
            labels[tweet_idx] = int(input("Enter 0 or 1:"))
            print('='*40)

            with open(labels_filename, 'w') as labels_file:
                labels_file.write(json.dumps(labels,
                                             sort_keys=True,
                                             indent=4))



if __name__ == '__main__':

    twipy = TwiPy()
    raw_tweets = twipy.search_tweets('python')
    twipy.export_tweets(raw_tweets)
    twipy.import_tweets()
    twipy.set_labels()

