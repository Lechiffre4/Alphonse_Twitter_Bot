import tweepy
from decouple import config
import openai


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


def CreateTweet(text):
    api.update_status(text)


def gpt3():
    openai.api_key = config("GPT_KEY")
    response = openai.Completion.create(
        engine="ada",
        prompt="tweet something cool #technology",
        max_tokens = 64
    )
    content = response.choices[0].text
    return content

CreateTweet(gpt3())





