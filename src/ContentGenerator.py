import os
import os.path
from random import randrange
from string import Template
import urllib
import urllib.parse
import psycopg2
import json
from Classes import Car
from RandomExternalLink import randomExternalLink


importanceArray = ["at all important", "Slightly important", "Important", "Fairly Important", "Very important"]

headPara = ["To compare $powerKeyword, this blog does the comparison of $car1 vs $car2 vs $car3. To make the comparison realistic, a set of criteria is used as mentioned below in this blog. We compare the cars for each criteria and tell you which car is better for a which criteria, to help you decide $powerKeyword. In the end, our AI algorithm shows the final verdict considering all criteria. ",
            "This blog compares $powerKeyword. More specifically, it does the comparison of $car1 vs $car2 vs $car3. Unlike other comparisons, it compares and rank based on some criteria mentioned below. Best car for each criteria is mentioned as well as the best car for all criteria is also mentioned in the verdict. This blog helps you to compare $powerKeyword and find the best one for your needs.",
            "$powerKeyword comparison is not an easy one. Both the cars are good. To find out the best one precisely, this blog uses $car1 vs $car2 vs $car3. We don't only compare rather we rank the cars based on realistic criteria to suit your needs. For each criteria, the best car is identified. Also, overall best car is identified to answer the comparison of $powerKeyword. "]

verdict = ["While comparing $powerKeyword, our car comparison found that $carwithRank1 is the better choice. Continue reading to understand why $carwithRank1 is better."]

line1 = ["In this blog, we will compare $car1 specs, $car2 specs and $car3 specs, and find out which one is good and why?","In this blog, lets compare $car1 specs, $car2 specs and $car3 specs, and understand which car is better and which car to buy. We will compare all specs and trims and rank cars to suit your needs."]
line3 = ["During the $car1 review for $criteria, we found that $car1 has $criteriaValueCar1 , $car2 has $criteriaValueCar2 and $car3 has $criteriaValueCar3.\n                        Because given preference is $givenPreference, it comes out that $carWithRank1 is the best because it has $criteria as $rank1CriteriaValue which is $highestOrLowest from others. And because\nyou have mentioned that $criteria is $importanceDescription, its $carWithRank1 weighted rank is 1 where as weighted rank of $carWithRank3 is 3\n.","Lets do $car1 review to understand if this is the best based on $criteria. $car1 has $criteriaValueCar1 , $car2 has $criteriaValueCar2 and $car3 has $criteriaValueCar3.\n It was mentioned that  $criteria is $givenPreference. So, $carWithRank1 seems better than the other two cars because its $rank1CriteriaValue is $highestOrLowest from others. And because\nyou have mentioned that $criteria is $importanceDescription, its $carWithRank1 weighted rank is 1 where as weighted rank of $carWithRank3 is 3.\n"]

line4 = ["To conclude the comparison of $powerKeyword, we compared $versus1, $versus2 and $versus3. In this car comparison, we calculate the final rank of cars by adding all the weighted ranks of each criteria. This car comparison shows that $carNameWithRank1 stands out to be the best one becuase your important \ncriteria are best matched in this car.","In $powerKeyword comparison and ranking, we compared $versus1, $versus2 and $versus3. We use the importance of each criteria mentioned. When we add weighted ranks, $carNameWithRank1 seems to be the best one among others because the mentioned criteria are best matched in this car."]
modelYearHigh = ["There are several benefits of new or recent cars such as manufacturer warranty if car is within 3-5 years old. Newer cars are coming with turbojet engine technology. Recent cars with low mileage is a big factor to consider. There might be very few electrical issues in recent cars. Based on this, the competing brands are $competingbrands. So, if you are only looking for recent cars, we suggest to go with $carWithRank1.",
                 "One of the benefits of recent car could be you get the manufacturer warranty. New cars equipped with latest technologies, sensors and fuel efficient engines. Most probably, a recent year car will have low mileage, so the car is not aged. You will be at peace of mind from several issues like electrical or engine issues. Considering this, the major competing brands are $competingbrands. And our comparison makes $carWithRank1 the WINNER.  ",
                 "If a car is not too old, you might get the manufacturer warranty on Engine, which is a big deal. Recent cars bring several advanced technolgies like fuel efficient engines, sensors, cameras, etc. Most likely they have low mileage which means engine is not burned out. You will have a peace of mind from several issues like electrical, engine or mechanical faults. So, the real comparison is between $competingbrands and our winner is $carWithRank1."]

