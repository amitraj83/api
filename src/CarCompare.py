import flask
from flask import request, jsonify
import psycopg2

import datetime
import numpy as np
import pandas as pd
import os
import os.path
from os import path
from random import randrange
from string import Template
import urllib
import urllib.parse
import psycopg2
import json
import datetime
from TitleGenerator import generateSEOTitleDescriptionKeywords
from ContentGenerator import getHTMLContent
from Classes import Car


app = flask.Flask(__name__)
app.config["DEBUG"] = True

jsonTemplate = {}


class LightCar:
    def __init__(self, name, id):
        self.name = name
        self.id = id
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)

class Criteria:
    def __init__(self, col_name, display_name, description):
        self.col_name = col_name
        self.display_name = display_name
        self.description = description
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)

class Make:
    def __init__(self, value, label):
        self.value = value
        self.label = label
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)

class Model:
    def __init__(self, value, label):
        self.value = value
        self.label = label
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)

class Variant:
    def __init__(self, value, label):
        self.value = value
        self.label = label
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)


defaultCriteria = {
  "criteria": [
    [
      {
        "id": 880,
        "col_name": "model_year",
        "displayname": "Model Year",
        "preference": "False",
        "importance": "5"
      },
      {
        "id": 8900,
        "col_name": "model_engine_cc",
        "displayname": "Engine size (cc)",
        "preference": "False",
        "importance": "5"
      },
      {
        "id": 6294,
        "col_name": "model_engine_cyl",
        "displayname": "Engine Cylinder",
        "preference": "False",
        "importance": "3"
      },
      {
        "id": 367,
        "col_name": "model_engine_power_rpm",
        "displayname": "Engine power (rpm)",
        "preference": "False",
        "importance": "2"
      },
      {
        "id": 8245,
        "col_name": "model_engine_torque_rpm",
        "displayname": "Engine Torque (rpm)",
        "preference": "False",
        "importance": "2"
      },
      {
        "id": 1234,
        "col_name": "model_seats",
        "displayname": "Seats",
        "preference": "True",
        "importance": "4"
      },
      {
        "id": 4567,
        "col_name": "model_doors",
        "displayname": "Doors",
        "preference": "True",
        "importance": "3"
      },
      {
        "id": 765,
        "col_name": "model_width_mm",
        "displayname": "Width (mm)",
        "preference": "True",
        "importance": "5"
      },
      {
        "id": 3756,
        "col_name": "model_height_mm",
        "displayname": "Height (mm)",
        "preference": "True",
        "importance": "5"
      }
    ]
  ]
  
}

class LinkInformation:
    def __init__(self, id, car_ids, criteria, response, display_text, summary, page_title, other_data, url, carDetails, keywords):
        self.id = id
        self.car_ids = car_ids
        self.criteria = criteria
        self.response = response
        self.display_text = display_text
        self.summary = summary
        self.page_title = page_title
        self.other_data = other_data
        self.url = url
        self.carDetails = carDetails
        self.keywords = keywords
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)

def compareData(vid1, vid2, vid3):
    connection = psycopg2.connect(user="postgres", password="postgres", host="127.0.0.1", port="5432",
                                  database="daft")
    try:
        cursor = connection.cursor()
        sql_select_Query = " select * from cars.car where model_id in ( "
        if vid1:
            sql_select_Query += " "+vid1+" "
        if vid2:
            sql_select_Query += ", "+vid2+" "
        if vid3:
            sql_select_Query += ", "+vid3+" "

        sql_select_Query += " ) "
        print(sql_select_Query)
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)

        # cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        listOfCars = []
        for row in records:
            listOfCars.append(Car(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20], row[21], row[22], row[23], row[24], row[25], row[26], row[27], row[28], row[29], row[30], row[31], row[32], row[33], row[34], row[35], row[36], row[37]))
        return listOfCars
    except (Exception, psycopg2.Error) as error:
        print("Error reading data from MySQL table", error)
    finally:
        if (connection):
            connection.commit()
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")





