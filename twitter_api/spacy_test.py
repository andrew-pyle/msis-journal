#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 19:31:12 2017

@author: asp
"""

import spacy
import pickle
import html

nlp = spacy.load('en')

with open('trump_tweets_2017-10-15.pkl', 'rb') as tpkl:
        tt = pickle.load(tpkl)

tweets = [html.unescape(tw.text) for tw in tt]

doc = nlp(tweets[0])

for word in doc:
    print(word.text, word.lemma, word.lemma_)
    
for word in doc:
    print(word.text, word.dep_, word.dep)
    
'''
x html unescape done. 
x spacy tags and parses automatically
- ... ... tweet pairs -> resolve 

'''