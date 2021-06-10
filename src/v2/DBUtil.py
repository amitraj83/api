
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