def insertLink(carsRequest, rankCriteria, rank_json, versus, category, all_ranks_json):
    connection = psycopg2.connect(user="postgres", password="postgres", host="127.0.0.1", port="5432",
                                  database="daft")
    number = None
    try:
        cursor = connection.cursor()
        cursor.execute("select nextval('cars.car_links_id_seq'::regclass)")
        number = cursor.fetchone()
        if not rankCriteria:
            rankCriteria = []
        cursor = connection.cursor()
        postgres_insert_query = " INSERT INTO cars.car_links "
        postgres_insert_query += " (id, car_ids, criteria, response, display_text, summary, page_title, other_data, url, keywords, powerKeyword) "
        postgres_insert_query += " VALUES ( %s, %s, %s, %s, %s, %s, %s, %s , %s, %s, %s )"

        metaData = generateSEOTitleDescriptionKeywords(all_ranks_json)
        powerKeyword = metaData['powerKeyword']

        url = "/compare/" + category + "/" + str(number[0]) + "/" + powerKeyword.replace(" ", "-")
        otherData = {"rank_data":json.loads(all_ranks_json), "blog_content":getHTMLContent(number[0], carsRequest, rankCriteria, rank_json, versus, versus, versus, {"rank_data":json.loads(all_ranks_json)}, url, metaData['keywords'], powerKeyword)}
        record_to_insert = (number[0], (carsRequest,), json.dumps(rankCriteria), rank_json, versus, metaData['description'], metaData['title'], json.dumps((otherData)), url, ', '.join(metaData['keywords']), powerKeyword,)


        cursor.execute(postgres_insert_query, record_to_insert)

        return url
    except (Exception, psycopg2.Error) as error:
        print("Error inserting link data to MySQL table", error)
    finally:
        if (connection):
            connection.commit()
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")




@app.route('/api/compare/cars', methods=['POST'])
def compareCars():

    if not request.data :
        return {};

    carsRequest = json.loads(request.data)['cars']
    rankCriteria = json.loads(request.data)['criteria']
    if len(carsRequest) > 3:
        return {}
    vid1 = None
    vid2 = None
    vid3 = None
    if carsRequest[0]:
        vid1 = str(carsRequest[0])
    if carsRequest[1]:
        vid2 = str(carsRequest[1])
    if carsRequest[2]:
        vid3 = str(carsRequest[2])

    data = compareData(vid1, vid2, vid3)

    if data:
        allData = []

        for eachCar in data:
            allData.append(eachCar.__dict__)

        cars = pd.DataFrame(allData)

        totalWgt = 0
        criteria = []

        if len(rankCriteria) > 0:
            criteria = rankCriteria
        else:
            criteria = defaultCriteria["criteria"][0]
            
        for i in range(len(criteria)):
            cars['rnk_'+criteria[i]['col_name']] = cars[criteria[i]['col_name']].rank(ascending=(criteria[i]['preference'] == "True"))
            totalWgt += int(criteria[0]['importance'])
        if totalWgt != 0:
            for i in range(len(criteria)):
                cars['wgt_' + criteria[i]['col_name']] = int(criteria[i]['importance']) / totalWgt
        rankConsolidate = 0
        for i in range(len(criteria)):
            rankConsolidate += cars['rnk_' + criteria[i]['col_name']] * cars[
                'wgt_' + criteria[i]['col_name']]
        cars['rnk_consolidate'] = rankConsolidate

        cars['rnk_consolidate_final'] = cars['rnk_consolidate'].rank()

        cars_ranks = cars[['rnk_consolidate_final', 'model_id', 'model_make_display', 'model_name', 'model_year', 'model_engine_cc', 'model_engine_cyl', 'model_engine_power_rpm', 'model_engine_torque_rpm', 'model_seats', 'model_doors', 'model_width_mm', 'model_height_mm']]
        rank_json = cars_ranks.to_json()
        versus = ""
        dash = "-vs-"
        for i in range(len(cars_ranks['model_make_display'])):
            if i == len(cars_ranks['model_make_display']) -1:
                dash = ""
            versus += cars_ranks['model_make_display'][i]+"-"+cars_ranks['model_name'][i]+"-"+str(int(cars_ranks['model_year'][i]))+dash
        pushUrl = insertLink(carsRequest, criteria, rank_json, versus, "cars", cars.to_json())
        return {"cars_ranks":cars_ranks.to_json(), "pushUrl":pushUrl}

    else:
        return "no data. provide vid1, vid2 and vid3 in query params"


