import tweepy
from decouple import config
from random_word import RandomWords


#API token ( Elevated access required)
auth = tweepy.OAuthHandler(config('CONSUMER_API_KEY'),config('CONSUMER_API_SECRET'))
auth.set_access_token(config('ACCESS_TOKEN'),config('ACCESS_TOKEN_SECRET'))

#connection
api = tweepy.API(auth)

#try if the api works
try:
    api.verify_credentials()
    print("everything works")
except:
    print("Something went wrong")

#function to create and send a tweet
def CreateTweet():
    r = RandomWords()
    word= r.get_random_word()
    api.update_status("Life is "+ word)

CreateTweet()





