import tweepy
from decouple import config
from random_word import RandomWords
import openai
import function


#API token ( Elevated access required)
auth = tweepy.OAuthHandler(config('CONSUMER_API_KEY'),config('CONSUMER_API_SECRET'))
auth.set_access_token(config('ACCESS_TOKEN'),config('ACCESS_TOKEN_SECRET'))

#connection
api = tweepy.API(auth)

connectResult = "error"
#try if the api works
while (connectResult == "error"):
    try:
        api.verify_credentials()
        connectResult = "ok"
        print("Connection works")

    except:
        connectResult = "error"


result="tweet error"
while (result == "tweet error"):
    try:
        function.CreateTweet(function.gpt3())
        result = "tweet ok"
        print("tweet sent!")

    except:
        result = "tweet error"










