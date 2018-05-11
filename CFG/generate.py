"""
Issues:
    1. Use CoreNLP's tokenization and only operate on those tokens.
    2. Recalculates cfg, bigram matrix, sample, ecery time. Need cache.
"""

import pickle
import json
import pandas as pd
import requests
import random

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from nltk import Tree, Nonterminal

import context_free_grammar
import bigram_matrix
import preprocess
import generate_methods


def load_tweets(filepath):
    """
    Opens a pickle file of tweets from Twitter API and extracts the text.

    params:
        filepath (str): Absolute path to .pkl

    returns:
        (list): text properties of all tweets in .pkl
    """
    with open(filepath, 'rb') as tpkl:
        tt = pickle.load(tpkl)

    tweets = [status.text for status in tt]

    return tweets


# Deprecated by preprocess module & one-liner
def get_corpus(tweet_list):
    """
    Creates corpus class from list of tweets

    params:
        tweet_list (list): list of tweet text from Twitter API

    returns:
        (Corpus): corpus class containing all the text and markov transition
            matrix
    """
    text = ' '.join(tweet_list).replace('\n', ' ')  # remove stray newlines

    corpus = bigram_matrix.Corpus(text)
    return corpus

# Deprecated by preprocess module & one-liner
def get_sample(tweet_list, n=10):
    """
    Creates sample string from list of tweets to generate from.

    params:
        tweet_list (list): list of tweet text from Twitter API
        n (int): number of tweets to retain in sample

    returns:
        (str): string of sample text
    """
    random_sample = random.sample(tweet_list, n)

    sample = ' '.join(random_sample).replace('\n', ' ')  # remove stray newlines

    return sample


def constituency_parse(url, text):
    """
    Custom wrapper for the Stanford CoreNLP Server API. The CoreNLP server must be running.

    params:
        url (str): url of CoreNLP server with port. e.g. 'http://localhost:9000'
        text (str): text to parse

    returns:
        (list): parse strings in CoreNLP format.
    """
    data = text.encode('utf-8')
    properties = {'annotators': 'pos,parse', 'outputFormat': 'json'}
    params = {'properties': str(properties), 'pipelineLanguage': 'en'}

    r = requests.post(url, params=params, data=data, headers={'Connection': 'close'})
    r_dict = json.loads(r.text)

    return [sent['parse'] for sent in r_dict['sentences']]


def pos_tag(url, text):
    """
    Custom wrapper for the Stanford CoreNLP Server API. The CoreNLP server must be running.

    params:
        url (str): url of CoreNLP server with port. e.g. 'http://localhost:9000'
        text (str): text to tag

    returns:
        (list): tags in Penn Treebank format.
    """
    data = text.encode('utf-8')
    properties = {'annotators': 'pos', 'outputFormat': 'json'}
    params = {'properties': str(properties), 'pipelineLanguage': 'en'}

    r = requests.post(url, params=params, data=data, headers={'Connection': 'close'})
    r_dict = json.loads(r.text)

    return [token['pos'] for sent in r_dict['sentences'] for token in sent['tokens']]


def tokenize(url, text):
    """
    Custom wrapper for the Stanford CoreNLP Server API. The CoreNLP server must be running.

    params:
        url (str): url of CoreNLP server with port. e.g. 'http://localhost:9000'
        text (str): text to tag

    returns:
        (list): tags in Penn Treebank format.
    """
    data = text.encode('utf-8')
    properties = {'annotators': 'tokenize', 'outputFormat': 'json'}
    params = {'properties': str(properties), 'pipelineLanguage': 'en'}

    r = requests.post(url, params=params, data=data, headers={'Connection': 'close'})
    r_dict = json.loads(r.text)

    return [token['word'] for token in r_dict['tokens']]


def create_cfg(parsed_sample):
    """
    Populates CFG with rules learned from CoreNLP Constituency parse

    params:
        parsed_sample (list): Parse-strings of sample

    returns:
        (CFG): CFG of rules learned
    """
    cfg = context_free_grammar.CFG()

    for sent in parsed_sample:
        tree = Tree.fromstring(sent)
        struct_rules = [(rule.lhs(), rule.rhs()) for rule in tree.productions()]
        for rule in struct_rules:
            if rule[1] not in cfg.productions[rule[0]]:
                cfg.productions[rule[0]].append(rule[1])

    return cfg


def pos_bucket_generate(cfg, tags):
    """
    Locate POS tag in CFG and replace it with a random terminal expansion

    params:
        cfg (CFG): contains all possible nonterminal to terminal expansions
        tags (list): POS tags from the sentence to replicate in sentence order
    returns:
        (list): terminal tokens generated
    """

    return [random.choice(cfg.productions[Nonterminal(tag)])[0] for tag in tags]


if __name__ == '__main__':

    choice = -1
    while choice not in ['y','n']:
        choice = input('\nEnter Own Text?\n> ')

    print('Initializing....')
    # -------- Load Tweets --------
    filepath = '/Users/asp/GitHub/msis-project/twitter_api/trump_tweets.pkl'
    url = 'http://localhost:9000'


    if choice == 'y':
        print('Use only periods (.) to separate sentences. No newlines in copy/paste text.\n')
        user_text = input('\nEnter your text here:\n> ')
        tt_clean = user_text
        sample_tweets = random.sample(user_text.split('. '), 1)
        # print(sample_tweets)  # Debug
        sample_clean = sample_tweets[0]

    else:
        # All tweets
        tt = load_tweets(filepath)  # list of str
        tt_text = ' '.join(tt)  # concatenated str
        tt_clean = preprocess.preprocess(tt_text)

        # Sample of tweets
        sample_tweets = random.sample(tt, 5)  # CFG: More than 5 never terminates
        # sample_tweets = random.sample(tt, 500)  # POS-bin
        sample_text = ' '.join(sample_tweets)  # concatenated str
        sample_clean = preprocess.preprocess(sample_text)
        # print(sample_clean)  # View Template text

    # -------- CFG Rules --------
    parse_tree = constituency_parse(url, sample_clean)
    cfg = create_cfg(parse_tree)  # convenience method to load rules

    # -------- Bigram Matrix --------
    corpus = bigram_matrix.Corpus(tt_clean)  # all tweets

    # UI Loop
    while True:
        choice = -1
        while choice not in [1,2,3,4]:
            choice = int(input('\nChoose ranking method:\n1. CFG-Generation & Sum\n2. CFG-Generation & Cosine Similarity\n3. Lowest-Symbol-Generation & Sum\n4. Lowest-Symbol-Generation & Cosine Similarity\n> '))

        if choice == 1:
            print('cfg_gen_sum')
            generate_methods.cfg_gen_sum(tt_clean, cfg, corpus)
        elif choice == 2:
            print('cfg_gen_cos')
            generate_methods.cfg_gen_cos(tt_clean, cfg)
        elif choice == 3:
            print('pos_gen_sum')
            generate_methods.pos_gen_sum(corpus, sample_tweets, cfg, url)
        elif choice == 4:
            print('pos_gen_cos')
            generate_methods.pos_gen_cos(tt_clean, sample_tweets, cfg, url)
