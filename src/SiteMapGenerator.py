import urllib
import urllib.parse
import psycopg2
import datetime
import os

# uiPath = "/root/car-compare/ui-app"
uiPath = "C:/house-idea/code/ui-app/"

def main():
    connection = psycopg2.connect(user="postgres", password="postgres", host="127.0.0.1", port="5432",
                                  database="daft")
    try:
        cursor = connection.cursor()
        sqlQuery = " select url FROM cars.car_links  order by car_links.id desc LIMIT 11000 "
        cursor.execute(sqlQuery)
        records = cursor.fetchall()
        dt = "2021-09-09T12:10:13+00:00"
        sitemap = open("/root/car-compare/ui/public/sitemap2.xml", "w+")
        sitemap.write("<?xml version = \"1.0\" encoding = \"UTF-8\" ?>\n")
        sitemap.write("<urlset\n")
        sitemap.write("xmlns = \"http://www.sitemaps.org/schemas/sitemap/0.9\"\n")
        sitemap.write("xmlns:xsi = \"http://www.w3.org/2001/XMLSchema-instance\"\n")
        sitemap.write("xsi:schemaLocation = \"http://www.sitemaps.org/schemas/sitemap/0.9 http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd\">\n")

        sitemap.write("<url>\n")
        sitemap.write("    <loc>https://suggestrank.com/</loc>\n")
        sitemap.write("    <lastmod>" + dt + "</lastmod>\n")
        sitemap.write("</url>\n")
        sitemap.write("\n")

        for row in records:
            if row[0]:
                sitemap.write("<url>\n")
                sitemap.write("    <loc>https://suggestrank.com"+urllib.parse.quote(row[0])+"</loc>\n")
                sitemap.write("    <lastmod>"+dt+"</lastmod>\n")
                sitemap.write("</url>\n")
                sitemap.write("\n")

        sitemap.write("</urlset>")
        sitemap.close()

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