modelYearLow = ["When the car is old, you will save money on purchase price. Usually, old cars are 50% cheaper than newer. Most of the depreciation has already occurred, so your resale value will still be good. If you are lucky, you will save money on insurance as well. Financing is easier as it costs lesser. You will have wide variety to select from. Based on this, the competing brands are $competingbrands. So, if you are not concerned about recent year, we suggest to go with $carWithRank1.",
                "The old car is cheaper, so you can save some money. Most of the depreciation happens in first 1-3 years, so no more worry of depreciation. After 1-2 years, you can resale the car almost same price as you purchased. As the car will be cheaper, finance approval will be easier. You might get a cheaper insurance based on lower car value. So, two competing cars are $competingbrands and the winner is $carWithRank1.",
                "You dont need to worry about the depreciation of old car as most depreciation happens in the first 1-3 years. You might resale this car at almost its purchased price. There are several other factors on which you can save money e.g., lesser car value mean lower insurance premium. As its cheaper, your finance approval might be troublefree. Only competing cars for this criteria are $competingbrands and our winner is $carWithRank1."]

engineSizeHigh = ["A big engine produces more power and better performance. As a result you will get better acceleration. If your car is usually high loaded or you are travelling mostly in hilly areas, big engine is preferred. Several small engines with  advancements such as direct fuel injection, turbo charging and variable cam timing helps but big V8 mechanical engine under the hood has no match. So, if you are mostly travelling with high load, on motorways or on hilly roads, you need more power. Based on this, the competing brands are $competingbrands. So, we suggest to go with $carWithRank1.",
                  "If you are looking for good accelaration, a big engine is more preffered as it produces more power. If you generally travel with high load or travel in hilly areas, big engine could be a great choice. Some small engines with turbo charging or direct fuel injection may produce similar power but a big engine under the hood is un-comparable. So, if you want to make your drive smooth and powerful, its hard to decide among $competingbrands. But, we would suggest to go with $carWithRank1.",
                  "Big engine give more power and makes your ride smooth. The will have a good very accelaration to ride smoothly on hilly areas or on with heavy loads. Of course, fuel consumption will be higher. So, you can also opt for small engines with technologies like turbo charging or direct fuel injection which can give a good power to the car. For a family car, 2000cc usually gives a good power. So, here the only contenders are $competingbrands and the winner for big engine side is $carWithRank1."]

engineSizeLow = ["Modern technologies like turbo charge, direct fuel injection and ecoboost have made smaller engines to produce more power. So, smaller engine does not necessary mean low power. In addition, smaller engines come with low exhaust emission which reduces CO2 emission, so you save some money on tax. Moreover, smaller engine car insurance is usually cheaper than bigger ones. Also, small engine consume lesser fuel than bigger ones, so you can save some money on fuel. Based on this, the competing brands are $competingbrands. So, if you are using car mostly inside the town, going on short trips, we suggest to go with $carWithRank1.",
                 "Small engine does not necessarily means less power because some newer technologies like turbo charge and direct fuel injection and ecoboost are making small engine to produce more power. So, you do not compromise on power. On the other hand you save on CO2 emission and probably on tax as well because small engine gives less exhaust emission. In addition, small engine consume less fuel, so you can save some money on fuel as well. Overall, recent cars with small engine are quite economical. Under this criteria, out of the competing cars $competingbrands, the winner is $carWithRank1.",
                 "There are several benefits of small cars. Small cars are usually cost effective and fuel efficient. Some small engine with latest technologies like eco boost, turbo charge and direct fuel injection are making small engine to produce similar power as that of big engines. In addition, small cars consume less fuel so exhaust emission is also low. Effectively, you can save money on tax as several countries charge more tax if CO2 emission is high. Considering the low engine size criteria, the competing brands are $competingbrands but we would suggest to go with $carWithRank1."]

engineCylinderHigh = ["More number of cylinders, means smaller and lighter pistons required which reduces vibrations in the car. For high rev car, smaller and lighter pistons preferred, so they put less efforts on crankshaft, so overall rpm is increased. Car sound become smoooth. However, it is worth to note that it would need more engine oil to reduce friction in many cylinders. Also, it relatively costs more than cars with lesser cylinders. Based on this, the competing brands are $competingbrands. So, if you want smooth drive and more rpm and better acceleration, we suggest to go with $carWithRank1.",
                      "More cylinders usually comes with smaller cylinders. So, it needs smaller and lighter pistons makes it easier piston movement. So, you will have less vibrations in the car because they do not put lot of pressure on crankshaft. It also helps to increase overall rpm so you get smoother ride even on low gears with more power. However, note that more cylinders means smore friction generates so it needs more oil. If you are looking for a luxury car and needs less vibrations and more pwoer, the compteting cars would be $competingbrands and our recommendation would be $carWithRank1."]

