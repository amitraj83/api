from string import Template
from random import randrange
import json
from v2.DBUtil import getCarComparisonUniqueNumber
from v2.DBUtil import executeInsertQuery
from v2.Classes import LightCarWithRank
from v2.Util import str2bool
import os
import urllib
import urllib.parse


allTitles = ['$powerkeyword - Which should you buy?', '$powerkeyword - Which brand is better?', '$powerkeyword - Which car is better?',
             '$powerkeyword - Battle of brands','$powerkeyword - Which one is better', '$powerkeyword - Which car is preferred?',
             '$powerkeyword - Which car is most wanted?', '$powerkeyword - Which brand is the winner', '$powerkeyword - Which one is better family car?',
             '$powerkeyword - Which one is fastest?', '$powerkeyword - Which car is cost effective?', '$powerkeyword - Which car is more powerful?', '$powerkeyword - Which car is worth buying?',
             '$powerkeyword - Which car is more reliable?']

allDescriptions = ['$powerkeyword car comparison is complicated. Big engine and more horse power not always the best. Compare cars $make1 and $make2 considering RPM, fuel economy, size and torque.',
                   '$powerkeyword usual car comparison may not suggest you right car. Our car comparison considers your situation and suggest best car for you. Check why $make1 is better/worse than $make2.',
                   '$powerkeyword car comparison. Car power depend on torque and RPM. Check if more RPM makes $make1 is better/worse than $make2. We compare cars for you only and suggest best one.',
                   '$powerkeyword compare cars side by side. Recent cars comes with manufacturer warranty and technologies. Check if such features make $make1 better than $make2.  ',
                   '$powerkeyword side by side car comparison. More torque is good for smooth drive but thats not the only think that makes $make1 better than $make2. Check which car is better?',
                   '$powerkeyword comparison side by side. Recent cars with small engine produce more power than older bigger engine. Check out if engine size makes $make1 better than $make2',
                   '$powerkeyword comparison based on engine size, torque, year, size, etc., and find out if $make1 is better than $make2. Compare cars with many other factors like engine size, torque, rpm, etc.',
                   '$powerkeyword car comparison and find the winner car. More cylinders, more piston movementm more power. Compare $make1 vs $make2 to see if car with more cylinders is best for you.',
                   'More the torque, better the drive but there are many other factors to compare $powerkeyword. Checkout if $make1 is better than $make2 and compare side by side',
                   '$powerkeyword car comparison to find which one is fastest. Having 2000cc with 3000 rpm is not the only deciding factor. Checkout if $make1 is faster and better than $make2.',
                   'Side by side comparison of $powerkeyword. Having a small engine is more fuel efficient. Is that why $make1 is more cost effective than $make2. Checkout this comparison.',
                   'Compare $powerkeyword for your needs. Compact family car not always less powerful. Checkout why car $make1 is more powerful than $make2 and is this your family car?',
                   'Not sure about $powerkeyword, checkout this comparison. Bigger engine makes car more powerful. Check if big engine makes $make1 better than $make2.']
headPara = ["To compare $powerKeyword, this blog does the comparison of $car1 vs $car2. To make the comparison realistic, a set of criteria is used as mentioned below in this blog. We compare the cars for each criteria and tell you which car is better for a which criteria, to help you decide $powerKeyword. In the end, our AI algorithm shows the final verdict considering all criteria. ",
            "This blog compares $powerKeyword. More specifically, it does the comparison of $car1 vs $car2. Unlike other comparisons, it compares and rank based on some criteria mentioned below. Best car for each criteria is mentioned as well as the best car for all criteria is also mentioned in the verdict. This blog helps you to compare $powerKeyword and find the best one for your needs.",
            "$powerKeyword comparison is not an easy one. Both the cars are good. To find out the best one precisely, this blog uses $car1 vs $car2. We don't only compare rather we rank the cars based on realistic criteria to suit your needs. For each criteria, the best car is identified. Also, overall best car is identified to answer the comparison of $powerKeyword. "]

verdict = ["While comparing $powerKeyword, our car comparison found that $carwithRank1 is the better choice. Continue reading to understand why $carwithRank1 is better."]

