import requests
import psycopg2
from random import randrange
import requests
import xml.etree.ElementTree as ET


def main():

    #r = requests.get('https://www.motortrend.com/sitemap_index.xml')
    #print(r.content)
    root = ET.parse('motortrend-sitemap.xml')
    query = "INSERT INTO cars.car_external_links( link ) VALUES(%s);"
    for loc in root.iter():
        if loc.text.endswith(".xml"):
            r = requests.get(loc.text)
            newRoot = ET.fromstring(r.content)
            for newLoc in newRoot.iter():
                if newLoc.text.startswith("http"):
                    connection = psycopg2.connect(user="postgres", password="postgres", host="127.0.0.1",
                                                  port="5432",
                                                  database="daft")

                    try:
                        cursor = connection.cursor()
                        recordToInsert = (newLoc.text.lower(), )
                        cursor.execute(query, recordToInsert)
                        connection.commit()

                    except (Exception, psycopg2.Error) as error:
                        print(error)
                    finally:
                        cursor.close()




if __name__ == "__main__":
    main()