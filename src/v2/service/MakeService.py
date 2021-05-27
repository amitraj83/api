import psycopg2

from src.v2.models.Make import Make


def getAllMakes():
    connection = psycopg2.connect(user="postgres", password="postgres", host="127.0.0.1", port="5432",
                                  database="daft")
    try:
        cursor = connection.cursor()
        sql_select_Query = " SELECT distinct make FROM cars.carsdata "

        cursor = connection.cursor()
        cursor.execute(sql_select_Query)

        records = cursor.fetchall()
        allMakes = []
        for row in records:
            if row[0] != None:
                allMakes.append(row[0])
        return allMakes
    except (Exception, psycopg2.Error) as error:
        print("Error reading data from MySQL table", error)
    finally:
        if (connection):
            connection.commit()
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

