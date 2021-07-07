
from random import randrange


from v2 import DBUtil
from v2.Classes import Variant, CarWithRankAndPopularity, Car
from v2.Classes import LightCarWithRank
from v2.Classes import Comparison
from v2.Classes import ComparisonCriteria
from v2.Classes import ComparisonPageData
from v2.Util import carAndRankMap
from v2.Util import getCategorizedSpecs
from v2.Util import getDescriptions
from v2.PandaCarCompare import compareTwoCars, defaultCarComparisonCriteria
from v2.CarCompareLinkGenerator import getCarComparisonLink




def getAllMakes():
    query = " SELECT model_make_id,  SUM( popularity ) as p FROM cars.car GROUP BY model_make_id ORDER BY p desc  "
    records = DBUtil.executeSelectQuery(query)
    allMakes = []
    for row in records:
        allMakes.append(row[0].title())
    return allMakes

def getAllModels(make):
    query = " SELECT	model_name,  SUM( popularity ) as p FROM cars.car where lower(model_make_id) = lower('"+str(make)+"') GROUP BY model_name   ORDER BY p desc;  "
    records = DBUtil.executeSelectQuery(query)
    allModels = []
    for row in records:
        allModels.append(row[0].title())
    return allModels


def getVariants(make, model):
    query = " select model_id, model_year ||' - '|| model_trim from cars.car where lower(model_make_id) = lower('"+make+"') and lower(model_name) = lower('"+model+"') and model_trim != '' order by model_year desc "
    records = DBUtil.executeSelectQuery(query)
    allVariants = []
    for row in records:
        allVariants.append(Variant(int(row[0]), row[1]) )
    return allVariants


def getPopularComparisons(page):
    query = " select id, url, other_data  from cars.car_links order by id desc offset "+str((int(page)-1) * 4)+" limit 4 "
    records = DBUtil.executeSelectQuery(query)
    comparisons = []
    for row in records:
        id = row[0]
        url = row[1]
        response = row[2]
        aComparison = []
        if response and response['rank_data']:
            rankData = response['rank_data']

            for i in range(len(rankData['model_id'])):
                aComparison.append(LightCarWithRank(rankData['model_id'][str(i)], rankData['model_make_display'][str(i)], rankData['model_name'][str(i)], rankData['model_trim'][str(i)], rankData['image'][str(i)], float(rankData['rnk_consolidate'][str(i)]), rankData['model_year'][str(i)]))
            aComparison.sort(key=lambda c: c.rank)
        if len(aComparison) >= 2:
            comparisons.append(Comparison(id, url, aComparison[0].image, aComparison[0].make, aComparison[0].model, aComparison[0].variant, aComparison[1].image, aComparison[1].make, aComparison[1].model, aComparison[1].variant))

    return comparisons


def getComparisonResult(id):
    query = " select car_ids, criteria, page_title, other_data, url from cars.car_links where id =  "+str(id)
    records = DBUtil.executeSelectQuery(query)
    comparison = None
    criterias = []
    title = ""
    headPara = ""
    threeCarsComparison = False
    carDetailsWhereClause = None
    carRankMap = None
    specDetails = []
    descriptions = []
    verdict = ""
    url = ""
    for row in records:
        carIDs = row[0]
        if len(carIDs) > 2:
            threeCarsComparison = True
        carDetailsWhereClause = str(carIDs).replace("[", "(").replace("]", ")")
        criteria = row[1]
        title = row[2]
        otherData = row[3]
        carRankMap = carAndRankMap(otherData['rank_data'])
        specDetails = getCategorizedSpecs(otherData['rank_data'])
        descriptions = getDescriptions(otherData['blog_content'])
        verdict = otherData['blog_content']["jsonTemplate"]["line4"]
        headPara = otherData['blog_content']['jsonTemplate']['headPara']
        url = row[4]
        for c in criteria:
            criterias.append(ComparisonCriteria(c['col_name'], c['col_name'], c['displayname'], True if (c['preference'] == "True" or c['preference'] == True) else False))

    if carDetailsWhereClause == None:
        return

    categoryQuery = " select col_name, display_name, category from cars.criteria where category != 'NoDisplay' "
    categoryQueryRecords = DBUtil.executeSelectQuery(categoryQuery)
    categoryDict = {}
    for cat in categoryQueryRecords:
        categoryDict[cat[0]] = {"displayName":cat[1], "category":cat[2]}

    carQuery = " select model_id, model_make_id, model_name, model_trim, image, model_year, popularity from cars.car where model_id in  "+carDetailsWhereClause
    carQueryRecords = DBUtil.executeSelectQuery(carQuery)
    carsData = []

    for car in carQueryRecords:
        carId = int(car[0])
        popularity = int(car[6])
        if popularity == 0:
            popularity = randrange(30,60)
        trim = ""
        if len(car) >= 4:
            trim = str(car[3]).title()
        print(    int(car[5]), popularity)
        carsData.append(CarWithRankAndPopularity(carId, str(car[1]).title(), str(car[2]).title(), trim, "/images/"+str(car[4]), carRankMap[carId], int(car[5]), popularity))

    categorizedSpecs = []
    for detail in specDetails:
        name = detail["name"]
        if 'car1' in detail and 'car2' in detail and 'car3' in detail:
            if detail["car1"] == 0 or detail["car2"] == 0 or detail["car3"] == 0:
                continue
        elif 'car1' in detail and 'car2' in detail:
            if detail["car1"] == 0 or detail["car2"] == 0:
                continue
        if name in list(categoryDict.keys()):
            category = categoryDict[name]['category']
            displayName = categoryDict[name]['displayName']

            categoryObjectFound = False
            for cs in categorizedSpecs:
                if str(cs["categoryName"]).lower() == str(category).lower():
                    detail["name"] = displayName
                    cs["details"].append(detail)
                    categoryObjectFound = True
            if categoryObjectFound == False:
                detail["name"] = displayName
                categorizedSpecs.append({"categoryName":category, "details":[detail]})

    comparison = ComparisonPageData(criterias, title, headPara,  threeCarsComparison, carsData, categorizedSpecs, descriptions, verdict, url)
    return comparison


