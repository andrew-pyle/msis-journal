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

    # # -------- POS Tags --------
    # train = random.choice(sample_tweets)  # select random tweet
    # # train = tweets[index]  # training tweet
    # # train = 'Military and economy are getting stronger by the day, and our enemies know it. #MAGA'
    # train_clean = preprocess.preprocess(train)
    # tags = pos_tag(url, train)  # get POS tags
    # print(train_clean)  # View Template text

    # # # -------- CFG Generate & Sum Rank --------
    # # outs = {'sentence': [], 'score': []}

    # # for x in range(100):
    # #     sent = cfg.nltk_expand(Nonterminal('ROOT'), alpha=0.01)
    # #     if len(sent) < 25:
    # #         line = ' '.join(sent)
    # #         outs['sentence'].append(line)
    # #         outs['score'].append(bigram_matrix.rate_sentence(line, corpus))
    
    # # out = outs['sentence']


    # # -------- POS Generate & Sum Rank --------
    # outs = {'sentence': [], 'score': []}
    # out = []
    
    # for x in range(100):
    #     # Fill POS tag list with terminal symbols
    #     sent = pos_bucket_generate(cfg, tags)  # list of terminal symbols
    #     line = ' '.join(sent)
    #     outs['sentence'].append(line)
    #     # outs['score'].append(bigram_matrix.rate_sentence(line, corpus))

    # out = outs['sentence']

    # # # -------- Bigram Matrix Output --------
    # # df = pd.DataFrame(data=outs)
    # # pd.set_option('display.max_colwidth', -1)
    # # print(df.sort_values(by='score', ascending=False).head(n=5))
    # # print(df.sort_values(by='score', ascending=False).tail(n=5))
    


    # # -------- Cosine Similarity --------
    # univec = CountVectorizer(ngram_range=(1,1), token_pattern=r'(?u)\b\w+\b')
    # bivec = CountVectorizer(ngram_range=(2,2), token_pattern=r'(?u)\b\w+\b')
    # # trivec = CountVectorizer(ngram_range=(3,3), token_pattern=r'(?u)\b\w+\b')
    # # quadvec = CountVectorizer(ngram_range=(4,4), token_pattern=r'(?u)\b\w+\b')

    # # Create list of sentences
    # corp = [tt_clean]
    # for sent in out:
    #     corp.append(sent)

    # X1 = univec.fit_transform(corp)
    # X2 = bivec.fit_transform(corp)
    # # X3 = trivec.fit_transform(corp)
    # # X4 = quadvec.fit_transform(corp)

    # # Cosine Similarity: compare corpus to all
    # score1 = cosine_similarity(X1[0], X1[1:])
    # df1 = pd.DataFrame({'text': out, 'score': score1[0]})

    # score2 = cosine_similarity(X2[0], X2[1:])
    # df2 = pd.DataFrame({'text': out, 'score': score2[0]})

    # # score3 = cosine_similarity(X3[0], X3[1:])
    # # df3 = pd.DataFrame({'text': out, 'score': score3[0]})

    # # score4 = cosine_similarity(X4[0], X4[1:])
    # # df4 = pd.DataFrame({'text': out, 'score': score4[0]})

    # # Pandas Display options
    # pd.set_option('display.max_colwidth', -1)
    # pd.set_option('display.max_columns', None)

    # # Top results
    # print('unigram', df1.nlargest(10, 'score'), '\n')
    # print('unigram', df1.nsmallest(10, 'score'), '\n')

    # print('bigram', df2.nlargest(10, 'score'), '\n')
    # print('bigram', df2.nsmallest(10, 'score'), '\n')

    # # print('trigram', df3.nlargest(10, 'score'), '\n')
    # # print('trigram', df3.nsmallest(10, 'score'), '\n')

    # # print('quadrigram', df4.nlargest(10, 'score'), '\n')
    # # print('quadrigram', df4.nsmallest(10, 'score'), '\n')


    # # # Load tweets
    # # filepath = '/Users/asp/GitHub/msis-project/twitter_api/trump_tweets.pkl'
    # # url = 'http://localhost:9000'

    # # tt = load_tweets(filepath)

    # # corpus = get_corpus(tt)
    # # sample = get_sample(tt, n=7)
    # # sample = preprocess.preprocess(sample)
    # # text = sample

    # # # Create CFG rules
    # # parse_string = constituency_parse(url, sample)
    # # cfg = create_cfg(parse_string)

    # # # Debug
    # # print(cfg.productions)

    # # # CFG Generation
    # # outs = {'sentence': [], 'score': []}

    # # for x in range(100):
    # #     sent = cfg.nltk_expand(Nonterminal('ROOT'), alpha=0.01)
    # #     if len(sent) < 25:
    # #         line = ' '.join(sent)
    # #         outs['sentence'].append(line)
    # #         outs['score'].append(bigram_matrix.rate_sentence(line, corpus))
    
    # # out = outs['sentence']
    
    # # # Bigram Matrix Output
    # # df = pd.DataFrame(data=outs)
    # # pd.set_option('display.max_colwidth', -1)
    # # print(df.sort_values(by='score', ascending=False).head(n=5))
    # # print(df.sort_values(by='score', ascending=False).tail(n=5))

    # # #
    # # index = random.choice(range(len(tt)))
    # # tags = pos_tag(url, tt[index])

    # # tw = pos_bucket_generate(cfg, tags)

    # # print(' '.join(tw))

    # # POS generation
    # # -------- Cache --------
    # # Load tweets
    # # filepath = '/Users/asp/GitHub/msis-project/twitter_api/trump_tweets.pkl'
    # # url = 'http://localhost:9000'

    # # tt = load_tweets(filepath)

    # # # Select slice of tweets
    # # tweets = random.sample(tt, 5)

    # # # Create CFG
    # # text = ' '.join(tweets)  # text to parse
    # # text = preprocess.preprocess(text)  # see preprocess module
    # # parse_tree = constituency_parse(url, text)  # CoreNLP constituency parse
    # # cfg = create_cfg(parse_tree)  # convenience method to load rules

    # # # Create Bigram matrix
    # # corpus = get_corpus(tt)

    # # # -------- New Seed Sentence --------
    # # # Get POS Tag list
    # # index = random.choice(range(len(tweets)))  # select random tweet
    # # train = tweets[index]  # training tweet
    # # # train = 'Military and economy are getting stronger by the day, and our enemies know it. #MAGA'
    # # train = preprocess.preprocess(train)
    # # tags = pos_tag(url, train)  # get POS tags
    # # print(train)  # Debug
    # # print(tags)

    # # outs = {'sentence': [], 'score': []}
    # # out = []
    # # # -------- POS Generate --------
    # # for x in range(100):
    # #     # Fill POS tag list with terminal symbols
    # #     sent = pos_bucket_generate(cfg, tags)  # list of terminal symbols
    # #     line = ' '.join(sent)
    # #     outs['sentence'].append(line)
    # #     outs['score'].append(bigram_matrix.rate_sentence(line, corpus))

    # # out = outs['sentence']

    # # # -------- CFG Generate --------
    # # # for x in range(5):
    # # #     txt = cfg.nltk_expand(Nonterminal('ROOT'), alpha=0.00001)
    # # #     if len(txt) < 20:
    # # #         line = ' '.join(txt)
    # # #         out.append(line)

    # # print(out) # debug

    # # # -------- Bigram Matrix Rate --------
    # # # Bigram Matrix Output
    # # df = pd.DataFrame(data=outs)
    # # pd.set_option('display.max_colwidth', -1)
    # # print(df.sort_values(by='score', ascending=False).head(n=5))
    # # print(df.sort_values(by='score', ascending=False).tail(n=5))

    # # # -------- Rate generated sentence --------
    # # # score = bigram_matrix.rate_sentence(join, corpus)  # tokenize, rate sentence 
    # # # FIXME The bigram matrix module does too much. Should just operate on token alone.
    # # # FIXME use CoreNLP tokenization throughout

    # # # print(' '.join(sent), score, '\n')
    # # # print(' '.join(sent))

    # # # tokens = tokenize(url, text)
    # # # bigram_corp = [tup[0] + tup[1] for tup in zip(tokens, tokens[1:])]
    # # # bigram_samp = list(zip(sent, sent[1:]))

    # # # print('bigram_corp', bigram_corp)
    # # # print('bigram_samp', bigram_samp)

    # # # -------- Cosine Similarity --------
    # # univec = CountVectorizer(ngram_range=(1,1), token_pattern=r'(?u)\b\w+\b')
    # # bivec = CountVectorizer(ngram_range=(2,2), token_pattern=r'(?u)\b\w+\b')
    # # trivec = CountVectorizer(ngram_range=(3,3), token_pattern=r'(?u)\b\w+\b')
    # # quadvec = CountVectorizer(ngram_range=(4,4), token_pattern=r'(?u)\b\w+\b')

    # # # Create list of sentences
    # # corp = [text]
    # # for sent in out:
    # #     corp.append(sent)

    # # X1 = univec.fit_transform(corp)
    # # X2 = bivec.fit_transform(corp)
    # # X3 = trivec.fit_transform(corp)
    # # X4 = quadvec.fit_transform(corp)

    # # # Cosine Similarity: compare corpus to all
    # # score1 = cosine_similarity(X1[0], X1[1:])
    # # df1 = pd.DataFrame({'text': out, 'score': score1[0]})

    # # score2 = cosine_similarity(X2[0], X2[1:])
    # # df2 = pd.DataFrame({'text': out, 'score': score2[0]})

    # # score3 = cosine_similarity(X3[0], X3[1:])
    # # df3 = pd.DataFrame({'text': out, 'score': score3[0]})

    # # score4 = cosine_similarity(X4[0], X4[1:])
    # # df4 = pd.DataFrame({'text': out, 'score': score4[0]})

    # # # Pandas Display options
    # # pd.set_option('display.max_colwidth', -1)
    # # pd.set_option('display.max_columns', None)

    # # # Top results
    # # print('unigram', df1.nlargest(10, 'score'), '\n')
    # # print('unigram', df1.nsmallest(10, 'score'), '\n')

    # # print('bigram', df2.nlargest(10, 'score'), '\n')
    # # print('bigram', df2.nsmallest(10, 'score'), '\n')

    # # print('trigram', df3.nlargest(10, 'score'), '\n')
    # # print('trigram', df3.nsmallest(10, 'score'), '\n')

    # # print('quadrigram', df4.nlargest(10, 'score'), '\n')
    # # print('quadrigram', df4.nsmallest(10, 'score'), '\n')

