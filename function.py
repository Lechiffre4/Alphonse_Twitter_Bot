import tweepy
from decouple import config
from random_word import RandomWords
import hashtaglist
import random
import json
import geocoder
from textblob import TextBlob
import re




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

def getTextinTrend(trend_name):
    tweettext = []
    tweets = tweepy.Cursor(api.search_tweets,
              q=trend_name,
              lang="en").items(250)

    for tweet in tweets:
        result = re.sub(r"http\S+", "", tweet.text)
        tweettext.append(result)

    tweettext = "".join(tweettext)
    return tweettext


def getSentimentFromHashtags(hashtag):
    text = getTextinTrend(hashtag)
    print(text)
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity # value between -1 and 1
    print(hashtag+": "+ str(sentiment))
    return sentiment

def interpretPolarity(polarity):
    sentiment = None
    if(polarity>=0.6):
        print("peace")
    elif(polarity<=0.5 and polarity>0.4):
        print("happy conversations")
    elif(polarity<=0.4 and polarity>0.3):
        print("normal conversation")
    elif(polarity<=0.3 and polarity>0.2):
        print("became titled")
    elif(polarity<=0.2 and polarity>0.1):
        print("titled")
    elif(polarity<=0.1 and polarity>0):
        print("dangerous")
    elif(polarity<=0 and polarity> -0.1):
        print("hardcore")
    elif(polarity<= -0.1 and polarity> -0.4):
        print("cursed topic")
    elif(polarity<= -0.4):
        print("anarchy")

interpretPolarity(getSentimentFromHashtags("#blm"))


    
