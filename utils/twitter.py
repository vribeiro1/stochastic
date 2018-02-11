import os
import tweepy
import pandas as pd

from collections import namedtuple
from decouple import config

START_TOKEN = "START_TOKEN"
END_TOKEN = "END_TOKEN"
PKG_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(PKG_DIR)

CONSUMER_KEY = config("CONSUMER_KEY", default="")
CONSUMER_SECRET = config("CONSUMER_SECRET", default="")
ACCESS_TOKEN = config("ACCESS_TOKEN", default="")
ACCESS_TOKEN_SECRET = config("ACCESS_TOKEN_SECRET", default="")

TwitterAuth = namedtuple("TwitterAuth", ["consumer_key", "consumer_secret", "access_token", "access_token_secret"])


def get_api(auth_keys):
    auth = tweepy.OAuthHandler(auth_keys.consumer_key, auth_keys.consumer_secret)
    auth.set_access_token(auth_keys.access_token, auth_keys.access_token_secret)

    return tweepy.API(auth)


def get_tweets_from_user(api, screen_name):
    all_tweets = []

    new_tweets = api.user_timeline(screen_name=screen_name, count=200)
    all_tweets.extend(new_tweets)

    oldest = all_tweets[-1].id - 1

    while len(new_tweets) > 0:
        new_tweets = api.user_timeline(screen_name=screen_name, count=200, max_id=oldest)
        all_tweets.extend(new_tweets)

        oldest = all_tweets[-1].id - 1

    tokenize = lambda tweet: " ".join([START_TOKEN, tweet.text, END_TOKEN]).encode("utf-8")
    tweets = [(tweet.id_str, tweet.created_at, tokenize(tweet)) for tweet in all_tweets]
    return tweets


def load_tweets_for_user(screen_name):
    if not screen_name:
        raise Exception("Required account to load tweets")

    filename = os.path.join(BASE_DIR, "data", "{}_tweets.csv".format(screen_name))

    if os.path.isfile(filename):
        df = pd.read_csv(filename)
    else:
        auth = TwitterAuth(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET,
                           access_token=ACCESS_TOKEN, access_token_secret=ACCESS_TOKEN_SECRET)

        api = get_api(auth)
        tweets = get_tweets_from_user(api, screen_name)
        df = pd.DataFrame(tweets, columns=["id", "created_at", "text"])
        df.to_csv(filename, index=False)

    return df


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--account", type=str, dest="account")
    args = parser.parse_args()

    load_tweets_for_user(args.account)
