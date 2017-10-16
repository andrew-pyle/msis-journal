---
layout: post
title:  "spaCy Testing"
date:   2017-10-15 23:00:00 -0500
categories: journal
---

*I had a death in my immediate family last week, so I don't have much to write here for now.*

## Twitter API Cont'd.
I created a python function which will fetch the newest tweets from [@realDonaldTrump](https://twitter.com/realDonaldTrump) and create a [.pkl file](https://docs.python.org/3/library/pickle.html) of the Twitter API data structure, which has been translated to a python list of dictionaries. It assumes that the number of tweets posted since the last download is under the Twitter API max (200 tweets/request).

```python
import pickle
from datetime import date

def update_tpkl(tpkl_url, screen_name):

    with open(tpkl_url, 'rb') as tpkl:
        tt = pickle.load(tpkl)
    latest_id = tt[0].id
    new_tweets = api.GetUserTimeline(screen_name=screen_name, trim_user=True,
                                     since_id=latest_id, count=200)
    new_tweets += tt    

    with open('trump_tweets_{}.pkl'.format(str(date.today())), 'wb') as f:
        pickle.dump(new_tweets, f)
```

I intend to set this up to run regularly, giving me access to Trump's tweets as they are posted. I could set up a cron job on my MacBook, but there is surely a more elegant way to do that. I could also use a free account on [pythonanywhere.com](https://www.pythonanywhere.com), and sync the data through GitHub. We will see.

## spaCy Testing
As it turns out, the standard spaCy document import pipeline automatically tags each document with part-of-speech (POS) and syntactic dependencies. The basic POS labels are described [in the documentation](https://spacy.io/docs/usage/pos-tagging).

```python
import spacy
import pickle
import html

nlp = spacy.load('en')
with open('trump_tweets_2017-10-15.pkl', 'rb') as tpkl:
    tt = pickle.load(tpkl)

# revert html escaped characters in tweet text: '&amp;' -> '&'
tweets = [html.unescape(tw.text) for tw in tt]
doc = nlp(tweets[0])  # first tweet

# prints word, lemma int representation, lemma (string)
for word in doc:
    print(word.text, word.lemma, word.lemma_)

# prints word, syntactic arc (string), syntactic arc (int)
for word in doc:
    print(word.text, word.dep_, word.dep)
```
The newest challenge is Trump's tendency to issue multiple tweets which make a single thought, or document in NLP terms. Matching them together would reconstitute the thought, but would wreck the tweet structure I am trying to characterize. Keeping them separate would also wreck the completeness of the pattern that could be captured.

I may have to remove all the double tweet documents. 