engineCylinderLow = ["Lesser the number of cylinders, better is the fuel efficiency. Of course, overall cost of the car is also reduced. Lesser the cylinders, smaller the engine size which gives more space in the car interior. Lesser the cylinders, lesser the friction so lesser oil consumption. It is worth noting that lesser cylinder make less smooth. But, if you are buying a family car, fuel efficient car, need more interior space and not concerned with speed, we would suggest to go with $carWithRank1 among the competing brands $competingbrands.",
                     "Lesser the cylinders, lesser the power and friction. So, overall, better fuel economy and reduced oil consumption. Moreover, the engine size will be reduced so manufacturer will put more space in the car interior. However, now the piston will have to be bigger and has to make longer movement, especially on low gears, you may experience some vibrations in the car. Overall, if you not concerned about the power and speed, the competing cars for lesser engine would be $competingbrands and our winner is $carWithRank1."]

engineRPMHigh = ["3000 rpm means piston is moving 3000 times in one minute. So, definitely 3000 rpm produces more power than 2000 rpm engine. High rev engines are more suitable for race tracks than streets. In addition, high rev car can also give good power is lower gears. So, if you are carrying a high load in your car and need more power in lower speed, it better to have an engine which has more rpm. Based on this, the competing brands are $competingbrands. So, we suggest to go ahead with $carWithRank1.",
                 "Car's horse power is dependent on engine rpm and torque. More the engine rpm, the the power you get. RPM is the number of back and forth movement of a piston in one minute. More the piston moves, more air and fuel is mixed to create power. If you are looking for racing cars, or mostly carry high loads in your car and travelling in hilly areas, high rpm cars are preffered so get instant more power. For this criteria, the competing cars are $competingbrands and our winner is $carWithRank1."]

engineRPMLow = ["Low RPM means lesser piston movement in one minute, so produces lesser power. But, it does not necessarily mean that car has less power. For example Diesel engines have lesser RPMs than gasoline/petrol engines. Because it makes long strokes on high compression ratios. So, overall, lower rpm engine can also provide sufficient power as compared to high rpm engine. Based on this, the competing brands are $competingbrands. So, we suggest to go ahead with $carWithRank1.",
                "Low rpm does not necessarily mean less power, it has to be seen with gears and speed. Lugging your engine means asking engine to do hard work. Low RPMs usually good when you are at a steady speed on just slowing down. But at the time of acceleration, low RPMs makes engine and cylinders temp rise, so your car may damage sooner. So, if you are not travelling in towns or not accelerating very often, you can go ahead with low RPM cars. In this case, the selection boils down to $competingbrands and winnger is $carWithRank1. "]

moreSeats = ["No doubt that more the number of seats, more people can go in a car. So, if you are a big family or travelling with full family very often, its good to buy a car with more number of seats. However, such cars consume more fuel than the cars with less seats. Another benefits of more seats is that if you need to carry some stuff, you can fold the seats and you will have enough space for your bags. So, if you are looking for more seats, go ahead with $carWithRank1 among the competing brands $competingbrands.",
             "If you have more seats, not only you can carry more people with you but also you will have better air conditioning and cross ventilation. You will have extra space for storage and for your comfort. You can have more leg room and hand rests, etc. However, you will have to pay extra cost of cleaning, tax, etc. So, if you are mostly travelling with many people or you need more comfort and space in the car, it advisable to with more number of seats. Here, the competing cars are $competingbrands and we would advice to go with $carWithRank1."]

lessSeats = ["Less the number of seats, lesser the passengers can go in your car. Means less weight in car which increases fuel efficiency and you can save some money on fuel. If you don't have a big family or mostly travelling alone, its preferred to have a car with lesser seats. Based on this, the competing brands are $competingbrands. So, we suggest to go ahead with $carWithRank1.",
             "Fewer the seats means less number of passengers can go in your car. It means its a small compact car which has several benefits like better fuel efficiency, less tax and mostly cheaper than big cars. If you are travelling mostly alone, if you are a new driver or if its your first car, it is recommended to go with small car. Here, the competing cars would be $competingbrands and our winning car is $carWithRank1."]

