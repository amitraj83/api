import requests
import psycopg2
from random import randrange
import requests
import xml.etree.ElementTree as ET


def main():

    root = ET.parse('sitemap.xml')
    query = "INSERT INTO cars.car_external_links( link ) VALUES(%s);"
    for loc in root.iter():
        if loc.text.startswith("http"):
            connection = psycopg2.connect(user="postgres", password="postgres", host="127.0.0.1",
                                          port="5432",
                                          database="daft")

            try:
                cursor = connection.cursor()
                recordToInsert = (loc.text.lower(),)
                cursor.execute(query, recordToInsert)
                connection.commit()

            except (Exception, psycopg2.Error) as error:
                print(error)
            finally:
                cursor.close()


if __name__ == "__main__":
    main()