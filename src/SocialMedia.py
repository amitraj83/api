import psycopg2
import json
from string import Template
from random import randrange
import os
import yaml
import urllib
import urllib.parse
import tweepy
import requests
import random
from datetime import datetime
import logging
import praw
from praw.models import InlineGif, InlineImage, InlineVideo

logging.basicConfig(filename='/var/log/social.log',  format='%(asctime)s %(message)s', level=logging.INFO)

titles = ["Checkout why $rank1car is better than $rank2car",
"These 5 reasons you should know before buying $rank1car,",
"Do not compare but rank cars to find why $rank1car is better.",
"Comparison is dumb, Ranking is smart. Check the rank of $rank1car, $rank2car and $rank3car",
"Did you do mistake buying $rank3car",
"10 criteria to rank and find best car among $rank1car, $rank2car and $rank3car",
"Check full specs and compare before buying $rank1car",
"$rank1car prices, full specs, equipment, review, sale price, interiors, review, engine, and images",
"I was amazed when I saw $rank1car is better than $rank2car and $rank3car",
"Do you know these 10 facts about  $rank1car ",
"Compare and Rank $rank1car, $rank2car and $rank3car",
"Checkout why $rank1car is better than $rank2car and $rank3car"
]

numberList = [1,2,3,4,5]

subreddits = ["u_suggestrank", "carporn",  "car"]
#cars does not allow the image posting. We should only post questions.

reddit = praw.Reddit(
    client_id="utcpaWWt5u9GFg",
    client_secret="OT3bMDBS0O_nnZ_4NCzcOhczgTUOIg",
    password="D15@Glaway",
    user_agent="SuggestRank by u/suggestrank",
    username="suggestrank",
)

tweetMessages = ["What do you think about this car. Please like it and follow me.", "See this cool car. Please like it, retweet and follow me.", "If you did not see this, you did not see anything. Please like it, retweet and follow me.", "This is cool. Isn't? Please like it, retweet and follow me.", "Did you like this car? Please retweet and follow me.", "Don't click on this pic. it will blow your mind. ", "This is one of my favourites. Please like it, retweet and follow me.", "This is a rare pic. Please like it and follow me. "]
redditMessages = ["My favourite toy is this one - $modelName", "I don't have money to buy this car $modelName. Do you have money to afford it?", "This used to be my favourite car - $modelName", "Today I spotted this $modelName.", "Check out this beautiful $modelName.", "Do you like this $modelName ?", "See this amazing beauty. Do you like this $modelName ?", "Can you tell me why should I buy this $modelName ?", "Please suggest why this $modelName a good car?", "$modelName - This is a cool car. Check this out. ", "What do you think about the engine size of this $modelName ?", "$modelName - More and small cylinders gives better power and smooth drive. Do you agree?", "$modelName - Big engine is not always good, more cylinders are preferred. Am I correct?", "Is this your dream $modelName ?", "Do you own this $modelName ?"]

def getImageUrl(cid):
    connection = psycopg2.connect(user="postgres", password="postgres", host="127.0.0.1", port="5432",
                                  database="daft")
    try:
        cursor = connection.cursor()
        sqlQuery = " select image from cars.car where model_id = "+str(cid)+" LIMIT 1 "
        cursor.execute(sqlQuery)
        records = cursor.fetchall()
        for row in records:
            return row[0]
    except (Exception, psycopg2.Error) as error:
        print("Error reading data from MySQL table", error)
    finally:
        if (connection):
            connection.commit()
            cursor.close()
            connection.close()


