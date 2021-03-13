#importing all dependencies
# https://iq.opengenus.org/tweet-using-twitter-api/
import numpy as np
import tweepy

#variables for accessing twitter API
consumer_key='cgReTPkGOAhmxp04YE4QKGAxS'
consumer_secret_key='a22Q7vsFDUdGsHyftqviioDt5puUt60jHjgilwo8z1KEF7uplD'
access_token='1369215911002013696-OXXb0eTXGxryx38IEm0XRncsdtlm1C'
access_token_secret='9Hlw5RA0PqyzsejKw6G6NYldyhwEdNZzJnvqpbBmL6cFn'


auth=tweepy.OAuthHandler(consumer_key,consumer_secret_key)
auth.set_access_token(access_token,access_token_secret)
api=tweepy.API(auth)

# list = api.home_timeline(1)
# print(list)

# tweet=input('enter the tweet')
#Generate text tweet
api.update_status("Why buy this car? Checkout this https://suggestrank.com/compare/cars/2907/Toyota-Auris-2007-vs-Toyota-Highlander-2007-vs-Toyota-RunX-2007")

# tweet_text=input('enter the tweet ')
# image_path =input('enter the path of the image ')

#Generate text tweet with media (image)
# status = api.update_with_media(image_path, tweet_text)
# api.update_status(tweet_media)