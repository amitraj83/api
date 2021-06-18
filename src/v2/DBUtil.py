
import psycopg2

def executeSelectQuery(query):
    connection = psycopg2.connect(user="postgres", password="postgres", host="127.0.0.1", port="5432",
                                  database="daft")
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    except (Exception, psycopg2.Error) as error:
        print("Error reading data from MySQL table: ", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()

def getCarComparisonUniqueNumber():
    connection = psycopg2.connect(user="postgres", password="postgres", host="127.0.0.1", port="5432",
                                  database="daft")
    try:
        cursor = connection.cursor()
        cursor.execute("select nextval('cars.car_links_id_seq'::regclass)")
        return cursor.fetchone()[0]
    except (Exception, psycopg2.Error) as error:
        print("Error while getting car comparison unique number: ", error)
    finally:
        if (connection):
            connection.commit()
            cursor.close()
            connection.close()

def executeInsertQuery(query, record_to_insert):
    connection = psycopg2.connect(user="postgres", password="postgres", host="127.0.0.1", port="5432",
                                  database="daft")
    try:
        cursor = connection.cursor()
        cursor.execute(query, record_to_insert)
        connection.commit()
    except (Exception, psycopg2.Error) as error:
        print("Error inserting data from MySQL table: ", error)
    finally:
        if (connection):
            cursor.close()
            connection.close()