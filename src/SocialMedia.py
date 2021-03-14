import psycopg2
import json
from string import Template
from random import randrange
import yaml
import urllib
import urllib.parse
import tweepy
import requests
from datetime import datetime
import logging
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
    with open(r'secret.yaml') as file:
        secrets = yaml.full_load(file)


        consumer_key = secrets['twitter']['consumer_key']
        consumer_secret_key = secrets['twitter']['consumer_secret_key']
        access_token = secrets['twitter']['access_token']
        access_token_secret = secrets['twitter']['access_token_secret']
        fbAccessToken = secrets['facebook']['access_token']


        dataList = getData()
        print(dataList)
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
                witterResponseStatus = api.update_status(twitterStatus)
                logging.info("Twitter status: "+str(witterResponseStatus))
                # print(str(twitterStatus))
            else:
                fbUrl = 'https://graph.facebook.com/v10.0/104277171736451/feed?message='+urllib.parse.quote(title)+' '+urllib.parse.quote(hashTags)+'&link='+url+'&access_token='+fbAccessToken
                print(fbUrl)
                response = requests.post(fbUrl)
                # print(response.json())
                logging.info('Facebook Status: '+str(response.json()))

if __name__ == "__main__":
    main()