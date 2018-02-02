---
layout: post
title: "Implementation Phase"
date: 2018-02-01 15:00:00 -0600
categories: journal
---
Spring 2018 will be the implementation period for this M.S. Project. To recap, I'll be developing a text generation system based on a [Context-Free Grammar (CFG)]({{ site.baseurl }}{% post_url 2017-10-30-Proposal %}), generated from a publicly available corpus of tweets.

## System Components
1. Twitter API Interface – download tweet corpus
1. Constituency Parser – [Stanford CoreNLP](https://stanfordnlp.github.io/CoreNLP/) will probably do the trick.
1. CFG Production Generator – This creates "rules" for legal speech
1. Quasi-Random Sentence Generator – Create sentences
1. Markov Probability Function – Make sure the tweet sounds like the corpus

## Issues
1. The [Stanford CoreNLP](https://stanfordnlp.github.io/CoreNLP/) library can do constituency parsing, but it's written in Java, so it'll have to be interfaced with Python.
1. Since productions in a CFG can be defined recursively, I'll need to write an algorithm to ensure we exit the Generator.
1. The Markov probability function will need tuning. A machine learning classifier will be investigated if time permits.

I'll be starting with finding a constituency parser and going down the list. The Twitter API interface should be straight forward, so that'll be last.
