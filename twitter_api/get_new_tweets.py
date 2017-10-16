import pickle
from datetime import date

import twitter
from tw_api import set_api

token = set_api()

api = twitter.Api(consumer_key=token['consumer_key'],
                  consumer_secret=token['consumer_secret'],
                  access_token_key=token['access_token_key'],
                  access_token_secret=token['access_token_secret'])


def update_tpkl(tpkl_url, screen_name):
    
    with open(tpkl_url, 'rb') as tpkl:
        tt = pickle.load(tpkl)
    latest_id = tt[0].id
    new_tweets = api.GetUserTimeline(screen_name=screen_name, trim_user=True, 
                                     since_id=latest_id, count=200)
    new_tweets += tt    
    
    with open('trump_tweets_{}.pkl'.format(str(date.today())), 'wb') as f:
        pickle.dump(new_tweets, f)