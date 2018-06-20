# import libraries
import twitter
import os
import json
import errno


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

        self.tweets = self.api.GetSearch(term=query, count=count)

    def export_tweets(self):
        output_filename = os.path.join(os.path.curdir, 'output', 'twitter', 'python_tweets.json')

        if not os.path.exists(os.path.dirname(output_filename)):
            try:
                os.makedirs(os.path.dirname(output_filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

        with open(output_filename, 'a') as output_file:
            for tweet in self.tweets:
                if tweet.text != "":
                    output_file.write(json.dumps(tweet.text))
                    output_file.write("\n\n")

    def import_tweets(self):
        input_filename = os.path.join(os.path.curdir, 'output', 'twitter', 'python_tweets.json')
        labels_filename = os.path.join(os.path.curdir, 'output', 'twitter', 'python_classes.json')

        with open(input_filename) as tweet_json_file:
            for tweet in tweet_json_file:
                if len(tweet.strip()) == 0:
                    continue
                self.tweets.append(json.loads(tweet))

        labels = []
        if os.path.exists(labels_filename):
            with open(labels_filename) as label_file:
                labels = json.load(label_file)


if __name__ == '__main__':

    twipy = TwiPy()
    twipy.search_tweets('python')
    twipy.export_tweets()
    twipy.import_tweets()
