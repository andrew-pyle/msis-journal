#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 15:36:56 2017

@author: asp
"""

import twitter
import pickle
from tw_api import set_api

token = set_api()

api = twitter.Api(consumer_key=token['consumer_key'],
                  consumer_secret=token['consumer_secret'],
                  access_token_key=token['access_token_key'],
                  access_token_secret=token['access_token_secret'])

trump = 'realDonaldTrump'

def get_timeline_page(screen_name, max_id):
    statuses = api.GetUserTimeline(screen_name=screen_name, count=200, trim_user=True, max_id=max_id)
    return statuses


# Initialize trump_tweets list with max_id=None
trump_tweets = api.GetUserTimeline(screen_name='realDonaldTrump', count=200, trim_user=True)

# get 2000 tweets
for x in range(20):
    new_max_id = trump_tweets[len(trump_tweets) - 1].id
    trump_tweets += get_timeline_page(trump, new_max_id)


with open('trump_tweets.pkl', 'wb') as f:
    pickle.dump(trump_tweets, f)


tpkl = open('trump_tweets.pkl', 'rb')
tt = pickle.load(tpkl)
tpkl.close()
