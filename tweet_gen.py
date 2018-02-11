import os
import codecs

from numpy import random
from collections import Counter

from markov import MarkovChain
from utils.twitter import load_tweets_for_user

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VOCABULARY_LIMIT = 10000
START_TOKEN = "START_TOKEN"
END_TOKEN = "END_TOKEN"


def build_vocabulary(sentences):
    vocabulary = []

    for sentence in sentences:
        sentence = sentence.strip("b").strip("'")
        vocabulary.extend(sentence.split(" "))

    counter = Counter(vocabulary).most_common(VOCABULARY_LIMIT)
    vocabulary = [word for word, freq in counter]

    return vocabulary


def generate_new_sentence(markov_chain):
    sentence = []
    word = START_TOKEN

    sentence = []
    word = START_TOKEN

    while word != END_TOKEN:
        if word != START_TOKEN:
            sentence.append(word)

        word_idx = markov_chain.get_state_index(word)
        next_word = random.choice(markov_chain.states, p=markov_chain.T[word_idx])
        word = next_word

    return codecs.decode(" ".join(sentence), "unicode_escape")


def generate_n_sentences(markov_chain, n=10):
    sentences = []

    for i in range(n):
        sentence = generate_new_sentence(markov_chain)
        sentences.append(sentence)

    return sentences


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--account", type=str, dest="account")
    parser.add_argument("--n-tweets", "-n", type=int, dest="n_tweets", default=10)
    args = parser.parse_args()

    df = load_tweets_for_user(args.account)
    tweets = df.text

    vocabulary = build_vocabulary(tweets)
    markov_chain = MarkovChain(vocabulary)
    markov_chain.train_with_sentences(tweets)

    sentences = generate_n_sentences(markov_chain, args.n_tweets)
    for sentence in sentences:
        print(sentence)
