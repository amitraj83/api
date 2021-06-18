import numpy as np
import pandas as pd


defaultCarComparisonCriteria = [
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



def compareTwoCars(data, rankCriteria):
    rank_json = {}
    if data:
        allData = []
        for eachCar in data:
            allData.append(eachCar.__dict__)
        cars = pd.DataFrame(allData)

        totalWgt = 0
        criteria = []

        if rankCriteria != None and len(rankCriteria) > 0:
            criteria = rankCriteria
        else:
            criteria = defaultCarComparisonCriteria

        rankCriteriaColumns = []
        for i in range(len(criteria)):
            cars['rnk_'+criteria[i]['col_name']] = cars[criteria[i]['col_name']].rank(ascending=(criteria[i]['preference'] == "True"))
            totalWgt += int(criteria[0]['importance'])
            rankCriteriaColumns.append('rnk_'+criteria[i]['col_name'])

        if totalWgt != 0:
            for i in range(len(criteria)):
                cars['wgt_' + criteria[i]['col_name']] = int(criteria[i]['importance']) / totalWgt

        rankConsolidate = 0
        for i in range(len(criteria)):
            rankConsolidate += cars['rnk_' + criteria[i]['col_name']] * cars[
                'wgt_' + criteria[i]['col_name']]
        cars['rnk_consolidate'] = rankConsolidate

        cars['rnk_consolidate_final'] = cars['rnk_consolidate'].rank()
        dataPointsArray = ['rnk_consolidate_final', 'model_id','model_make_id','model_name','model_trim','model_year','model_body','model_engine_position','model_engine_cc','model_engine_cyl','model_engine_type','model_engine_valves_per_cyl','model_engine_power_ps','model_engine_power_rpm','model_engine_torque_nm','model_engine_torque_rpm','model_engine_bore_mm','model_engine_stroke_mm','model_engine_compression','model_engine_fuel','model_top_speed_kph','model_0_to_100_kph','model_drive','model_transmission_type','model_seats','model_doors','model_weight_kg','model_length_mm','model_width_mm','model_height_mm','model_wheelbase_mm','model_lkm_hwy','model_lkm_mixed','model_lkm_city','model_fuel_cap_l','model_sold_in_us','model_co2','model_make_display','image']
        for i in range(len(rankCriteriaColumns)):
            dataPointsArray.append(rankCriteriaColumns[i])
        cars_ranks = cars[dataPointsArray]
        rank_json = cars_ranks.to_json()
    return rank_json