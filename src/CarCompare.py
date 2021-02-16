import flask
from flask import request, jsonify
import psycopg2
import json
import datetime
import numpy as np
import pandas as pd

app = flask.Flask(__name__)
app.config["DEBUG"] = True


class Car:
    def __init__(self, model_id,model_make_id,model_name,model_trim,model_year,model_body,model_engine_position,model_engine_cc,model_engine_cyl,model_engine_type,model_engine_valves_per_cyl,model_engine_power_ps,model_engine_power_rpm,model_engine_torque_nm,model_engine_torque_rpm,model_engine_bore_mm,model_engine_stroke_mm,model_engine_compression,model_engine_fuel,model_top_speed_kph,model_0_to_100_kph,model_drive,model_transmission_type,model_seats,model_doors,model_weight_kg,model_length_mm,model_width_mm,model_height_mm,model_wheelbase_mm,model_lkm_hwy,model_lkm_mixed,model_lkm_city,model_fuel_cap_l,model_sold_in_us,model_co2,model_make_display, image):
        self.model_id = model_id
        self.model_make_id = model_make_id
        self.model_name = model_name
        self.model_trim = model_trim
        self.model_year = model_year
        self.model_body = model_body
        self.model_engine_position = model_engine_position
        self.model_engine_cc = model_engine_cc
        self.model_engine_cyl = model_engine_cyl
        self.model_engine_type = model_engine_type
        self.model_engine_valves_per_cyl = model_engine_valves_per_cyl
        self.model_engine_power_ps = model_engine_power_ps
        self.model_engine_power_rpm = model_engine_power_rpm
        self.model_engine_torque_nm = model_engine_torque_nm
        self.model_engine_torque_rpm = model_engine_torque_rpm
        self.model_engine_bore_mm = model_engine_bore_mm
        self.model_engine_stroke_mm = model_engine_stroke_mm
        self.model_engine_compression = model_engine_compression
        self.model_engine_fuel = model_engine_fuel
        self.model_top_speed_kph = model_top_speed_kph
        self.model_0_to_100_kph = model_0_to_100_kph
        self.model_drive = model_drive
        self.model_transmission_type = model_transmission_type
        self.model_seats = model_seats
        self.model_doors = model_doors
        self.model_weight_kg = model_weight_kg
        self.model_length_mm = model_length_mm
        self.model_width_mm = model_width_mm
        self.model_height_mm = model_height_mm
        self.model_wheelbase_mm = model_wheelbase_mm
        self.model_lkm_hwy = model_lkm_hwy
        self.model_lkm_mixed = model_lkm_mixed
        self.model_lkm_city = model_lkm_city
        self.model_fuel_cap_l = model_fuel_cap_l
        self.model_sold_in_us = model_sold_in_us
        self.model_co2 = model_co2
        self.model_make_display = model_make_display
        self.image = image

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)


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



class LinkInformation:
    def __init__(self, id, car_ids, criteria, response, display_text, summary, page_title, other_data, url, carDetails):
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

        cursor.execute(sql_select_Query)
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