line1 = ["In this blog, we will compare $car1 specs and $car2 specs, and find out which one is good and why?","In this blog, lets compare $car1 specs and $car2 specs, and understand which car is better and which car to buy. We will compare all specs and trims and rank cars to suit your needs."]
line3 = ["During the $car1 review for $criteria, we found that $car1 has $criteriaValueCar1 and $car2 has $criteriaValueCar2.\n                        Because given preference is $givenPreference, it comes out that $carWithRank1 is the best because it has $criteria as $rank1CriteriaValue which is $highestOrLowest from others. And because\n  your criteria is $criteria, its $carWithRank1 weighted rank is 1 where as weighted rank of $carWithRank2 is 2\n.","Lets do $car1 review to understand if this is the best based on $criteria. $car1 has $criteriaValueCar1 and $car2 has $criteriaValueCar2.\n It was mentioned that  $criteria is $givenPreference. So, $carWithRank1 seems better than the other two cars because its $rank1CriteriaValue is $highestOrLowest from others. And because\n your criteria is $criteria, its $carWithRank1 weighted rank is 1 where as weighted rank of $carWithRank2 is 2.\n"]

line4 = ["To conclude the comparison of $powerKeyword, we compared $versus1. In this car comparison, we calculate the final rank of cars by adding all the weighted ranks of each criteria. This car comparison shows that $carNameWithRank1 stands out to be the best one becuase your important \ncriteria are best matched in this car.","In $powerKeyword comparison and ranking, we compared $versus1. We use the importance of each criteria mentioned. When we add weighted ranks, $carNameWithRank1 seems to be the best one among others because the mentioned criteria are best matched in this car."]

modelYearHigh = ["There are several benefits of new or recent cars such as manufacturer warranty if car is within 3-5 years old. Newer cars are coming with turbojet engine technology. Recent cars with low mileage is a big factor to consider. There might be very few electrical issues in recent cars. So, if you are only looking for recent cars, we suggest to go with $carWithRank1.",
                 "One of the benefits of recent car could be you get the manufacturer warranty. New cars equipped with latest technologies, sensors and fuel efficient engines. Most probably, a recent year car will have low mileage, so the car is not aged. You will be at peace of mind from several issues like electrical or engine issues. And our comparison makes $carWithRank1 the WINNER.  ",
                 "If a car is not too old, you might get the manufacturer warranty on Engine, which is a big deal. Recent cars bring several advanced technolgies like fuel efficient engines, sensors, cameras, etc. Most likely they have low mileage which means engine is not burned out. You will have a peace of mind from several issues like electrical, engine or mechanical faults. Our winner is $carWithRank1."]

modelYearLow = ["When the car is old, you will save money on purchase price. Usually, old cars are 50% cheaper than newer. Most of the depreciation has already occurred, so your resale value will still be good. If you are lucky, you will save money on insurance as well. Financing is easier as it costs lesser. You will have wide variety to select from. So, if you are not concerned about recent year, we suggest to go with $carWithRank1.",
                "The old car is cheaper, so you can save some money. Most of the depreciation happens in first 1-3 years, so no more worry of depreciation. After 1-2 years, you can resale the car almost same price as you purchased. As the car will be cheaper, finance approval will be easier. You might get a cheaper insurance based on lower car value. So, the winner is $carWithRank1.",
                "You dont need to worry about the depreciation of old car as most depreciation happens in the first 1-3 years. You might resale this car at almost its purchased price. There are several other factors on which you can save money e.g., lesser car value mean lower insurance premium. As its cheaper, your finance approval might be troublefree. Our winner is $carWithRank1."]

engineSizeHigh = ["A big engine produces more power and better performance. As a result you will get better acceleration. If your car is usually high loaded or you are travelling mostly in hilly areas, big engine is preferred. Several small engines with  advancements such as direct fuel injection, turbo charging and variable cam timing helps but big V8 mechanical engine under the hood has no match. So, if you are mostly travelling with high load, on motorways or on hilly roads, you need more power. So, we suggest to go with $carWithRank1.",
                  "If you are looking for good accelaration, a big engine is more preffered as it produces more power. If you generally travel with high load or travel in hilly areas, big engine could be a great choice. Some small engines with turbo charging or direct fuel injection may produce similar power but a big engine under the hood is un-comparable. So, if you want to make your drive smooth and powerful, its hard to decide among the two cars. But, we would suggest to go with $carWithRank1.",
                  "Big engine give more power and makes your ride smooth. The will have a good very accelaration to ride smoothly on hilly areas or on with heavy loads. Of course, fuel consumption will be higher. So, you can also opt for small engines with technologies like turbo charging or direct fuel injection which can give a good power to the car. For a family car, 2000cc usually gives a good power. So, the winner for big engine side is $carWithRank1."]

