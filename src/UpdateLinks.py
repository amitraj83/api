import psycopg2
import json
import datetime
from TitleGenerator import generateSEOTitleDescriptionKeywords
from ContentGenerator import getHTMLContent





def main():
    connection = psycopg2.connect(user="postgres", password="postgres", host="127.0.0.1", port="5432",
                                  database="daft")
    number = None
    #, rankCriteria, rank_json, versus, category, all_ranks_json
    try:
        cursor = connection.cursor()
        cursor.execute("select id, car_ids, criteria, response, display_text, summary, page_title, other_data, url from cars.car_links where other_data::text != '{}' and criteria::text != '[]'")
        records = cursor.fetchall()

        for row in records:
            id = row[0]
            print(id)
            carsRequest = row[1]
            rank_json = json.dumps(row[3])
            versus = row[4]
            url = row[8]
            print(url)
            all_ranks_json = json.dumps(row[7]['rank_data'])
            rankCriteria = row[2]

            cursor2 = connection.cursor()

            metaData = generateSEOTitleDescriptionKeywords(all_ranks_json)
            otherData = {"rank_data":json.loads(all_ranks_json),
                         "blog_content":getHTMLContent(id, carsRequest, rankCriteria, rank_json, versus, versus, versus,
                                                       {"rank_data":json.loads(all_ranks_json)}, url, metaData['keywords'],
                                                       metaData['powerKeyword'])}

            postgres_update_query = ' UPDATE cars.car_links  SET  summary=%s, page_title=%s, other_data=%s, keywords=%s, powerkeyword=%s WHERE id = %s; '
            record_to_update = (metaData['description'], metaData['title'], json.dumps((otherData)), ', '.join(metaData['keywords']), metaData['powerKeyword'], id,)

            cursor.execute(postgres_update_query, record_to_update)


    except (Exception, psycopg2.Error) as error:
        print("Error inserting link data to MySQL table", error)
    finally:
        if (connection):
            connection.commit()
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


if __name__ == "__main__":
    main()