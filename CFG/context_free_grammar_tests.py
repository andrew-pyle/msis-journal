# -*- coding: utf-8 -*-
"""
Created on Tue Feb 20 10:30:44 2018

@author: asp
"""
import pprint
from collections import defaultdict
from stanfordcorenlp import StanfordCoreNLP
from nltk import Tree, Nonterminal

import context_free_grammar


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

    text = ('The top Leadership and Investigators '
    'of the FBI and the Justice Department have politicized the sacred inves'
    'tigative process in favor of Democrats and against Republicans - someth'
    'ing which would have been unthinkable just a short time ago? Rank & Fil'
    'e are great people!')

    rules = nlp.parse(text)
    tree = Tree.fromstring(rules)

    cfg = context_free_grammar.CFG()
    cfg.add_nltk_tree(tree)

    print(cfg.productions)

    generation_suite(cfg)
    
def stanford_with_nonterminal():
    # nlp = StanfordCoreNLP(r'/Users/asp/stanford-corenlp-full-2017-06-09')
    nlp = StanfordCoreNLP('http://localhost', port=9000)

    text = ('The top Leadership and Investigators '
    'of the FBI and the Justice Department have politicized the sacred inves'
    'tigative process in favor of Democrats and against Republicans - someth'
    'ing which would have been unthinkable just a short time ago. Rank & Fil'
    'e are great people!')

    rules = nlp.parse(text)
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


# simple_grammar()
simple_stanford_parser()
# stanford_with_nonterminal()

# nonterminal named identically to terminal causes infinite expansion until
# p < Random.choice epsilon, so it's zero
