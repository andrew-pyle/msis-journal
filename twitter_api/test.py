#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  2 13:38:56 2017

@author: asp
"""

import twitter
import pickle

api = twitter.Api(consumer_key='***REMOVED***',
                  consumer_secret='***REMOVED***',
                  access_token_key='***REMOVED***',
                  access_token_secret='***REMOVED***')

trump = 'realDonaldTrump'

def get_timeline_page(screen_name, max_id):
    statuses = api.GetUserTimeline(screen_name=screen_name, count=200, trim_user=True, max_id=max_id)
    return statuses


# %%

# Initialize trump_tweets list with max_id=None
trump_tweets = api.GetUserTimeline(screen_name='realDonaldTrump', count=200, trim_user=True)

# get 2000 tweets
for x in range(20):
    new_max_id = trump_tweets[len(trump_tweets) - 1].id
    trump_tweets += get_timeline_page(trump, new_max_id)

# %%
    
with open('trump_tweets.pkl', 'wb') as f:
    pickle.dump(trump_tweets, f)
    
# %%
tpkl = open('trump_tweets.pkl', 'rb')
tt = pickle.load(tpkl)
tpkl.close()

# %%

for x in range(5):
    new_statuses = api.GetUserTimeline(screen_name='realDonaldTrump', count=5, trim_user=True, max_id = new_max_id)
    for i in new_statuses:
        statuses.append(i)
    new_max_id = statuses[len(statuses) - 1].id
    

# %%
counter = 0
for s in statuses:
    counter += 1
    print(str(counter) + ':', s.text, end='\n\n')
# %%
print(statuses[0].id, statuses[0].text, end='\n\n')
print(statuses[1].id, statuses[1].text, end='\n\n')
print(statuses[len(statuses)-1].id, statuses[len(statuses)-1].text)
print('No. of tweets: ', len(statuses))