def insertLink(carsRequest, rankCriteria, rank_json, versus, category):
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
        postgres_insert_query += " (id, car_ids, criteria, response, display_text, summary, page_title, other_data, url) "
        postgres_insert_query += " VALUES ( %s, %s, %s, %s, %s, %s, %s, %s , %s )"

        url = "/compare/" + category + "/" + str(number[0]) + "/" + versus
        record_to_insert = (number[0], (carsRequest,), json.dumps(rankCriteria), rank_json, versus, versus, versus, '{}', url,)

        # print("LInk Query", postgres_insert_query)
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
        if rankCriteria:
            for i in range(len(rankCriteria[0])):
                cars['rnk_'+rankCriteria[0][i]['col_name']] = cars[rankCriteria[0][i]['col_name']].rank(ascending=(rankCriteria[0][i]['preference'] == "True"))
                totalWgt += int(rankCriteria[0][0]['importance'])
            if totalWgt != 0:
                for i in range(len(rankCriteria[0])):
                    cars['wgt_' + rankCriteria[0][i]['col_name']] = int(rankCriteria[0][i]['importance']) / totalWgt
            rankConsolidate = 0
            for i in range(len(rankCriteria[0])):
                rankConsolidate += cars['rnk_' + rankCriteria[0][i]['col_name']] * cars[
                    'wgt_' + rankCriteria[0][i]['col_name']]
            cars['rnk_consolidate'] = rankConsolidate
        else:
            cars['rnk_model_year'] = cars['model_year'].rank(ascending=False)
            cars['rnk_model_engine_cc'] = cars['model_engine_cc'].rank(ascending=False)
            cars['rnk_model_engine_cyl'] = cars['model_engine_cyl'].rank(ascending=False)
            cars['rnk_model_engine_power_rpm'] = cars['model_engine_power_rpm'].rank(ascending=False)
            cars['rnk_model_engine_torque_rpm'] = cars['model_engine_torque_rpm'].rank(ascending=False)
            cars['rnk_model_seats'] = cars['model_seats'].rank(ascending=False)
            cars['rnk_model_doors'] = cars['model_doors'].rank(ascending=False)
            cars['rnk_model_width_mm'] = cars['model_width_mm'].rank(ascending=False)
            cars['rnk_model_height_mm'] = cars['model_height_mm'].rank(ascending=False)

            cars['wgt_model_year'] = 0.3
            cars['wgt_model_engine_cc'] = 0.1
            cars['wgt_model_engine_cyl'] = 0.05
            cars['wgt_model_engine_power_rpm'] = 0.05
            cars['wgt_model_engine_torque_rpm'] = 0.05
            cars['wgt_model_seats'] = 0.2
            cars['wgt_model_doors'] = 0.1
            cars['wgt_model_width_mm'] = 0.1
            cars['wgt_model_height_mm'] = 0.1

            model_year_Consilidate = cars['rnk_model_year'] * cars['wgt_model_year']
            model_engine_cc_Consolidate = cars['rnk_model_engine_cc'] * cars['wgt_model_engine_cc']
            model_engine_cyl_Consolidate = cars['rnk_model_engine_cyl'] * cars['wgt_model_engine_cyl']
            model_engine_power_rpm_Consolidate = cars['rnk_model_engine_power_rpm'] * cars['wgt_model_engine_power_rpm']
            model_engine_torque_rpm_Consolidate = cars['rnk_model_engine_torque_rpm'] * cars['wgt_model_engine_torque_rpm']
            model_seats_Consolidate = cars['rnk_model_seats'] * cars['wgt_model_seats']
            model_doors_Consolidate = cars['rnk_model_doors'] * cars['wgt_model_doors']
            model_width_mm_Consolidate = cars['rnk_model_width_mm'] * cars['wgt_model_width_mm']
            model_height_mm_Consolidate = cars['rnk_model_height_mm'] * cars['wgt_model_height_mm']

            cars['rnk_consolidate'] = model_year_Consilidate + model_engine_cc_Consolidate + model_engine_cyl_Consolidate + model_engine_power_rpm_Consolidate + model_engine_torque_rpm_Consolidate + model_seats_Consolidate + model_doors_Consolidate + model_width_mm_Consolidate + model_height_mm_Consolidate


        cars['rnk_consolidate_final'] = cars['rnk_consolidate'].rank()

        cars_ranks = cars[['rnk_consolidate_final', 'model_id', 'model_make_display', 'model_name', 'model_year', 'model_engine_cc', 'model_engine_cyl', 'model_engine_power_rpm', 'model_engine_torque_rpm', 'model_seats', 'model_doors', 'model_width_mm', 'model_height_mm']]
        rank_json = cars_ranks.to_json()
        versus = ""
        dash = "-vs-"
        for i in range(len(cars_ranks['model_make_display'])):
            if i == len(cars_ranks['model_make_display']) -1:
                dash = ""
            versus += cars_ranks['model_make_display'][i]+"-"+cars_ranks['model_name'][i]+"-"+str(int(cars_ranks['model_year'][i]))+dash
        #cars_ranks['model_make_display'][0]+"-"+cars_ranks['model_name'][0]+"-"+str(int(cars_ranks['model_year'][0]))
        pushUrl = insertLink(carsRequest, rankCriteria[0] if rankCriteria else None, rank_json, versus, "cars")
        return {"cars_ranks":cars_ranks.to_json(), "pushUrl":pushUrl}
        # return json.dumps([ob.__dict__ for ob in data])
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


def getLinkData(key):
    connection = psycopg2.connect(user="postgres", password="postgres", host="127.0.0.1", port="5432",
                                  database="daft")
    try:
        cursor = connection.cursor()
        cursor2 = connection.cursor()

        sql_select_Query = " select id, car_ids, criteria, response, display_text, summary, page_title, other_data, url from cars.car_links where id = "+key

        if key:
            cursor.execute(sql_select_Query)
            records = cursor.fetchall()
            linkInfo = None
            for row in records:
                carDetails = []
                listofId = str(row[1]).replace("[", "(").replace("]",")")
                carsQuery = " select model_id, model_make_id, model_name, model_trim, model_year, model_body, model_engine_position, model_engine_cc, model_engine_cyl, model_engine_type, model_engine_valves_per_cyl, model_engine_power_ps, model_engine_power_rpm, model_engine_torque_nm, model_engine_torque_rpm, model_engine_bore_mm, model_engine_stroke_mm, model_engine_compression, model_engine_fuel, model_top_speed_kph, model_0_to_100_kph, model_drive, model_transmission_type, model_seats, model_doors, model_weight_kg, model_length_mm, model_width_mm, model_height_mm, model_wheelbase_mm, model_lkm_hwy, model_lkm_mixed, model_lkm_city, model_fuel_cap_l, model_sold_in_us, model_co2, model_make_display, image from cars.car where model_id in "+listofId
                cursor2.execute(carsQuery)
                carRecords = cursor2.fetchall()
                for carRow in carRecords:
                    carDetails.append(Car(carRow[0], carRow[1], carRow[2], carRow[3], carRow[4], carRow[5], carRow[6], carRow[7], carRow[8], carRow[9], carRow[10], carRow[11],
                    carRow[12], carRow[13], carRow[14], carRow[15], carRow[16], carRow[17], carRow[18], carRow[19], carRow[20], carRow[21], carRow[22],
                    carRow[23], carRow[24], carRow[25], carRow[26], carRow[27], carRow[28], carRow[29], carRow[30], carRow[31], carRow[32], carRow[33],
                    carRow[34], carRow[35], carRow[36], carRow[37]))
                newCarDetails = json.dumps([ob.__dict__ for ob in carDetails])
                if not newCarDetails:
                    newCarDetails = row[3]
                linkInfo = LinkInformation(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], newCarDetails)

        return linkInfo
    except (Exception, psycopg2.Error) as error:
        print("Error reading data from MySQL table", error)
    finally:
        if (connection):
            connection.commit()
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


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
def getCar():
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

        sql_select_Query = " select id, car_ids, criteria, response, display_text, summary, page_title, other_data, url from cars.car_links where display_text != '' order by id desc LIMIT 20 "

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





@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

app.run(host='0.0.0.0')