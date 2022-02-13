import tweepy
from decouple import config
from random_word import RandomWords
import openai


#API token ( Elevated access required)
auth = tweepy.OAuthHandler(config('CONSUMER_API_KEY'),config('CONSUMER_API_SECRET'))
auth.set_access_token(config('ACCESS_TOKEN'),config('ACCESS_TOKEN_SECRET'))

#connection
api = tweepy.API(auth)




#function to create and send a tweet
def CreateRandomTweet():
    r = RandomWords()
    word= r.get_random_word()
    api.update_status("Life is "+ word)


def CreateTweet(text):
    api.update_status(text)


def gpt3():
    openai.api_key = config("GPT_KEY")
    response = openai.Completion.create(
        engine="davinci",
        prompt= "tweet something cool about tecchnology #technology",
        max_tokens = 50
    )
    content = response.choices[0].text
    return content