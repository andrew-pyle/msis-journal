# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 10:30:44 2018

@author: asp
"""
import pprint
from collections import defaultdict
from stanfordcorenlp import StanfordCoreNLP
from nltk import Tree, Nonterminal

import json
import requests
import pickle
import pandas as pd

import context_free_grammar
import bigram_matrix


text1 = '''The top Leadership and Investigators of the FBI and the Justice Department have politicized the sacred investigative process in favor of Democrats and against Republicans - something which would have been unthinkable just a short time ago? Rank & File are great people!'''

text2 = '''The top Leadership and Investigators of the FBI and the Justice Department have politicized the sacred investigative process in favor of Democrats and against Republicans - something which would have been unthinkable just a short time ago. Rank & File are great people!'''

text3 = '''Whether we are Republican or Democrat, we must now focus on strengthening Background Checks!'''

text4 = '''Republicans are now leading the Generic Poll, perhaps because of the popular Tax Cuts which the Dems want to take away. Actually, they want to raise you taxes, substantially. Also, they want to do nothing on DACA, R’s want to fix! The U.S. economy is looking very good, in my opinion, even better than anticipated. Companies are pouring back into our country, reversing the long term trend of leaving. The unemployment numbers are looking great, and Regulations & Taxes have been massively Cut! JOBS, JOBS, JOBS'''


def simple_grammar():
    cfg = context_free_grammar.CFG()
    cfg.add_production('S', 'S VP')
    cfg.add_production('S', 'NP VP')
    # cfg.add_production('S', 'NP')
    # cfg.add_production('S', 'VP')
    cfg.add_production('NP', 'I')
    cfg.add_production('VP', 'V ADJ')
    cfg.add_production('VP', 'V')
    cfg.add_production('V', 'am | are | run | play')
    cfg.add_production('ADJ', 'blue')
    cfg.add_production('ADJ', 'green')

    print(cfg.productions)

    generation_suite(cfg)


def simple_stanford_parser():
    """
    $ cd /Users/asp/stanford-corenlp-full-2017-06-09
    $ java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port
      9000 -timeout 15000

    Starts the Stanford CoreNLP Server with all JAR files, including the Shift-Rediuce parser: stanford-srparser-2014-10-23-models.jar
    """

    # nlp = StanfordCoreNLP(r'/Users/asp/stanford-corenlp-full-2017-06-09')
    nlp = StanfordCoreNLP('http://localhost', port=9000)

    rules = nlp.parse(text1)
    tree = Tree.fromstring(rules)

    cfg = context_free_grammar.CFG()
    cfg.add_nltk_tree(tree)

    print(cfg.productions)

    generation_suite(cfg)

def stanford_with_nonterminal():
    # nlp = StanfordCoreNLP(r'/Users/asp/stanford-corenlp-full-2017-06-09')
    nlp = StanfordCoreNLP('http://localhost', port=9000)

    rules = nlp.parse(text1)
    tree = Tree.fromstring(rules)
    struct_rules = [(rule.lhs(), rule.rhs()) for rule in tree.productions()]
    d = defaultdict(list)
    for rule in struct_rules:
        if rule[1] not in d[rule[0]]:
            d[rule[0]].append(rule[1])

    cfg = context_free_grammar.CFG()
    cfg.productions = d

    print(cfg.productions)
    nonterm_generation_suite(cfg)

def generation_suite(cfg):
    # Data
    symbols = []
    expansions = defaultdict(list)

    # Run tests
    # TODO expand all nonterminals
    for x in range(5):
        expansions['ROOT'].append(cfg.expand('ROOT'))

    # Print results
    print('Symbols in cfg:\n')
    pprint.pprint(cfg.productions.keys())
    print('\nExpansions:\n')

    for symbol in expansions:
        if symbol == 'S':
            print('Root:', symbol, '\n')
        else:
            print('Nonroot:', symbol)
        pprint.pprint(expansions[symbol])
        print('\n')

def nonterm_generation_suite(cfg):
    # Data
    expansions = defaultdict(list)

    # Run tests
    # TODO expand all nonterminals
    for x in range(5):
        expansions[Nonterminal('ROOT')].append(
            cfg.nltk_expand(Nonterminal('ROOT')))

    # Print results
    print('Symbols in cfg:\n')
    pprint.pprint(cfg.productions.keys())
    print('\nExpansions:\n')

    for symbol in expansions:
        if symbol == 'S':
            print('Root:', symbol, '\n')
        else:
            print('Nonroot:', symbol)
        pprint.pprint(expansions[symbol])
        print('\n')

def pickle_multi_sent():
    with open('/Users/asp/GitHub/msis-project/twitter_api/trump_tweets.pkl', 'rb') as tpkl:
        tt = pickle.load(tpkl)

    tweets = [status.text for status in tt]
    text = ' '.join(tweets).replace('\n', ' ')  # remove stray newlines
    sample = ' '.join(tweets[:10]).replace('\n', ' ')

    print(sample)
    corpus = bigram_matrix.Corpus(text)


    url = 'http://localhost:9000'
    cfg = context_free_grammar.CFG()

    sents = constituency_parse(url, sample)
    for sent in sents:
        tree = Tree.fromstring(sent)
        struct_rules = [(rule.lhs(), rule.rhs()) for rule in tree.productions()]
        #d = defaultdict(list)
        for rule in struct_rules:
            if rule[1] not in cfg.productions[rule[0]]:
                cfg.productions[rule[0]].append(rule[1])
        # cfg.productions.update(d)

    print(cfg.productions, '\n\n')
    out = {'sentence': [], 'score': []}

    for x in range(100):
        txt = cfg.nltk_expand(Nonterminal('ROOT'))
        if len(txt) < 20:
            line = ' '.join(txt)
            out['sentence'].append(line)
            out['score'].append(bigram_matrix.rate_sentence(line, corpus))

    df = pd.DataFrame(data=out)
    pd.set_option('display.max_colwidth', -1)
    print(df.sort_values(by='score', ascending=False).head(n=5))


    #nonterm_generation_suite(cfg)

def constituency_parse(url, text):
    data = text.encode('utf-8')
    properties = {'annotators': 'pos,parse', 'outputFormat': 'json'}
    params = {'properties': str(properties), 'pipelineLanguage': 'en'}

    r = requests.post(url, params=params, data=data, headers={'Connection': 'close'})
    r_dict = json.loads(r.text)

    return [sent['parse'] for sent in r_dict['sentences']]


# simple_grammar()
# simple_stanford_parser()
# stanford_with_nonterminal()

text = ''
pickle_multi_sent()
