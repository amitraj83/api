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
    def __init__(self, model_id,model_make_id,model_name,model_trim,model_year,model_body,model_engine_position,model_engine_cc,model_engine_cyl,model_engine_type,model_engine_valves_per_cyl,model_engine_power_ps,model_engine_power_rpm,model_engine_torque_nm,model_engine_torque_rpm,model_engine_bore_mm,model_engine_stroke_mm,model_engine_compression,model_engine_fuel,model_top_speed_kph,model_0_to_100_kph,model_drive,model_transmission_type,model_seats,model_doors,model_weight_kg,model_length_mm,model_width_mm,model_height_mm,model_wheelbase_mm,model_lkm_hwy,model_lkm_mixed,model_lkm_city,model_fuel_cap_l,model_sold_in_us,model_co2,model_make_display):
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
            listOfCars.append(Car(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20], row[21], row[22], row[23], row[24], row[25], row[26], row[27], row[28], row[29], row[30], row[31], row[32], row[33], row[34], row[35], row[36]))
        return listOfCars
    except (Exception, psycopg2.Error) as error:
        print("Error reading data from MySQL table", error)
    finally:
        if (connection):
            connection.commit()
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")




@app.route('/compare/cars', methods=['POST'])
def compareCars():

    if not request.data :
        return {};

    cars = json.loads(request.data)['cars']
    if len(cars) > 3:
        return {}
    vid1 = None
    vid2 = None
    vid3 = None
    if cars[0]:
        vid1 = str(cars[0])
    if cars[1]:
        vid2 = str(cars[1])
    if cars[2]:
        vid3 = str(cars[2])

    data = compareData(vid1, vid2, vid3)
    #return json.dumps([ob.__dict__ for ob in data]) json.loads(request.data)['criteria']
    #len(json.loads(request.data)['criteria'][0]) = 3
    #json.loads(request.data)['criteria'][0][0]
    #json.loads(request.data)['criteria'][0][1]
    #json.loads(request.data)['criteria'][0][2]
    #len(json.loads(request.data)['cars']) = 3
    #json.loads(request.data)['cars'][1]
    #json.loads(request.data)['cars'][0]

    if data:
        allData = []

        for eachCar in data:
            allData.append(eachCar.__dict__)

        cars = pd.DataFrame(allData)
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
        return cars_ranks.to_json()
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


@app.route('/list/cars', methods=['GET'])
def listCarsAPI():
    key = request.args.get('key')
    # return json.dumps(foundItems(key))
    return json.dumps([ob.__dict__ for ob in foundItems(key)])

@app.route('/criteria', methods=['GET'])
def listCriteria():
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

        return json.dumps([ob.__dict__ for ob in listOfCriteria])
    except (Exception, psycopg2.Error) as error:
        print("Error reading data from MySQL table", error)
    finally:
        if (connection):
            connection.commit()
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")






@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

app.run(host='0.0.0.0')