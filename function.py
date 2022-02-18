import tweepy
from decouple import config
from random_word import RandomWords
import hashtaglist
import random
import json
import geocoder
from textblob import TextBlob
import re
import time




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
              lang="en").items(100)

    for tweet in tweets:
        result = re.sub(r"http\S+", "", tweet.text)
        tweettext.append(result)

    tweettext = "".join(tweettext)
    return tweettext


def getSentimentFromHashtags(hashtag):
    text = getTextinTrend(hashtag)
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity # value between -1 and 1
    print(hashtag+": "+ str(sentiment))
    return sentiment

def interpretPolarity(polarity):
    sentiment = None
    if(polarity == 0):
        print("Rien à signaler sur le hashtag")
        sentiment = "null"
    elif(polarity>=0.5):
        print("peace")
        sentiment = "peace"
    elif(polarity<=0.5 and polarity>0.4):
        print("happy conversations")
        sentiment = "happy"
    elif(polarity<=0.4 and polarity>0.3):
        print("normal conversation")
        sentiment = "normal"
    elif(polarity<=0.3 and polarity>0.2):
        print("became tilted")
        sentiment = "tense"
    elif(polarity<=0.2 and polarity>0.1):
        print("tilted")
        sentiment = "tilted"
    elif(polarity<=0.1 and polarity>0):
        print("dangerous")
        sentiment = "dangerous"
    elif(polarity<=0 and polarity> -0.1):
        print("hardcore")
        sentiment = "hard"
    elif(polarity<= -0.1 and polarity> -0.4):
        print("cursed topic")
        sentiment = "cursed"
    elif(polarity<= -0.4):
        print("anarchy")
        sentiment = "anarchy"
    return sentiment

def extract_hash_tags(s):
    return set(part[1:] for part in s.split() if part.startswith('#'))

def reply():
    bot_id = int(api.verify_credentials().id_str)
    mention_id = 1

    message = "Here I am"
    while True:
        mentions = api.mentions_timeline(since_id=mention_id)
        for mention in mentions:
            print("Mention Tweet Found!")
            print(f"{mention.author.screen_name} - {mention.text}")
            mention_id = mention.id
            targeted_hashtag = extract_hash_tags(mention.text)
            if (len(targeted_hashtag)>1):
                targeted_hashtag = targeted_hashtag[0]
            
            #check if the the tweet contain hashtag
            getSentimentFromHashtags(targeted_hashtag)


            if mention.in_reply_to_status_id is None and mention.author.id != bot_id:
                try:
                    print("Attempting Reply...")
                    api.update_status(message.format(mention.author.screen_name), in_reply_to_status_id=mention.id_str)
                    print("Successfully replies :")
                except Exception as e:
                    print(e)

        time.sleep(15)

reply()






    