def getData():
    connection = psycopg2.connect(user="postgres", password="postgres", host="127.0.0.1", port="5432",
                                  database="daft")
    data = []
    try:
        cursor = connection.cursor()
        sqlQuery = " select url, page_title, response from cars.car_links where page_title != ''  and response::text != '' order by random() LIMIT 2 "
        cursor.execute(sqlQuery)
        records = cursor.fetchall()
        for row in records:
            listOfCarsRanks = []
            listOfCarsRanks.append({"image":getImageUrl(row[2]['model_id']['0']), "carName":row[2]['model_make_display']['0']+" "+row[2]['model_name']['0']+" "+str(row[2]['model_year']['0']), "rank":row[2]['rnk_consolidate_final']['0']})
            listOfCarsRanks.append({"image":getImageUrl(row[2]['model_id']['1']), "carName":row[2]['model_make_display']['1']+" "+row[2]['model_name']['1']+" "+str(row[2]['model_year']['1']), "rank":row[2]['rnk_consolidate_final']['1']})
            listOfCarsRanks.append({"image":getImageUrl(row[2]['model_id']['2']), "carName":row[2]['model_make_display']['2']+" "+row[2]['model_name']['2']+" "+str(row[2]['model_year']['2']), "rank":row[2]['rnk_consolidate_final']['2']})
            # listOfCarsRanks.sort(key='rank', reverse=True)
            sortedList = sorted(listOfCarsRanks, key=lambda x : x['rank'], reverse=False)
            shortlistedTitle = titles[randrange(len(titles))]
            title = Template(shortlistedTitle)\
                .substitute(rank1car=sortedList.__getitem__(0)['carName'], rank2car=sortedList.__getitem__(1)['carName'], rank3car=sortedList.__getitem__(2)['carName'])
            data.append({"title":title, "url":"https://suggestrank.com"+str(urllib.parse.quote(row[0])), "carNames":row[2]['model_make_display']['0'] +" " + row[2]['model_make_display']['1'] +" "+row[2]['model_make_display']['2']})

            #
        return data
    except (Exception, psycopg2.Error) as error:
        print("Error reading data : ", error)
    finally:
        if (connection):
            connection.commit()
            cursor.close()
            connection.close()

def main():
    with open(r'/root/car-compare/api/src/secret.yaml') as file:
        secrets = yaml.full_load(file)


        consumer_key = secrets['twitter']['consumer_key']
        consumer_secret_key = secrets['twitter']['consumer_secret_key']
        access_token = secrets['twitter']['access_token']
        access_token_secret = secrets['twitter']['access_token_secret']
        fbAccessToken = secrets['facebook']['access_token']

        randomImageFile = random.choice(os.listdir("/root/images-for-twitter"))
        spllittedName = randomImageFile.split("$$")
        # if len(spllittedName) > 1:
        #     randomMessage = random.choice(redditMessages)
        #     modelName = spllittedName[0]
        #     newMessage = Template(randomMessage).substitute(modelName=modelName)
        #     randomSubReddit = random.choice(subreddits)
        #     print("Reddit posted to : " + randomSubReddit)
        #     reddit.subreddit(randomSubReddit).submit_image(newMessage,
        #                                                image_path=os.path.join("/root/images-for-twitter",randomImageFile ))



        dataList = getData()
        for i in range(len(dataList)):
            data = dataList[i]
            title = data['title']
            url = data['url']
            carNames = data['carNames']
            hashTagSet = set()
            for word in carNames.split():
                hashTagSet.add(word)
            hashTags = ""
            for hashTag in hashTagSet:
                hashTags += " #" + hashTag



            if i == 0:
                twitterStatus = title+" "+hashTags + " "+url

                auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
                auth.set_access_token(access_token, access_token_secret)
                api = tweepy.API(auth)
                randomSelect = random.choice(numberList)
                print(randomSelect)
                if (randomSelect == 2 or randomSelect == 3 or randomSelect == 4) and len(os.listdir("/root/images-for-twitter")) > 0:
                    randomFile = random.choice(os.listdir("/root/images-for-twitter"))
                    print(randomFile)
                    api.update_with_media(os.path.join("/root/images-for-twitter",randomFile ) , random.choice(tweetMessages) +" #cars #car #newcar")
                    os.remove(os.path.join("/root/images-for-twitter",randomFile ))
                else:
                    witterResponseStatus = api.update_status(twitterStatus)
                    logging.info("Twitter status: "+str(url))
                # print(str(twitterStatus))
            else:
                fbUrl = 'https://graph.facebook.com/v10.0/104277171736451/feed?message='+urllib.parse.quote(title)+' '+urllib.parse.quote(hashTags)+'&link='+url+'&access_token='+fbAccessToken
                response = requests.post(fbUrl)
                # print(response.json())
                logging.info('Facebook Status: '+str(response.json()))

if __name__ == "__main__":
    main()
