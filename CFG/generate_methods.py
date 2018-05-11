import random

import pandas as pd
from nltk import Nonterminal
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import preprocess
import bigram_matrix
import generate


def cfg_gen_sum(tweets_clean, cfg, corpus):

    # -------- CFG Generate & Sum Rank --------
    outs = {'sentence': [], 'score': []}

    for x in range(100):
        sent = cfg.nltk_expand(Nonterminal('ROOT'), alpha=0.01)
        if len(sent) < 25:
            line = ' '.join(sent)
            outs['sentence'].append(line)
            outs['score'].append(bigram_matrix.rate_sentence(line, corpus))

    # -------- Bigram Matrix Output --------
    df = pd.DataFrame(data=outs)
    pd.set_option('display.max_colwidth', -1)
    print(df.sort_values(by='score', ascending=False).head(n=5))
    print(df.sort_values(by='score', ascending=False).tail(n=5))


def cfg_gen_cos(tweets_clean, cfg):
    # -------- CFG Generate & Sum Rank --------
    out = []

    for x in range(100):
        sent = cfg.nltk_expand(Nonterminal('ROOT'), alpha=0.01)
        if len(sent) < 25:
            line = ' '.join(sent)
            out.append(line)

    # -------- Cosine Similarity --------
    univec = CountVectorizer(ngram_range=(1,1), token_pattern=r'(?u)\b\w+\b')
    bivec = CountVectorizer(ngram_range=(2,2), token_pattern=r'(?u)\b\w+\b')

    # Create list of sentences
    corp = [tweets_clean]
    for sent in out:
        corp.append(sent)

    X1 = univec.fit_transform(corp)
    X2 = bivec.fit_transform(corp)

    # Cosine Similarity: compare corpus to all
    score1 = cosine_similarity(X1[0], X1[1:])
    df1 = pd.DataFrame({'text': out, 'score': score1[0]})

    score2 = cosine_similarity(X2[0], X2[1:])
    df2 = pd.DataFrame({'text': out, 'score': score2[0]})

    # Pandas Display options
    pd.set_option('display.max_colwidth', -1)
    pd.set_option('display.max_columns', None)

    # Top results
    print('unigram', df1.nlargest(10, 'score'), '\n')
    print('unigram', df1.nsmallest(10, 'score'), '\n')

    print('bigram', df2.nlargest(10, 'score'), '\n')
    print('bigram', df2.nsmallest(10, 'score'), '\n')


def pos_gen_sum(bigram_corpus, sample_tweets, cfg, url):
    # -------- POS Tags --------
    train = random.choice(sample_tweets)  # select random tweet
    # train = tweets[index]  # training tweet
    # train = 'Military and economy are getting stronger by the day, and our enemies know it. #MAGA'  # test case
    train_clean = preprocess.preprocess(train)
    tags = generate.pos_tag(url, train)  # get POS tags
    print(train_clean)  # View Template text

    # -------- POS Generate & Sum Rank --------
    outs = {'sentence': [], 'score': []}
    
    for x in range(100):
        # Fill POS tag list with terminal symbols
        sent = generate.pos_bucket_generate(cfg, tags)  # list of terminal symbols
        line = ' '.join(sent)
        outs['sentence'].append(line)
        outs['score'].append(bigram_matrix.rate_sentence(line, bigram_corpus))

    out = outs['sentence']

    # -------- Bigram Matrix Output --------
    df = pd.DataFrame(data=outs)
    pd.set_option('display.max_colwidth', -1)
    print(df.sort_values(by='score', ascending=False).head(n=5))
    print(df.sort_values(by='score', ascending=False).tail(n=5))


def pos_gen_cos(tweets_clean, sample_tweets, cfg, url):
    # -------- POS Tags --------
    train = random.choice(sample_tweets)  # select random tweet
    # train = tweets[index]  # training tweet
    # train = 'Military and economy are getting stronger by the day, and our enemies know it. #MAGA'  # test case
    train_clean = preprocess.preprocess(train)
    tags = generate.pos_tag(url, train)  # get POS tags
    print(train_clean)  # View Template text

    # -------- POS Generate & Sum Rank --------
    outs = {'sentence': [], 'score': []}
    
    for x in range(100):
        # Fill POS tag list with terminal symbols
        sent = generate.pos_bucket_generate(cfg, tags)  # list of terminal symbols
        line = ' '.join(sent)
        outs['sentence'].append(line)

    out = outs['sentence']

     # -------- Cosine Similarity --------
    univec = CountVectorizer(ngram_range=(1,1), token_pattern=r'(?u)\b\w+\b')
    bivec = CountVectorizer(ngram_range=(2,2), token_pattern=r'(?u)\b\w+\b')

    # Create list of sentences
    corp = [tweets_clean]
    for sent in out:
        corp.append(sent)

    X1 = univec.fit_transform(corp)
    X2 = bivec.fit_transform(corp)

    # Cosine Similarity: compare corpus to all
    score1 = cosine_similarity(X1[0], X1[1:])
    df1 = pd.DataFrame({'text': out, 'score': score1[0]})

    score2 = cosine_similarity(X2[0], X2[1:])
    df2 = pd.DataFrame({'text': out, 'score': score2[0]})

    # Pandas Display options
    pd.set_option('display.max_colwidth', -1)
    pd.set_option('display.max_columns', None)

    # Top results
    print('unigram', df1.nlargest(10, 'score'), '\n')
    print('unigram', df1.nsmallest(10, 'score'), '\n')

    print('bigram', df2.nlargest(10, 'score'), '\n')
    print('bigram', df2.nsmallest(10, 'score'), '\n')
