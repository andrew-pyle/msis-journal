---
layout: post
title:  "Twitter API and Parsing"
date:   2017-10-07 14:00:00 -0500
categories: journal
---

The last week began the process of exploratory analysis, to borrow a terms from the [machine learning](https://elitedatascience.com/exploratory-analysis) discipline. I learned a bit about the [Twitter API](https://developer.twitter.com/en/docs/tweets/timelines/overview) (actually more about a [python client](https://github.com/bear/python-twitter) for it), and started the parsing process. There are several types of parsing in NLP:
- Part of Speech tagging
- Syntactic Parsing
- Semantic Parsing

We can attempt to use all these methods to construct [slots]({{ site.baseurl }}{% post_url 2017-09-28-Jurafsky %}#task-oriented-dialog-agents) for a Tweet-generating dialog agent's frame.

## Twitter API with Python Clients
[`python-twitter`](https://github.com/bear/python-twitter) from GitHub user [bear](https://github.com/bear) is an Apache 2.0 licensed python client for communicating with the Twitter API. Another python client is [`tweepy`](https://github.com/tweepy/tweepy) from [tweepy](http://www.tweepy.org), which is MIT-licensed. Both of these clients seem to be good options for acquiring tweet data from Twitter's API programmatically.

Since, they seem to be equal, I will go with `python-twitter` unless something changes my mind. (Maybe the MIT license would be more attractive in a production or commercial system. I'll think on that).

### Twitter API Limits
Twitter exposes limited data through its API to standard users. My impression is that they do not maintain the infrastructure to provide more than a sampling of tweets to API users.

>However, Twitter does partner with other organizations to provide full-archive search for [Enterprise](https://developer.twitter.com/en/enterprise) users.

Basically, search is limited to a sample (undefined) of tweets for the past 7 days. Luckily for us, each user's tweet history is directly retrievable for the past 3,200 tweets, called the `user_timeline`. Response is JSON formatted, and temporal restrictions apply:
- Requests / 15-min window (user auth): 900
- Requests / 15-min window (app auth): 1500

I don't know how `python-twitter` handles the OAuth authentication, so I will need to check that out. The authentication process seems to be what determines the user/app auth status.  

[Twitter OAuth Docs](https://developer.twitter.com/en/docs/basics/authentication/overview/application-only) & [`python-twitter` Docs](https://python-twitter.readthedocs.io/en/latest/)

### Tweet Data
Using a simple script, I was able to download the 3,200 max tweets from [@realDonaldTrump](https://twitter.com/realDonaldTrump)'s `user_timeline` and [`pickle`](https://docs.python.org/3/library/pickle.html) them for later analysis.

```python
import twitter
import pickle

api = twitter.Api(consumer_key='XXXXX',
                  consumer_secret='XXXXX',
                  access_token_key='XXXXX',
                  access_token_secret='XXXXX')

trump = 'realDonaldTrump'

def get_timeline_page(screen_name, max_id):
    statuses = api.GetUserTimeline(screen_name=screen_name, count=200,
                                   trim_user=True, max_id=max_id)
    return statuses


# Initialize trump_tweets list with max_id=None
trump_tweets = api.GetUserTimeline(screen_name='realDonaldTrump',
                                   count=200, trim_user=True)

# get 2000 tweets
for x in range(20):
    new_max_id = trump_tweets[len(trump_tweets) - 1].id
    trump_tweets += get_timeline_page(trump, new_max_id)


with open('trump_tweets.pkl', 'wb') as f:
    pickle.dump(trump_tweets, f)


tpkl = open('trump_tweets.pkl', 'rb')
tt = pickle.load(tpkl)
tpkl.close()
```

## Parsing
There are two major python packages for NLP available to me: [Natural Language Toolkit (NLTK)](http://www.nltk.org/) and [spaCY](https://spacy.io/). Both of which have benefits. I will attempt to learn both and decide which serves my needs better.

### [NLTK](http://www.nltk.org/)
NLTK is primarily a pedagogical tool, from the [Natural Language Processing with Python](http://www.nltk.org/book/) textbook from Steven Bird, Ewan Klein, and Edward Loper, available online. The standard [Anaconda installation](https://docs.anaconda.com/) of Python 3 includes the `nltk` package, as well, so it is accessible.

### [spaCY](https://spacy.io/)
[spaCy](https://spacy.io/) is an open-source, commercially-focused python package from a former academic resarcher. It [seems to outperform the NLTK package](https://spacy.io/docs/api/), especially in syntactic parsing speed, so it might be a better fit.

Next up, learn the APIs and parse some tweets. (and read more....and more....)
