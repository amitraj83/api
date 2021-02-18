import os
from string import Template
import urllib
import urllib.parse
import psycopg2
import json

jsonTemplate = {}

importanceArray = ["at all important", "Slightly important", "Important", "Fairly Important", "Very important"]


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



def getCar(id):
    connection = psycopg2.connect(user="postgres", password="postgres", host="127.0.0.1", port="5432",
                                  database="daft")
    try:
        cursor = connection.cursor()
        sqlQuery = " select model_id, model_make_id, model_name, model_trim, model_year, model_body, model_engine_position, model_engine_cc, model_engine_cyl, model_engine_type, model_engine_valves_per_cyl, model_engine_power_ps, model_engine_power_rpm, model_engine_torque_nm, model_engine_torque_rpm, model_engine_bore_mm, model_engine_stroke_mm, model_engine_compression, model_engine_fuel, model_top_speed_kph, model_0_to_100_kph, model_drive, model_transmission_type, model_seats, model_doors, model_weight_kg, model_length_mm, model_width_mm, model_height_mm, model_wheelbase_mm, model_lkm_hwy, model_lkm_mixed, model_lkm_city, model_fuel_cap_l, model_sold_in_us, model_co2, model_make_display, image from cars.car where model_id = "+str(id) +" ; "
        cursor.execute(sqlQuery)
        records = cursor.fetchall()
        for row in records:
            return Car(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20], row[21], row[22], row[23], row[24], row[25], row[26], row[27], row[28], row[29], row[30], row[31], row[32], row[33], row[34], row[35], row[36], row[37])
    except (Exception, psycopg2.Error) as error:
        print("Error reading data from MySQL table", error)
    finally:
        if (connection):
            connection.commit()
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

def getRelatedLinks(listOfKeys):
    if len(listOfKeys) > 0:
        connection = psycopg2.connect(user="postgres", password="postgres", host="127.0.0.1", port="5432",
                                      database="daft")
        try:
            cursor = connection.cursor()
            sqlQuery = " select display_text, url from cars.car_links where "
            OR = " or "
            for i in range(len(listOfKeys)):
                if i == len(listOfKeys)-1:
                    OR = "  "
                key = listOfKeys[i]
                sqlQuery += " url ilike '%"+key+"%' " + OR
            sqlQuery += " order by id desc LIMIT 5  "
            cursor.execute(sqlQuery)
            records = cursor.fetchall()
            results = []
            for row in records:
                results.append({"url":row[1],"displayText":row[0]})
            return results
        except (Exception, psycopg2.Error) as error:
            print("Error reading data from MySQL table", error)
        finally:
            if (connection):
                connection.commit()
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed")