engineSizeLow = ["Modern technologies like turbo charge, direct fuel injection and ecoboost have made smaller engines to produce more power. So, smaller engine does not necessary mean low power. In addition, smaller engines come with low exhaust emission which reduces CO2 emission, so you save some money on tax. Moreover, smaller engine car insurance is usually cheaper than bigger ones. Also, small engine consume lesser fuel than bigger ones, so you can save some money on fuel. So, if you are using car mostly inside the town, going on short trips, we suggest to go with $carWithRank1.",
                 "Small engine does not necessarily means less power because some newer technologies like turbo charge and direct fuel injection and ecoboost are making small engine to produce more power. So, you do not compromise on power. On the other hand you save on CO2 emission and probably on tax as well because small engine gives less exhaust emission. In addition, small engine consume less fuel, so you can save some money on fuel as well. Overall, recent cars with small engine are quite economical. Under this criteria, the winner is $carWithRank1.",
                 "There are several benefits of small cars. Small cars are usually cost effective and fuel efficient. Some small engine with latest technologies like eco boost, turbo charge and direct fuel injection are making small engine to produce similar power as that of big engines. In addition, small cars consume less fuel so exhaust emission is also low. Effectively, you can save money on tax as several countries charge more tax if CO2 emission is high. Considering the low engine size criteria, and we would suggest to go with $carWithRank1."]

engineCylinderHigh = ["More number of cylinders, means smaller and lighter pistons required which reduces vibrations in the car. For high rev car, smaller and lighter pistons preferred, so they put less efforts on crankshaft, so overall rpm is increased. Car sound become smoooth. However, it is worth to note that it would need more engine oil to reduce friction in many cylinders. Also, it relatively costs more than cars with lesser cylinders. So, if you want smooth drive and more rpm and better acceleration, we suggest to go with $carWithRank1.",
                      "More cylinders usually comes with smaller cylinders. So, it needs smaller and lighter pistons makes it easier piston movement. So, you will have less vibrations in the car because they do not put lot of pressure on crankshaft. It also helps to increase overall rpm so you get smoother ride even on low gears with more power. However, note that more cylinders means smore friction generates so it needs more oil. If you are looking for a luxury car and needs less vibrations and more pwoer. So our recommendation would be $carWithRank1."]

engineCylinderLow = ["Lesser the number of cylinders, better is the fuel efficiency. Of course, overall cost of the car is also reduced. Lesser the cylinders, smaller the engine size which gives more space in the car interior. Lesser the cylinders, lesser the friction so lesser oil consumption. It is worth noting that lesser cylinder make less smooth. But, if you are buying a family car, fuel efficient car, need more interior space and not concerned with speed, we would suggest to go with $carWithRank1.",
                     "Lesser the cylinders, lesser the power and friction. So, overall, better fuel economy and reduced oil consumption. Moreover, the engine size will be reduced so manufacturer will put more space in the car interior. However, now the piston will have to be bigger and has to make longer movement, especially on low gears, you may experience some vibrations in the car. Overall, if you not concerned about the power and speed, and our winner is $carWithRank1."]

engineRPMHigh = ["3000 rpm means piston is moving 3000 times in one minute. So, definitely 3000 rpm produces more power than 2000 rpm engine. High rev engines are more suitable for race tracks than streets. In addition, high rev car can also give good power is lower gears. So, if you are carrying a high load in your car and need more power in lower speed, it better to have an engine which has more rpm. So, we suggest to go ahead with $carWithRank1.",
                 "Car's horse power is dependent on engine rpm and torque. More the engine rpm, the the power you get. RPM is the number of back and forth movement of a piston in one minute. More the piston moves, more air and fuel is mixed to create power. If you are looking for racing cars, or mostly carry high loads in your car and travelling in hilly areas, high rpm cars are preffered so get instant more power. For this criteria, our winner is $carWithRank1."]

engineRPMLow = ["Low RPM means lesser piston movement in one minute, so produces lesser power. But, it does not necessarily mean that car has less power. For example Diesel engines have lesser RPMs than gasoline/petrol engines. Because it makes long strokes on high compression ratios. So, overall, lower rpm engine can also provide sufficient power as compared to high rpm engine. So, we suggest to go ahead with $carWithRank1.",
                "Low rpm does not necessarily mean less power, it has to be seen with gears and speed. Lugging your engine means asking engine to do hard work. Low RPMs usually good when you are at a steady speed on just slowing down. But at the time of acceleration, low RPMs makes engine and cylinders temp rise, so your car may damage sooner. So, if you are not travelling in towns or not accelerating very often, you can go ahead with low RPM cars. In this case, the winnger is $carWithRank1. "]

