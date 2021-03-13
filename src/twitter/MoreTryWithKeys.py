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

# for tweet in api.home_timeline(5):
#     print (tweet.text, tweet.id)

api.update_status("Think before selecting a Volkswagen? Checkout here \r\n #Volkswagen #compare #cars #comparecars. https://suggestrank.com/compare/cars/3271/Volkswagen-Jetta-2011-vs-Volkswagen-Caddy-2011-vs-Volkswagen-Jetta-2011")