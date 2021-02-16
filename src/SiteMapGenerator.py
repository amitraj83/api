import urllib
import urllib.parse
import psycopg2

def main():
    connection = psycopg2.connect(user="postgres", password="postgres", host="127.0.0.1", port="5432",
                                  database="daft")
    try:
        cursor = connection.cursor()
        sqlQuery = " select url  FROM cars.car_links "
        cursor.execute(sqlQuery)
        records = cursor.fetchall()
        for row in records:
            if row[0]:
                print("<url>")
                print("    <loc>https://suggestrank.com"+urllib.parse.quote(row[0])+"</loc>")
                print("    <lastmod>2021-02-16T12:21:13+00:00</lastmod>")
                print("</url>")
                print("")
    except (Exception, psycopg2.Error) as error:
        print("Error reading data from MySQL table", error)
    finally:
        if (connection):
            connection.commit()
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


if __name__ == "__main__":
    main()