moreSeats = ["No doubt that more the number of seats, more people can go in a car. So, if you are a big family or travelling with full family very often, its good to buy a car with more number of seats. However, such cars consume more fuel than the cars with less seats. Another benefits of more seats is that if you need to carry some stuff, you can fold the seats and you will have enough space for your bags. So, if you are looking for more seats, go ahead with $carWithRank1 among the two cars.",
             "If you have more seats, not only you can carry more people with you but also you will have better air conditioning and cross ventilation. You will have extra space for storage and for your comfort. You can have more leg room and hand rests, etc. However, you will have to pay extra cost of cleaning, tax, etc. So, if you are mostly travelling with many people or you need more comfort and space in the car, it advisable to with more number of seats. Here, we would advice to go with $carWithRank1."]

lessSeats = ["Less the number of seats, lesser the passengers can go in your car. Means less weight in car which increases fuel efficiency and you can save some money on fuel. If you don't have a big family or mostly travelling alone, its preferred to have a car with lesser seats. So, we suggest to go ahead with $carWithRank1.",
             "Fewer the seats means less number of passengers can go in your car. It means its a small compact car which has several benefits like better fuel efficiency, less tax and mostly cheaper than big cars. If you are travelling mostly alone, if you are a new driver or if its your first car, it is recommended to go with small car. Here, our winning car is $carWithRank1."]

lessWidth = ["There are several benefits on a small and compact cars for example, you can maneuver car easily, it is easy to park, environment friendly, easy to afford and need lesser maintenance. If you are learning to drive car or if its your first cars, its prefeered to have a small car. So, better to go ahead with $carWithRank1.",
             "If you are looking for a compact family cars, less width cars is preffered. The primary benefits are you can easily maneuver the car, easy to park and need less space to park, less fuel consumption and environment friendly, easy to afford, easy to finance as it is usually cheaper than bigger cars. If its your first car or you new driver, its preffered to go with less width compact car. Here the winner is $carWithRank1."]

moreWidth = ["Bigger cars have more internal space mean more luxury and comfort. In fact, big families prefer to have a big car so that you can carry your full family and their luggage as well. In addition, bigger car has better visbility on roads, suspensions are better, have more power and are smooth to drive. So, go ahead with $carWithRank1."]


def generatePowerKeywordAndKeywordsAndCarNames(listOfCars):
    powerKeyword = ""
    keywords = []
    carNames = []
    if len(listOfCars) == 2:
        car1Make = listOfCars[0].make
        car1Model = listOfCars[0].model
        car1Year = str(listOfCars[0].year)
        car1Variant = str(listOfCars[0].variant)
        carNames.append(car1Make+" "+car1Model)

        car2Make = listOfCars[1].make
        car2Model = listOfCars[1].model
        car2Year = str(listOfCars[1].year)
        car2Variant = str(listOfCars[1].variant)
        carNames.append(car2Make+" "+car2Model)

        if car1Make == car2Make:
            if car1Model == car2Model:
                keywords.append(car1Make + ' ' + car1Model + ' ' + car1Variant + ' vs ' + car2Make + ' ' + car2Model + ' ' + car2Variant)
                if car1Year == car2Year:
                    powerKeyword = car1Make +' '+car1Model+' '+car1Variant+' vs '+car2Make+' '+car2Model+' '+car2Variant
                else:
                    powerKeyword = car1Make + ' ' + car1Model + ' ' + car1Year + ' vs ' + car2Make + ' ' + car2Model + ' ' + car2Year
            else:
                powerKeyword = car1Make + ' ' + car1Model + ' vs ' + car2Model
                keywords.append( car1Make + ' ' + car1Model + ' vs ' + car2Make + ' ' + car2Model)
        else:
            powerKeyword = car1Make +  ' vs ' + car2Make
            keywords.append( car1Make + ' ' + car1Model + ' vs ' + car2Make + ' ' + car2Model)
        keywords.append(car1Make)
        keywords.append(car2Make)
        keywords.append(car1Make+" "+car1Model)
        keywords.append(car2Make+" "+car2Model)
    return {"powerKeyword":powerKeyword, "keywords":keywords, "carNames":carNames}