lessWidth = ["There are several benefits on a small and compact cars for example, you can maneuver car easily, it is easy to park, environment friendly, easy to afford and need lesser maintenance. If you are learning to drive car or if its your first cars, its prefeered to have a small car. Based on this, the competing brands are $competingbrands. So, better to go ahead with $carWithRank1.",
             "If you are looking for a compact family cars, less width cars is preffered. The primary benefits are you can easily maneuver the car, easy to park and need less space to park, less fuel consumption and environment friendly, easy to afford, easy to finance as it is usually cheaper than bigger cars. If its your first car or you new driver, its preffered to go with less width compact car. Here the competition boils down to $competingbrands and the winner is $carWithRank1."]

moreWidth = ["Bigger cars have more internal space mean more luxury and comfort. In fact, big families prefer to have a big car so that you can carry your full family and their luggage as well. In addition, bigger car has better visbility on roads, suspensions are better, have more power and are smooth to drive. Based on this, the competing brands are $competingbrands. So, go ahead with $carWithRank1."]
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
                # print("PostgreSQL connection is closed")



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
            # print("PostgreSQL connection is closed")


def getHTMLContent(id, car_ids, criteria, response, display_text, summary, page_title, other_data, url, keywords, powerKeyword):
    connection = psycopg2.connect(user="postgres", password="postgres", host="127.0.0.1", port="5432",
                                  database="daft")
    count = 0
    try:
        cursor = connection.cursor()
        row = [id, car_ids, criteria, json.loads(response), display_text, summary, page_title, other_data, url]

        blogTemplateFile = os.path.join(os.getcwd(),  "blog-template.json")
        with open(blogTemplateFile, 'r') as tf:
            jsonTemplate = json.loads(tf.read())


        if len(row[7]) > 0 and ('rank_data' in row[7].keys()):
            car1 = getCar(row[1][0])
            car2 = getCar(row[1][1])
            car3 = getCar(row[1][2])
            carIDMap = {row[1][0]:car1,row[1][1]:car2,row[1][2]:car3}



            jsonTemplate["title"] = row[6]
            jsonTemplate["pageURL"] = urllib.parse.quote(row[8])
            jsonTemplate["keywords"] = "Car, compare, compare cars, compare car specs, compare car features, compare engine specifications, compare Car side by side, car comparison tool, "
            description = "Compare "
            if car1:
                jsonTemplate["keywords"] += car1.model_make_display.title()  +", "
                description += car1.model_make_display.title()  + " vs "
            if car2:
                jsonTemplate["keywords"] += car2.model_make_display.title()  + ", "
                description += car2.model_make_display.title() + " vs "
            if car3:
                jsonTemplate["keywords"] += car3.model_make_display.title() + ", "
                description += car3.model_make_display.title() + " vs "
            description += "side by side and find out which car is better. See full car specs and trims. Ranks cars to decide which car to buy"
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
                carName = str(aCar.model_year)+" "+aCar.model_make_display +" "+aCar.model_name
                rankCars[str(rank)] = carName

                if rank == int(min(row[3]['rnk_consolidate_final'].values())):
                    jsonTemplate["image_car1"] = aCar.image
                    jsonTemplate["carName1"] = carName
                    seen.add(i)
                    rank1_car_name = carName
                    rank1Car = aCar

                if rank == int(max(row[3]['rnk_consolidate_final'].values())):
                    seen.add(i)
                    jsonTemplate["image_car3"] = aCar.image
                    jsonTemplate["carName3"] = carName
                    rank3_car_name = carName
                    rank3Car = aCar

            for i in range(len(row[3]['model_id'])):
                if not i in seen:
                    rank = int(row[3]['rnk_consolidate_final'][str(i)])
                    carId = int(row[3]['model_id'][str(i)])
                    aCar = carIDMap.get(carId)
                    carName = str(aCar.model_year) +" "+aCar.model_make_display +" "+aCar.model_name
                    rankCars[str(rank)] = carName

                    jsonTemplate["image_car2"] = aCar.image
                    jsonTemplate["carName2"] = carName
                    rank2_car_name = carName
                    rank2Car = aCar


            jsonTemplate["line1"] = Template(line1[randrange(2)]).substitute(car1=rank1_car_name, car2=rank2_car_name, car3=rank3_car_name)
            criteria = row[2]
            criteria_rows = ""
            line3Text = []
            randomPositionForExternalLink = randrange(len(criteria))
            line3H3Heading = []
            line3H3HeadingExternalLink = []
            for i in range(len(criteria)):
                otherData = row[7]
                displayName = criteria[i]["displayname"]
                colName = criteria[i]["col_name"]
                pref = "Lower the better"
                localHighestLowest = "Lowest"
                if criteria[i]["preference"].lower() == "false":
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

                    objectlist = [{"rank": list(values)[0],"car": otherData["rank_data"]["model_id"]["0"]} ,
                                  {"rank": list(values)[1],"car": otherData["rank_data"]["model_id"]["1"]} ,
                                  {"rank": list(values)[2],"car": otherData["rank_data"]["model_id"]["2"] }]
                    objectlist.sort(key=lambda x:x['rank'])
                    localRank1Car = carIDMap.get(objectlist[0]['car'])
                    localRank2Car = carIDMap.get(objectlist[1]['car'])
                    localRank3Car = carIDMap.get(objectlist[2]['car'])
                    localCriteriaValue = json.loads(localRank1Car.toJSON())[colName]


                #for Line 3
                competingbrands = "";
                #localRank1Car.model_make_display + " " + localRank1Car.model_name
                if localRank1Car.model_make_display == localRank2Car.model_make_display:
                    if localRank1Car.model_name == localRank2Car.model_name:
                        competingbrands = localRank1Car.model_make_display +" "+localRank1Car.model_name
                    else:
                        competingbrands = localRank1Car.model_make_display +" "+localRank1Car.model_name +" vs "+localRank2Car.model_name
                else:
                    competingbrands = localRank1Car.model_make_display +" "+localRank1Car.model_name +" vs "+localRank2Car.model_make_display +" "+localRank2Car.model_name

                h3Heading = powerKeyword +" - "+displayName
                line3H3Heading.append(h3Heading)
                line3TextValue = ""
                if i == randomPositionForExternalLink:
                    line3H3HeadingExternalLink.append(randomExternalLink(localRank1Car.model_make_display))
                else:
                    line3H3HeadingExternalLink.append("")
                if (displayName in "Model Year") or (displayName == "Model Year"):
                    if pref == "Higher the better":
                        line3TextValue = modelYearHigh[randrange(len(modelYearHigh))]
                    else:
                        line3TextValue = modelYearLow[randrange(len(modelYearLow))]
                    line3Text.append(Template(line3TextValue).substitute(competingbrands=competingbrands, carWithRank1=str(localRank1Car.model_year)+" "+localRank1Car.model_make_display+" "+localRank1Car.model_name))
                elif (displayName in "Engine size (cc)") or (displayName == "Engine size (cc)"):
                    if pref == "Higher the better":
                        line3TextValue = engineSizeHigh[randrange(len(engineSizeHigh))]
                    else:
                        line3TextValue = engineSizeLow[randrange(len(engineSizeLow))]
                    line3Text.append(Template(line3TextValue).substitute(competingbrands=competingbrands, carWithRank1=str(
                        localRank1Car.model_year) + " " + localRank1Car.model_make_display + " " + localRank1Car.model_name))
                elif (displayName in "Engine Cylinder") or (displayName == "Engine Cylinder"):
                    if pref == "Higher the better":
                        line3TextValue = engineCylinderHigh[randrange(len(engineCylinderHigh))]
                    else:
                        line3TextValue = engineCylinderLow[randrange(len(engineCylinderLow))]
                    line3Text.append(Template(line3TextValue).substitute(competingbrands=competingbrands, carWithRank1=str(
                        localRank1Car.model_year) + " " + localRank1Car.model_make_display + " " + localRank1Car.model_name))
                elif (displayName in "Engine power (rpm)") or (displayName == "Engine power (rpm)"):
                    if pref == "Higher the better":
                        line3TextValue = engineRPMHigh[randrange(len(engineRPMHigh))]
                    else:
                        line3TextValue = engineRPMLow[randrange(len(engineRPMLow))]
                    line3Text.append(Template(line3TextValue).substitute(competingbrands=competingbrands, carWithRank1=str(
                        localRank1Car.model_year) + " " + localRank1Car.model_make_display + " " + localRank1Car.model_name))
                elif (displayName in "Seats") or (displayName == "Seats"):
                    if pref == "Higher the better":
                        line3TextValue = moreSeats[randrange(len(moreSeats))]
                    else:
                        line3TextValue = lessSeats[randrange(len(lessSeats))]
                    line3Text.append(Template(line3TextValue).substitute(competingbrands=competingbrands, carWithRank1=str(
                        localRank1Car.model_year) + " " + localRank1Car.model_make_display + " " + localRank1Car.model_name))
                elif (displayName in "Width (mm)") or (displayName == "Width (mm)"):
                    if pref == "Higher the better":
                        line3TextValue = moreWidth[randrange(len(moreWidth))]
                    else:
                        line3TextValue = lessWidth[randrange(len(lessWidth))]
                    line3Text.append(Template(line3TextValue).substitute(competingbrands=competingbrands, carWithRank1=str(
                        localRank1Car.model_year) + " " + localRank1Car.model_make_display + " " + localRank1Car.model_name))

                else:
                    line3TextValue = line3[randrange(2)]
                    line3Text.append(Template(line3TextValue).substitute(h3Heading=h3Heading,criteria=displayName, car1=str(car1.model_year)+" "+car1.model_make_display +" "+car1.model_name, \
                                                           car2=str(car2.model_year)+" "+car2.model_make_display +" "+car2.model_name,\
                                                           car3=str(car3.model_year)+" "+car3.model_make_display +" "+car3.model_name,\
                                                           criteriaValueCar1=str(json.loads(car1.toJSON())[criteria[i]["col_name"]]), \
                                                           criteriaValueCar2=str(json.loads(car2.toJSON())[criteria[i]["col_name"]]), \
                                                           criteriaValueCar3=str(json.loads(car3.toJSON())[criteria[i]["col_name"]]), \
                                                           givenPreference=pref, carWithRank1=str(localRank1Car.model_year)+" "+localRank1Car.model_make_display+" "+localRank1Car.model_name, \
                                                            rank1CriteriaValue=localCriteriaValue, highestOrLowest=localHighestLowest, importanceDescription=importance, \
                                                            carWithRank3=str(localRank3Car.model_year)+" "+localRank3Car.model_make_display+" "+localRank3Car.model_name
                                                           ))

            jsonTemplate["line3"] = line3Text
            jsonTemplate["line3H3Heading"] = line3H3Heading
            jsonTemplate["line3H3HeadingExternalLink"] = line3H3HeadingExternalLink
            jsonTemplate["criteria_rows"] = criteria_rows
            jsonTemplate["headPara"] = Template(headPara[randrange(len(headPara))]).substitute(powerKeyword=powerKeyword, car1=car1.model_make_display +" "+car1.model_name, car2=car2.model_make_display +" "+car2.model_name, car3=car3.model_make_display +" "+car3.model_name)
            versus1 = ""
            versus2 = ""
            versus3 = ""
            if (car1.model_make_display == car2.model_make_display and car2.model_make_display == car3.model_make_display):
                versus1 = car1.model_make_display +" "+car1.model_name+" vs "+car2.model_name
                versus2 = car1.model_make_display +" "+car1.model_name+" vs "+car3.model_name
                versus3 = car1.model_make_display +" "+car2.model_name+" vs "+car3.model_name
            else:
                versus1 = car1.model_make_display + " " + car1.model_name + " vs " +car2.model_make_display + " " + car2.model_name
                versus2 = car1.model_make_display + " " + car1.model_name + " vs " +car3.model_make_display + " " + car3.model_name
                versus3 = car2.model_make_display + " " + car2.model_name + " vs " +car3.model_make_display + " " + car3.model_name
            jsonTemplate["line4"] = Template(line4[randrange(2)]).substitute(powerKeyword=powerKeyword,carNameWithRank1=rank1_car_name, versus1=versus1, versus2=versus2, versus3=versus3)

            listOfKey = [car1.model_make_display, car1.model_name, car2.model_make_display, car2.model_name, car3.model_make_display, car3.model_name]
            relatedLinksData = getRelatedLinks(listOfKey)

            count += 1
            # print("generate: " + str(substitutedData))

            return {"jsonTemplate":jsonTemplate, "relatedLinks":relatedLinksData }

        # print("Total Generated: "+str(count))
    except (Exception, psycopg2.Error) as error:
        print("Error:", error)
    finally:
        if (connection):
            connection.commit()
            cursor.close()
            connection.close()
            # print("PostgreSQL connection is closed")

