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