def generateSEOTitleDescriptionKeywords(rankData, rankedCarsList):
    titleRandomIndex = randrange(len(allTitles))
    descRandomIndex = randrange(len(allDescriptions))
    title = allTitles[titleRandomIndex]
    description = allDescriptions[descRandomIndex]
    listOfCars = rankedCarsList
    keywordsData = generatePowerKeywordAndKeywordsAndCarNames(listOfCars)
    newTitle = Template(title).substitute(powerkeyword=keywordsData["powerKeyword"])
    newDescription = Template(description).substitute(powerkeyword=keywordsData["powerKeyword"], make1=keywordsData["carNames"][0], make2=keywordsData["carNames"][1])
    return {'title': newTitle,'description': newDescription, 'keywords': keywordsData["keywords"], 'powerKeyword': keywordsData["powerKeyword"]}



def getHTMLContent(rankedCarsList, criteria, powerKeyword, url, rank_data):
    blogTemplateFile = os.path.join(os.getcwd(), "blog-template.json")
    car1Name = ""
    car2Name = ""
    if len(rankedCarsList) == 2:
        car1Name = rankedCarsList[0].make+" "+rankedCarsList[0].model
        car2Name = rankedCarsList[1].make+" "+rankedCarsList[1].model
    with open(blogTemplateFile, 'r') as tf:
        jsonTemplate = json.loads(tf.read())
        jsonTemplate["keywords"] = powerKeyword
        if car1Name:
            jsonTemplate["keywords"] += ", " + car1Name
        if car2Name:
            jsonTemplate["keywords"] += ", " + car2Name
        jsonTemplate["keywords"] += ", Car, compare, compare cars, compare car specs, compare car features, compare engine specifications, compare Car side by side, car comparison tool "
        jsonTemplate["pageURL"] = urllib.parse.quote(url)
        jsonTemplate["line1"] = Template(line1[randrange(len(line1))]).substitute(car1=car1Name, car2=car2Name)
        line3Text = []
        line3H3Heading = []
        for i in range(len(criteria)):

            displayName = criteria[i]["displayname"]
            colName = criteria[i]["col_name"]
            lowerTheBetter = str2bool(str(criteria[i]["preference"]))
            prefText = "Lower the better" if lowerTheBetter else "Higher the better"
            localHighestLowest = "Lowest" if lowerTheBetter else "Highest"
            line3TextValue = ""
            rank1CriteriaValue = ""
            criteriaValueCar1 = ""
            criteriaValueCar2 = ""
            h3Heading = powerKeyword + " - " + displayName
            line3H3Heading.append(h3Heading)
            rankDataJSON = json.loads(rank_data)
            winningIndex = -1
            for n in range(len(rankDataJSON['model_id'])):
                if rankedCarsList[0].id == rankDataJSON['model_id'][str(n)]:
                    winningIndex = n
                    rank1CriteriaValue = rankDataJSON[colName][str(n)]
                #check if this criteria is a comparison criteria or not
            if "rnk_"+colName in dict(rankDataJSON).keys():
                criteriaValueCar1 = rankDataJSON[colName][str(winningIndex)]
                criteriaValueCar2 = rankDataJSON[colName][str(1 if winningIndex == 0 else 0)]



            if (displayName in "Model Year") or (displayName == "Model Year"):
                if not lowerTheBetter:
                    line3TextValue = modelYearHigh[randrange(len(modelYearHigh))]
                else:
                    line3TextValue = modelYearLow[randrange(len(modelYearLow))]
                line3Text.append(Template(line3TextValue).substitute( carWithRank1=str(car1Name)))
            elif (displayName in "Engine size (cc)") or (displayName == "Engine size (cc)"):
                if not lowerTheBetter:
                    line3TextValue = engineSizeHigh[randrange(len(engineSizeHigh))]
                else:
                    line3TextValue = engineSizeLow[randrange(len(engineSizeLow))]
                line3Text.append(Template(line3TextValue).substitute(carWithRank1=str(car1Name)))
            elif (displayName in "Engine Cylinder") or (displayName == "Engine Cylinder"):
                if not lowerTheBetter:
                    line3TextValue = engineCylinderHigh[randrange(len(engineCylinderHigh))]
                else:
                    line3TextValue = engineCylinderLow[randrange(len(engineCylinderLow))]
                line3Text.append(Template(line3TextValue).substitute(carWithRank1=str(car1Name)))
            elif (displayName in "Engine power (rpm)") or (displayName == "Engine power (rpm)"):
                if not lowerTheBetter:
                    line3TextValue = engineRPMHigh[randrange(len(engineRPMHigh))]
                else:
                    line3TextValue = engineRPMLow[randrange(len(engineRPMLow))]
                line3Text.append(Template(line3TextValue).substitute(carWithRank1=str(car1Name)))
            elif (displayName in "Seats") or (displayName == "Seats"):
                if not lowerTheBetter:
                    line3TextValue = moreSeats[randrange(len(moreSeats))]
                else:
                    line3TextValue = lessSeats[randrange(len(lessSeats))]
                line3Text.append(Template(line3TextValue).substitute(carWithRank1=str(car1Name)))
            elif (displayName in "Width (mm)") or (displayName == "Width (mm)"):
                if not lowerTheBetter:
                    line3TextValue = moreWidth[randrange(len(moreWidth))]
                else:
                    line3TextValue = lessWidth[randrange(len(lessWidth))]
                line3Text.append(Template(line3TextValue).substitute(carWithRank1=str(car1Name)))

            else:
                line3TextValue = line3[randrange(2)]
                line3Text.append(Template(line3TextValue).substitute( criteria=displayName,
                                                                      car1=car1Name, \
                                                                      car2=car2Name, \
                                                                      criteriaValueCar1=criteriaValueCar1, \
                                                                      criteriaValueCar2=criteriaValueCar2, \
                                                                      givenPreference=prefText, carWithRank1=car1Name, \
                                                                      rank1CriteriaValue=rank1CriteriaValue,
                                                                      highestOrLowest=localHighestLowest,
                                                                      carWithRank2=car2Name))
        jsonTemplate["line3"] = line3Text
        jsonTemplate["line3H3Heading"] = line3H3Heading
        jsonTemplate["headPara"] = Template(headPara[randrange(len(headPara))]).substitute(powerKeyword=powerKeyword,
                                                                                           car1=car1Name,
                                                                                           car2=car2Name)
        jsonTemplate["line4"] = Template(line4[randrange(2)]).substitute(powerKeyword=powerKeyword,
                                                                         carNameWithRank1=car1Name,
                                                                         versus1=powerKeyword)
    return {"jsonTemplate":jsonTemplate, "relatedLinks":[] }


