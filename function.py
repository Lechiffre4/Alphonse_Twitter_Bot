import tweepy
from decouple import config
from random_word import RandomWords
import hashtaglist
import random
import json
import geocoder
from datetime import datetime, timedelta


#API token ( Elevated access required)
auth = tweepy.OAuthHandler(config('CONSUMER_API_KEY'),config('CONSUMER_API_SECRET'))
auth.set_access_token(config('ACCESS_TOKEN'),config('ACCESS_TOKEN_SECRET'))

#connection
api = tweepy.API(auth)



#function to create and send a tweet
def CreateRandomTweet():
    r = RandomWords()
    word= r.get_random_word()
    firsthash = hashtaglist.hashtags[random.randint(0,len(hashtaglist.hashtags))]
    secondhash = hashtaglist.hashtags[random.randint(0,len(hashtaglist.hashtags))]
    while(firsthash == secondhash):
        secondhash = hashtaglist.hashtags[random.randint(0,len(hashtaglist.hashtags))]
    api.update_status("Life is "+ word+ "  "+firsthash+" "+ secondhash)


def CreateTweet(text):
    api.update_status(text)

def getAllTrends():
    geo = "France"
    hashtags_trend = []
    geo = geocoder.osm(geo)

    closest_loc = api.closest_trends(geo.lat, geo.lng)
    trends = api.get_place_trends(closest_loc[0]["woeid"])
    trends = trends[0]
    trends = trends["trends"]

    for trend in trends:
        hashtags_trend.append(trend["name"])


    return hashtags_trend

def yesterday(string=False, frmt='%Y-%m-%d'):
    yesterday = datetime.now() - timedelta(1)
    if string:
        return yesterday.strftime(frmt)
    return yesterday

def getTextinTrend(trend_name):

    tweets = tweepy.Cursor(api.search_tweets,
              q=trend_name,
              lang="en").items(5)

    for tweet in tweets:
        print(tweet.text)
    return tweets
