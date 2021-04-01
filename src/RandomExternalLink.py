import psycopg2

def randomExternalLink(keyword):
    connection = psycopg2.connect(user="postgres", password="postgres", host="127.0.0.1", port="5432",
                                  database="daft")
    try:
        cursor = connection.cursor()
        query = " SELECT link FROM cars.car_external_links where link ilike '%"+keyword+"%' ORDER BY RANDOM() LIMIT 1 "
        cursor.execute(query)
        records = cursor.fetchall()
        for row in records:
            return row[0]
    except (Exception, psycopg2.Error) as error:
        print("Error ", error)
    finally:
        if (connection):
            connection.commit()
            cursor.close()
            connection.close()