def foundItems(key):
    connection = psycopg2.connect(user="postgres", password="postgres", host="127.0.0.1", port="5432",
                                  database="daft")
    try:
        cursor = connection.cursor()
        sql_select_Query = "select CONCAT(model_make_display, ' - ', model_name, ' ( ', model_year, ' )') as display_name, model_id from cars.car "


        if key:
            sql_select_Query += "  where model_make_display ILIKE '%"+key+"%' or model_name ILIKE '%"+key+"%'"

        sql_select_Query += " order by model_year DESC "

        cursor = connection.cursor()

        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        listOfCars = []
        for row in records:
            listOfCars.append(LightCar(row[0],row[1]))

        return listOfCars
    except (Exception, psycopg2.Error) as error:
        print("Error reading data from MySQL table", error)
    finally:
        if (connection):
            connection.commit()
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def getOneLinkInformation(row):
    connection = psycopg2.connect(user="postgres", password="postgres", host="127.0.0.1", port="5432",
                                  database="daft")
    cursor2 = connection.cursor()
    carDetails = []
    listofId = str(row[1]).replace("[", "(").replace("]", ")")
    carsQuery = " select model_id, model_make_id, model_name, model_trim, model_year, model_body, model_engine_position, model_engine_cc, model_engine_cyl, model_engine_type, model_engine_valves_per_cyl, model_engine_power_ps, model_engine_power_rpm, model_engine_torque_nm, model_engine_torque_rpm, model_engine_bore_mm, model_engine_stroke_mm, model_engine_compression, model_engine_fuel, model_top_speed_kph, model_0_to_100_kph, model_drive, model_transmission_type, model_seats, model_doors, model_weight_kg, model_length_mm, model_width_mm, model_height_mm, model_wheelbase_mm, model_lkm_hwy, model_lkm_mixed, model_lkm_city, model_fuel_cap_l, model_sold_in_us, model_co2, model_make_display, image from cars.car where model_id in " + listofId
    cursor2.execute(carsQuery)
    carRecords = cursor2.fetchall()
    for carRow in carRecords:
        carDetails.append(
            Car(carRow[0], carRow[1], carRow[2], carRow[3], carRow[4], carRow[5], carRow[6], carRow[7], carRow[8],
                carRow[9], carRow[10], carRow[11],
                carRow[12], carRow[13], carRow[14], carRow[15], carRow[16], carRow[17], carRow[18], carRow[19],
                carRow[20], carRow[21], carRow[22],
                carRow[23], carRow[24], carRow[25], carRow[26], carRow[27], carRow[28], carRow[29], carRow[30],
                carRow[31], carRow[32], carRow[33],
                carRow[34], carRow[35], carRow[36], carRow[37]))
    newCarDetails = json.dumps([ob.__dict__ for ob in carDetails])
    if not newCarDetails:
        newCarDetails = row[3]
    linkInfo = LinkInformation(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], carDetails, row[9])
    return linkInfo

def getLinkData(key):
    connection = psycopg2.connect(user="postgres", password="postgres", host="127.0.0.1", port="5432",
                                  database="daft")
    try:
        cursor = connection.cursor()

        where = " where id = "+key

        sql_select_Query = " select id, car_ids, criteria, response, display_text, summary, page_title, other_data, url, keywords from cars.car_links "+where

        if key:
            cursor.execute(sql_select_Query)
            records = cursor.fetchall()
            linkInfo = None
            for row in records:
                linkInfo = getOneLinkInformation(row)
        return linkInfo
    except (Exception, psycopg2.Error) as error:
        print("Error reading data from MySQL table", error)
    finally:
        if (connection):
            connection.commit()
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def getAllLinkData():
    connection = psycopg2.connect(user="postgres", password="postgres", host="127.0.0.1", port="5432",
                                  database="daft")
    try:
        cursor = connection.cursor()
        sql_select_Query = " select id, car_ids, criteria, response, display_text, summary, page_title, other_data, url, keywords from cars.car_links "

        allLinks = []
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        for row in records:
            allLinks.append(getOneLinkInformation(row))
        return allLinks
    except (Exception, psycopg2.Error) as error:
        print("Error reading data from MySQL table", error)
    finally:
        if (connection):
            connection.commit()
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


@app.route('/api/all/links/information', methods=['GET'])
def getLinkInformationAll():
    data = getAllLinkData()
    return json.dumps([ob.__dict__ for ob in data])


@app.route('/api/links/information', methods=['GET'])
def getLinkInformation():
    linkNumber = request.args.get('linkNumber')
    data = getLinkData(linkNumber)
    return data.toJSON()

@app.route('/api/list/cars', methods=['GET'])
def listCarsAPI():
    key = request.args.get('key')
    # return json.dumps(foundItems(key))
    return json.dumps([ob.__dict__ for ob in foundItems(key)])