def getRankedCarsList(rankData):
    listOfCars = []
    jRankData = json.loads(rankData)
    for i in range(len(jRankData['rnk_consolidate_final'])):
        make = jRankData['model_make_display'][str(i)].replace('-', ' ')
        model = jRankData['model_name'][str(i)].replace('-', ' ')
        year = jRankData['model_year'][str(i)]
        id = jRankData['model_id'][str(i)]
        variant = jRankData['model_trim'][str(i)]
        listOfCars.append(
            LightCarWithRank(id, make, model, variant, "", jRankData['rnk_consolidate_final'][str(i)], year))

    listOfCars.sort(key=lambda x: x.rank, reverse=False)
    return listOfCars


def getCarComparisonLink(ids, all_ranks_json, rankCriteria):
    uniqueId = getCarComparisonUniqueNumber()
    rankedCarsList = getRankedCarsList(all_ranks_json)
    seoData = generateSEOTitleDescriptionKeywords(all_ranks_json, rankedCarsList)
    powerKeyword = seoData["powerKeyword"]
    description = seoData["description"]
    title = seoData["title"]
    keywords = seoData["keywords"]

    url = "/compare/cars/" + str(uniqueId) + "/" + powerKeyword.replace(" ", "-")
    htmlContent = getHTMLContent(rankedCarsList, rankCriteria, powerKeyword, url, all_ranks_json)
    otherData = {"rank_data":json.loads(all_ranks_json), "blog_content":htmlContent}

    postgres_insert_query = " INSERT INTO cars.car_links "
    postgres_insert_query += " (id, car_ids, criteria, response, display_text, summary, page_title, other_data, url, keywords, powerKeyword) "
    postgres_insert_query += " VALUES ( %s, %s, %s, %s, %s, %s, %s, %s , %s, %s, %s )"

    record_to_insert = (
    uniqueId, [int(ids.split(",")[0]), int(ids.split(",")[1])], json.dumps(rankCriteria), all_ranks_json, powerKeyword, description, title,
    json.dumps(otherData), url, ', '.join(keywords), powerKeyword,)
    executeInsertQuery(postgres_insert_query, record_to_insert)
    return url
