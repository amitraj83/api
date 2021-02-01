import flask
from flask import request, jsonify
import psycopg2
import json
import datetime
import numpy as np
import pandas as pd

app = flask.Flask(__name__)
app.config["DEBUG"] = True


class Property:
    def __init__(self, url, price, bedSize, bathrooms, sqMeter, propertyType, description, ber, datePostedRenewed,
                 views, features, facilities):
        self.url = url
        self.price = price
        self.bedSize = bedSize
        self.bathrooms = bathrooms
        self.sqMeter = sqMeter
        self.propertyType = propertyType
        self.description = description
        self.ber = ber
        self.datePostedRenewed = ""#datetime.datetime.strptime(datePostedRenewed, '%d-%m-%Y').timestamp()
        self.views = views
        self.features = features
        self.facilities = facilities

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)

def compare(url1, url2, url3, url4, url5):
    connection = psycopg2.connect(user="postgres", password="postgres", host="127.0.0.1", port="5432",
                                  database="daft")
    try:

        cursor = connection.cursor()

        sql_select_Query = " select title_url, price, beds_size_acres, bathrooms, square_meter, property_type, description, ber, date, views from public.properties where title_url in ("
        if url1:
            sql_select_Query += "'"+url1+"'"
        if url2:
            sql_select_Query += ", '" + url2 +"'"
        if url3:
            sql_select_Query += ", '" + url3+"'"

        if url4:
            sql_select_Query += ", '" + url4+"'"

        if url5:
            sql_select_Query += ", '" + url5+"'"

        sql_select_Query += " )"
        cursor = connection.cursor()
        #record_to_insert = (url1, url2, url3, url4, url5, )
        cursor.execute(sql_select_Query)

        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        print("Total number of rows in Laptop is: ", cursor.rowcount)
        listOfProperties = []
        print("\nPrinting each laptop record")
        for row in records:
            # listOfProperties.append(Property())
            print("url = ", row[0], )
            print("price = ", row[1], )
            print("bedSize = ", row[2], )
            print("bathrooms = ", row[3], )
            print("sqMeter = ", row[4], )
            print("propertyType = ", row[5], )
            print("description = ", row[6], )
            print("ber = ", row[7], )
            print("date = ", row[8], )
            print("views  = ", row[9], "\n")
            listOfProperties.append(Property(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], "", ""))

        return listOfProperties
    except (Exception, psycopg2.Error) as error:
        print("Error reading data from MySQL table", error)
    finally:
        if (connection):
            connection.commit()
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


@app.route('/', methods=['GET'])
def home():
    url1 = request.args.get('url1')
    url2 = request.args.get('url2')
    url3 = request.args.get('url3')
    url4 = request.args.get('url4')
    url5 = request.args.get('url5')
    #data = compare(url1, url2, url3, url4, url5)
    #pd.DataFrame(data)
    """
    data["Rank"] = data["Name"].rank()

    # display
    data

    # sorting w.r.t name column
    data.sort_values("Name", inplace=True)

    # display after sorting w.r.t Name column
    data
    
    """
    allProperties = []
    for eachProperty in compare(url1, url2, url3, url4, url5):

        allProperties.append(eachProperty.__dict__)

    properties = pd.DataFrame(allProperties)
    properties['rnk_price'] = properties['price'].rank(ascending=True)
    properties['rnk_views'] = properties['views'].rank(ascending=False)
    properties['wgt_price'] = 0.9
    properties['wgt_views'] = 0.1

    properties['rnk_consolidate'] = properties['rnk_price']* properties['wgt_price'] + properties['rnk_views']* properties['wgt_views']
    properties['rnk_consolidate_final'] =properties['rnk_consolidate'].rank()

    properties_ranks = properties[['price','views','rnk_consolidate_final','url']]

    return properties_ranks.to_html()


def foundItems(key):
    connection = psycopg2.connect(user="postgres", password="postgres", host="127.0.0.1", port="5432",
                                  database="daft")
    try:

        cursor = connection.cursor()

        sql_select_Query = " select title_url, price, beds_size_acres, bathrooms, square_meter, property_type, description, ber, date, views "
        sql_select_Query +=" from public.properties where title ILIKE '%"+key+"%' LIMIT 20 "
        cursor = connection.cursor()

        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        print("Total number of rows in Laptop is: ", cursor.rowcount)
        listOfProperties = []
        print("\nPrinting each laptop record")
        for row in records:
            # listOfProperties.append(Property())
            print("url = ", row[0], )
            print("price = ", row[1], )
            print("bedSize = ", row[2], )
            print("bathrooms = ", row[3], )
            print("sqMeter = ", row[4], )
            print("propertyType = ", row[5], )
            print("description = ", row[6], )
            print("ber = ", row[7], )
            print("date = ", row[8], )
            print("views  = ", row[9], "\n")
            listOfProperties.append(
                Property(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], "", ""))

        return listOfProperties
    except (Exception, psycopg2.Error) as error:
        print("Error reading data from MySQL table", error)
    finally:
        if (connection):
            connection.commit()
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


@app.route('/find', methods=['GET'])
def find():
    key = request.args.get('key')
    return json.dumps([ob.__dict__ for ob in foundItems(key)])

@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

app.run()