def getCarDetails(id):
    connection = psycopg2.connect(user="postgres", password="postgres", host="127.0.0.1", port="5432",
                                  database="daft")
    try:
        cursor = connection.cursor()
        sql_select_Query = " select model_id, model_make_id, model_name, model_trim, model_year, model_body, model_engine_position, model_engine_cc, model_engine_cyl, model_engine_type, model_engine_valves_per_cyl, model_engine_power_ps, model_engine_power_rpm, model_engine_torque_nm, model_engine_torque_rpm, model_engine_bore_mm, model_engine_stroke_mm, model_engine_compression, model_engine_fuel, model_top_speed_kph, model_0_to_100_kph, model_drive, model_transmission_type, model_seats, model_doors, model_weight_kg, model_length_mm, model_width_mm, model_height_mm, model_wheelbase_mm, model_lkm_hwy, model_lkm_mixed, model_lkm_city, model_fuel_cap_l, model_sold_in_us, model_co2, model_make_display, image from cars.car where model_id = "+id

        cursor = connection.cursor()
        cursor.execute(sql_select_Query)

        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        for row in records:
            return Car(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11],
                    row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20], row[21], row[22],
                    row[23], row[24], row[25], row[26], row[27], row[28], row[29], row[30], row[31], row[32], row[33],
                    row[34], row[35], row[36], row[37])
        return None
    except (Exception, psycopg2.Error) as error:
        print("Error reading data from MySQL table", error)
    finally:
        if (connection):
            connection.commit()
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


@app.route('/api/car/details', methods=['GET'])
def getCar12():
    id = request.args.get('id')
    # return json.dumps(foundItems(key))
    description = json.dumps([ob.__dict__ for ob in listAllFields()])
    return getCarDetails(id).toJSON()


def getAllMakes():
    connection = psycopg2.connect(user="postgres", password="postgres", host="127.0.0.1", port="5432",
                                  database="daft")
    try:
        cursor = connection.cursor()
        sql_select_Query = " select distinct model_make_id from cars.car where model_trim != '' order by model_make_id "

        cursor = connection.cursor()
        cursor.execute(sql_select_Query)

        # cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        allMakes = []
        for row in records:
            allMakes.append(Make(row[0], row[0].title()))
        return allMakes
    except (Exception, psycopg2.Error) as error:
        print("Error reading data from MySQL table", error)
    finally:
        if (connection):
            connection.commit()
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def getMakesForAModel(key):
    connection = psycopg2.connect(user="postgres", password="postgres", host="127.0.0.1", port="5432",
                                  database="daft")
    try:
        cursor = connection.cursor()
        # sql_select_Query = " select  distinct model_name from cars.car where model_make_id = '"+key+"' "
        sql_select_Query = " select  distinct (model_name || ' (' || model_year || ')') as modelName, model_name, model_year from cars.car where model_make_id ILIKE '"+key+"' and model_trim != '' order by model_year DESC "
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)

        # cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        allModels = []
        for row in records:
            allModels.append(Model(row[1]+"$"+str(row[2]), row[0]))
        return allModels
    except (Exception, psycopg2.Error) as error:
        print("Error reading data from MySQL table", error)
    finally:
        if (connection):
            connection.commit()
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")




@app.route('/api/car/makes', methods=['GET'])
def getMakes():

    # return json.dumps(foundItems(key))
    return json.dumps([ob.__dict__ for ob in getAllMakes()])

@app.route('/api/car/models', methods=['GET'])
def getModels():
    make = request.args.get('make')
    # return json.dumps(foundItems(key))
    return json.dumps([ob.__dict__ for ob in getMakesForAModel(make)])


def getVariants(make, model):
    connection = psycopg2.connect(user="postgres", password="postgres", host="127.0.0.1", port="5432",
                                  database="daft")
    try:
        cursor = connection.cursor()
        splittedModelYear = model.split("$")
        year = int(splittedModelYear[1])
        model = str(splittedModelYear[0])
        sql_select_Query = " select model_trim, model_id, model_year  from cars.car where model_make_id = '"+make+"' and model_name = '"+model+"' and model_year = "+str(year)+" and model_trim != '' order by model_year DESC "

        cursor = connection.cursor()

        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        allVariants = []
        for row in records:
            allVariants.append(Variant(row[1], row[0]))
        return allVariants
    except (Exception, psycopg2.Error) as error:
        print("Error reading data from MySQL table", error)
    finally:
        if (connection):
            connection.commit()
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def getThreeRandomBlogLinks():
    connection = psycopg2.connect(user="postgres", password="postgres", host="127.0.0.1", port="5432",
                                  database="daft")
    try:
        cursor = connection.cursor()
        sql_select_Query = " select  other_data, url from cars.car_links where other_data::text != '{}'::text and url != '' and display_text != '' order by RANDOM() LIMIT 3 "

        cursor = connection.cursor()

        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        listOfBlogs = []
        for row in records:
            listOfBlogs.append({"other_data": row[0], "url": row[1]})

        return listOfBlogs
    except (Exception, psycopg2.Error) as error:
        print("Error reading data from MySQL table", error)
    finally:
        if (connection):
            connection.commit()
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def getAllBlogLinks():
    connection = psycopg2.connect(user="postgres", password="postgres", host="127.0.0.1", port="5432",
                                  database="daft")
    try:
        cursor = connection.cursor()
        sql_select_Query = " select url, display_text from cars.car_links where url != '' and display_text != '' order by id desc LIMIT 10  "

        cursor = connection.cursor()

        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        listOfBlogs = []
        for row in records:
            listOfBlogs.append({"link":row[0], "displayText":row[1]})

        return listOfBlogs
    except (Exception, psycopg2.Error) as error:
        print("Error reading data from MySQL table", error)
    finally:
        if (connection):
            connection.commit()
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


