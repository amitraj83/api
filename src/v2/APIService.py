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

from src.v2 import DBUtil
from src.v2.Classes import Variant, CarWithRankAndPopularity
from src.v2.Classes import LightCarWithRank
from src.v2.Classes import Comparison
from src.v2.Classes import ComparisonCriteria
from src.v2.Classes import ComparisonPageData
from src.v2.Util import carAndRankMap
from src.v2.Util import getCategorizedSpecs
from src.v2.Util import getDescriptions



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
    query = " select car_ids, criteria, page_title, other_data from cars.car_links where id =  "+str(id)
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
        for c in criteria:
            criterias.append(ComparisonCriteria(c['id'], c['col_name'], c['displayname'], True if c['preference'] == "True" else False))

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
        carsData.append(CarWithRankAndPopularity(carId, str(car[1]).title(), str(car[2]).title(), str(car[3]).title(), "/images/"+str(car[4]), carRankMap[carId], int(car[5]), popularity))

    categorizedSpecs = []
    for detail in specDetails:
        name = detail["name"]
        if detail["car1"] == 0 or detail["car2"] == 0 or detail["car3"] == 0:
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

    comparison = ComparisonPageData(criterias, title, headPara,  threeCarsComparison, carsData, categorizedSpecs, descriptions, verdict)
    return comparison
