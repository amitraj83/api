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
from src.v2.Classes import Variant
from src.v2.Classes import LightCarWithRank
from src.v2.Classes import Comparison



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
                aComparison.append(LightCarWithRank(rankData['model_id'][str(i)], rankData['model_make_display'][str(i)], rankData['model_name'][str(i)], rankData['model_trim'][str(i)], rankData['image'][str(i)], float(rankData['rnk_consolidate'][str(i)])))
            aComparison.sort(key=lambda c: c.rank)
        if len(aComparison) >= 2:
            comparisons.append(Comparison(id, url, aComparison[0].image, aComparison[0].make, aComparison[0].model, aComparison[0].variant, aComparison[1].image, aComparison[1].make, aComparison[1].model, aComparison[1].variant))

    return comparisons