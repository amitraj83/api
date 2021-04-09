import os
import os.path
from random import randrange
from string import Template
import urllib
import urllib.parse
import psycopg2
import json


def main():
    connection = psycopg2.connect(user="postgres", password="postgres", host="127.0.0.1", port="5432",
                                  database="daft")
    try:
        cursor = connection.cursor()
        sqlQuery = " select car_ids, id, url from cars.car_links "
        cursor.execute(sqlQuery)
        records = cursor.fetchall()
        results = []
        f = open("deletedurls.csv", "x")
        for row in records:
            if len(row) > 0:
                car1id = row[0][0]
                car2id = row[0][1]
                car3id = row[0][2]
                nameQuery = " select count (distinct model_make_display||model_name) from cars.car where model_id in " +str(row[0]).replace('[', '(').replace(']',')')
                cursor2 = connection.cursor()
                cursor2.execute(nameQuery)
                count = int(cursor2.fetchone()[0])
                if count != 3:
                    f.write('{},{}\r\n'.format(row[1], row[2]))
                    cursor3 = connection.cursor()
                    cursor3.execute(" delete from cars.car_links where id = "+str(row[1]))
                    cursor3.close()
                cursor2.close()
        f.close()
    except (Exception, psycopg2.Error) as error:
        print("Error reading data from MySQL table", error)
    finally:
        if (connection):
            connection.commit()
            cursor.close()
            connection.close()
            # print("PostgreSQL connection is closed")


if __name__ == "__main__":
    main()