def main():
    connection = psycopg2.connect(user="postgres", password="postgres", host="127.0.0.1", port="5432",
                                  database="daft")
    try:
        cursor = connection.cursor()
        sqlQuery = " select id, car_ids, criteria, response, display_text, summary, page_title, other_data, url  FROM cars.car_links "
        cursor.execute(sqlQuery)
        records = cursor.fetchall()
        for row in records:

            with open('../doc/blog-template.json', 'r') as tf:
                jsonTemplate = json.loads(tf.read())


            if len(row[7]) > 0 and ('rank_data' in row[7].keys()):
                car1 = getCar(row[1][0])
                car2 = getCar(row[1][1])
                car3 = getCar(row[1][2])
                carIDMap = {row[1][0]:car1,row[1][1]:car2,row[1][2]:car3}



                with open('../doc/template.html', 'r') as f:
                    data = f.read()
                    template = Template(data)
                    jsonTemplate["title"] = row[6]
                    jsonTemplate["pageURL"] = urllib.parse.quote(row[8])
                    jsonTemplate["keywords"] = "Compare Car side by side, car comparison tool, "
                    description = "Compare "
                    if car1:
                        jsonTemplate["keywords"] += car1.model_make_display.title() + ", "
                        description += car1.model_make_display.title() + ", "
                    if car2:
                        jsonTemplate["keywords"] += car2.model_make_display.title() + ", "
                        description += car2.model_make_display.title() + ", "
                    if car3:
                        jsonTemplate["keywords"] += car3.model_make_display.title() + ", "
                        description += car3.model_make_display.title() + ", "
                    description += "side by side and rank them according to your preferences."
                    jsonTemplate["description"] = description

                    rank1_car_name = ""
                    rank2_car_name = ""
                    rank3_car_name = ""
                    rank1Car = None
                    rank2Car = None
                    rank3Car = None
                    rankCars = {}
                    seen = set()
                    for i in range(len(row[3]['model_id'])):
                        rank = int(row[3]['rnk_consolidate_final'][str(i)])
                        carId = int(row[3]['model_id'][str(i)])
                        aCar = carIDMap.get(carId)
                        carName = aCar.model_make_display +" "+aCar.model_name+" ("+str(aCar.model_year)+") "
                        rankCars[str(rank)] = carName
                        # TODO, rank is not always 1
                        if rank == int(min(row[3]['rnk_consolidate_final'].values())):
                            jsonTemplate["stars_car1"] = "<i class=\"fas fa-star\"></i><i class=\"fas fa-star\"></i><i class=\"fas fa-star\"></i><i class=\"fas fa-star\"></i><i class=\"fas fa-star\"></i>"
                            jsonTemplate["image_car1"] = aCar.image
                            jsonTemplate["carName1"] = carName
                            seen.add(i)
                            rank1_car_name = carName
                            rank1Car = aCar

                        if rank == int(max(row[3]['rnk_consolidate_final'].values())):
                            seen.add(i)
                            jsonTemplate["stars_car3"] = "<i class=\"fas fa-star\"></i><i class=\"far fa-star\"></i><i class=\"far fa-star\"></i><i class=\"far fa-star\"></i><i class=\"far fa-star\"></i>"
                            jsonTemplate["image_car3"] = aCar.image
                            jsonTemplate["carName3"] = carName
                            rank3_car_name = carName
                            rank3Car = aCar

                    for i in range(len(row[3]['model_id'])):
                        if not i in seen:
                            rank = int(row[3]['rnk_consolidate_final'][str(i)])
                            carId = int(row[3]['model_id'][str(i)])
                            aCar = carIDMap.get(carId)
                            carName = aCar.model_make_display +" "+aCar.model_name+" ("+str(aCar.model_year)+") "
                            rankCars[str(rank)] = carName
                            # TODO, rank is not always 1
                            if rank == 2:
                                jsonTemplate["stars_car2"] = "<i class=\"fas fa-star\"></i><i class=\"fas fa-star\"></i><i class=\"fas fa-star\"></i><i class=\"far fa-star\"></i><i class=\"far fa-star\"></i>"
                                jsonTemplate["image_car2"] = aCar.image
                                jsonTemplate["carName2"] = carName
                                rank2_car_name = carName
                                rank2Car = aCar


                    jsonTemplate["line1"] = Template(jsonTemplate["line1"]).substitute(car1=rank1_car_name, car2=rank2_car_name, car3=rank3_car_name)
                    criteria = row[2]
                    criteria_rows = ""
                    line3Text = ""
                    for i in range(len(criteria)):
                        otherData = row[7]
                        displayName = criteria[i]["displayname"]
                        colName = criteria[i]["col_name"]
                        pref = "Lower the better"
                        localHighestLowest = "Lowest"
                        if criteria[0]["preference"].lower() == "false":
                            pref = "Higher the better"
                            localHighestLowest = "Highest"
                        importance = importanceArray[int(criteria[0]["importance"]) - 1]
                        criteria_rows += "<tr><td>"+displayName+"</td><td>"+pref+"</td><td>"+importance+"</td></tr>"

                        localRank1Car = None
                        localRank2Car = None
                        localRank3Car = None
                        localCriteriaValue = None
                        # otherData["rank_data"]["rnk_" + colName] = > {'0': 1.0, '1': 2.0, '2': 3.0}

                        values = otherData["rank_data"]["rnk_" + colName].values()
                        if max(values) == min(values):
                            localRank1Car = carIDMap.get(otherData["rank_data"]["model_id"]["0"])
                            localCriteriaValue = json.loads(localRank1Car.toJSON())[colName]
                            localRank2Car = carIDMap.get(otherData["rank_data"]["model_id"]["1"])
                            localRank3Car = carIDMap.get(otherData["rank_data"]["model_id"]["2"])
                        else:

                            for n in range(len(otherData["rank_data"]["rnk_" + colName])):
                                if otherData["rank_data"]["rnk_"+colName][str(n)] == min(values):
                                    localRank1Car = carIDMap.get(otherData["rank_data"]["model_id"][str(n)])
                                    localCriteriaValue = json.loads(localRank1Car.toJSON())[colName]

                            for n in range(len(otherData["rank_data"]["rnk_" + colName])):
                                if otherData["rank_data"]["rnk_" + colName][str(n)] == max(values):
                                    localRank3Car = carIDMap.get(otherData["rank_data"]["model_id"][str(n)])

                        #for Line 3
                        line3Text += Template(jsonTemplate["line3"]).substitute(criteria=displayName, car1=car1.model_make_display +" "+car1.model_name+" ("+str(car1.model_year)+") ", \
                                                                   car2=car2.model_make_display +" "+car2.model_name+" ("+str(car2.model_year)+") ",\
                                                                   car3=car3.model_make_display +" "+car3.model_name+" ("+str(car3.model_year)+") ",\
                                                                   criteriaValueCar1=str(json.loads(car1.toJSON())[criteria[i]["col_name"]]), \
                                                                   criteriaValueCar2=str(json.loads(car2.toJSON())[criteria[i]["col_name"]]), \
                                                                   criteriaValueCar3=str(json.loads(car3.toJSON())[criteria[i]["col_name"]]), \
                                                                   givenPreference=pref, carWithRank1=localRank1Car.model_make_display+" "+localRank1Car.model_name+" ("+str(localRank1Car.model_year)+") ", \
                                                                    rank1CriteriaValue=localCriteriaValue, highestOrLowest=localHighestLowest, importanceDescription=importance, \
                                                                    carWithRank3=localRank3Car.model_make_display+" "+localRank3Car.model_name+" ("+str(localRank3Car.model_year)+") "
                                                                   )

                    jsonTemplate["line3"] = line3Text
                    jsonTemplate["criteria_rows"] = criteria_rows

                    jsonTemplate["line4"] = Template(jsonTemplate["line4"]).substitute(carNameWithRank1=rank1_car_name)

                    listOfKey = [car1.model_make_display, car1.model_name, car2.model_make_display, car2.model_name, car3.model_make_display, car3.model_name]
                    relatedLinksData = getRelatedLinks(listOfKey)
                    footerLinks = ""
                    for r in range(len(relatedLinksData)):
                        linkData = relatedLinksData[r]
                        footerLinks += "<li><a href=\""+linkData["url"]+"\">"+linkData["displayText"]+"</a></li>\n"
                    jsonTemplate["footer_links"] = footerLinks
                    substitutedData = template.substitute(jsonTemplate)

                    rank1CarMake = urllib.parse.quote(rank1Car.model_make_display)
                    if not os.path.exists(rank1CarMake):
                        os.makedirs(rank1CarMake)

                    # print(str(substitutedData))
                    newFile = open(rank1CarMake+"/"+str(row[0])+".html", "x")
                    newFile.write(str(substitutedData))
                    f.close()
                    newFile.close()


    except (Exception, psycopg2.Error) as error:
        print("Error:", error)
    finally:
        if (connection):
            connection.commit()
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


if __name__ == "__main__":
    main()