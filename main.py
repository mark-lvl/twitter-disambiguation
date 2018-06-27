from twipy import TwiPy
import argparse
from colorama import Fore, Back, init
import naivebayes_model as nbm


if __name__ == '__main__':
    # reset color changes
    init(autoreset=True)

    parser = argparse.ArgumentParser(prog='main',
                                     usage='%(prog)s func [options]',
                                     description='Disambiguating the use of the given term  on Twitter stream.')
    parser.add_argument(
        'func',
        choices=['fetch_tweets',
                 'label_tweets',
                 'build_model',
                 'list_top_words',
                 'predict'],
        help='The method name to call')
    parser.add_argument(
        '-p',
        '--phrase',
        required=True,
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
    if args.func and not args.phrase:
        parser.error('For chosen function, -p argument is required.')

    twipy = TwiPy()

    if args.func == 'fetch_tweets':
        if not args.phrase:
            print(Fore.RED + 'use -p option to set phrase.')
        # fetch tweets from api
        tweets, tweets_filename = twipy.fetch_tweets(args.phrase, args.count)
        print(Back.GREEN + Fore.BLACK + '{} tweets exported in {} successfully.'.format(len(tweets),
                                                                                        tweets_filename))

    if args.func == 'label_tweets':
        twipy.disambiguate_tweets(args.phrase)

    # Constructing the model printing the score
    if args.func == 'build_model':
        score = nbm.build_model(args.phrase, True)
        if not score:
            print(Back.RED + Fore.BLACK + "There are unlabeled tweets, run label_tweets again.")
        else:
            print(Back.GREEN + Fore.BLACK + "Model f1-Score mean: {:.3f}".format(score))

    if args.func == 'list_top_words':
        print(nbm.list_top_words(args.phrase))

    if args.func == 'predict':
        if not args.phrase:
            print(Fore.RED + 'use -p option to set phrase.')
        print(nbm.model_prediction(args.phrase, args.count))