def getCarComparisonFeatures():
    query = " select col_name, display_name, category, lower_is_better from cars.criteria where is_comparison_feature=true "
    queryRecords = DBUtil.executeSelectQuery(query)
    features = {}

    for feature in queryRecords:
        category = feature[2]
        if not (category in features.keys()):
            features[category] = []
        features[category].append({"id":feature[0], "displayName":feature[1], "lowerIsBetter":feature[3], "included":True})
    return features


def getLightCarDetailsWithoutRank(id):
    query = " select model_id, model_make_id, model_name, model_trim, image, model_year from cars.car where model_id = "+str(id)
    queryRecords = DBUtil.executeSelectQuery(query)
    for row in queryRecords:
        return LightCarWithRank(row[0], str(row[1]).title(),  str(row[2]).title(), row[3], row[4], 0, row[5])
    return {}

def convertCarIDsIntoPGList(ids):
    pgList = []
    for i in range(len(ids)):
        pgList.append(int(ids[i]))
    return str(pgList).replace("[", " ( ").replace("]"," ) ")

def makeCarCompareData(ids):
    if len(str(ids).split(",")) > 2:
        return {}

    whereClause = " where model_id in "+convertCarIDsIntoPGList(str(ids).split(","))
    print(whereClause)
    query = " select model_id, model_make_id, model_name, model_trim, model_year, model_body, model_engine_position, model_engine_cc, model_engine_cyl, model_engine_type, model_engine_valves_per_cyl, model_engine_power_ps, model_engine_power_rpm, model_engine_torque_nm, model_engine_torque_rpm, model_engine_bore_mm, model_engine_stroke_mm, model_engine_compression, model_engine_fuel, model_top_speed_kph, model_0_to_100_kph, model_drive, model_transmission_type, model_seats, model_doors, model_weight_kg, model_length_mm, model_width_mm, model_height_mm, model_wheelbase_mm, model_lkm_hwy, model_lkm_mixed, model_lkm_city, model_fuel_cap_l, model_sold_in_us, model_co2, model_make_display, image from cars.car   "+whereClause
    print(query)
    queryRecords = DBUtil.executeSelectQuery(query)
    data = []
    for row in queryRecords:
        data.append(
            Car(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11],
                row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19], row[20], row[21], row[22],
                row[23], row[24], row[25], row[26], row[27], row[28], row[29], row[30], row[31], row[32], row[33],
                row[34], row[35], row[36], row[37]))
    return data

def compareCars(ids, rankCriteria):
    rank_json = {}
    criteria = rankCriteria
    if criteria == None or len(criteria) == 0:
        criteria = defaultCarComparisonCriteria
    carCompareData = makeCarCompareData(ids)
    rank_json = compareTwoCars(carCompareData, criteria)
    url = getCarComparisonLink(ids, rank_json, criteria)
    return {"pushUrl":url}