def listAllFields():
    connection = psycopg2.connect(user="postgres", password="postgres", host="127.0.0.1", port="5432",
                                  database="daft")
    try:
        cursor = connection.cursor()
        sql_select_Query = "SELECT * FROM cars.criteria ORDER BY col_name ASC  "

        cursor = connection.cursor()

        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        listOfCriteria = []
        for row in records:
            listOfCriteria.append(Criteria(row[0], row[1], row[2]))

        return listOfCriteria
    except (Exception, psycopg2.Error) as error:
        print("Error reading data from MySQL table", error)
    finally:
        if (connection):
            connection.commit()
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

@app.route('/api/car/variants', methods=['GET'])
def getVarian():
    make = request.args.get('make')
    model = request.args.get('model')
    # return json.dumps(foundItems(key))
    return json.dumps([ob.__dict__ for ob in getVariants(make, model)])

@app.route('/api/criteria', methods=['GET'])
def listCriteria():
    return json.dumps([ob.__dict__ for ob in listAllFields()]);

@app.route('/api/car/fields/descriptions', methods=['GET'])
def getdescription():
    return json.dumps([ob.__dict__ for ob in listAllFields()]);


def recentComparisons(type):
    connection = psycopg2.connect(user="postgres", password="postgres", host="127.0.0.1", port="5432",
                                  database="daft")
    try:
        cursor = connection.cursor()

        sql_select_Query = " select id, car_ids, criteria, response, display_text, summary, page_title, other_data, url from cars.car_links where display_text != '' order by random() desc LIMIT 20 "

        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        linkInfo = []
        for row in records:
            splittedTitle = row[4].split("-")
            if len(splittedTitle) > 0:
                title = splittedTitle[0]
                name = row[4]
                link = row[8]
                try:
                    # title exists

                    if len(linkInfo) == 0:
                        linkInfo.append({"title": title, "resources": [{"name": name, "link": link}]})
                        continue
                    titleAlreadyExists = False
                    for i in range(len(linkInfo)):
                        temp = linkInfo[i]
                        temp = linkInfo[i]
                        if temp["title"] == title:
                            tempResources = temp["resources"]
                            if len(tempResources) < 5:
                                tempResources.append({"name":name, "link":link})
                                temp["resources"] = tempResources
                                linkInfo[i] = temp
                            titleAlreadyExists = True
                    if not titleAlreadyExists and len(linkInfo) < 5:
                            linkInfo.append({"title": title, "resources": [{"name": name, "link": link}]})
                except (Exception) as error:
                    # title does not exists
                    print(error)

        return linkInfo
    except (Exception, psycopg2.Error) as error:
        print("Error reading data from MySQL table", error)
    finally:
        if (connection):
            connection.commit()
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


@app.route('/api/car/recent/comparisons', methods=['GET'])
def getRecentComparisons():
    comparisons = recentComparisons("cars");
    return json.dumps([ob for ob in comparisons]);

@app.route('/api/car/criteria/default', methods=['GET'])
def getDefaultCriteria():

    return json.dumps(defaultCriteria["criteria"][0]);




@app.route('/api/car/blogs/links', methods=['GET'])
def getBlogsLInks():

    return json.dumps(getAllBlogLinks());


@app.route('/api/car/blogs/cards', methods=['GET'])
def getThreeBlogsLInks():

    return json.dumps(getThreeRandomBlogLinks());


@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

app.run(host='0.0.0.0')