import requests
import psycopg2

def main():
    connection = psycopg2.connect(user="postgres", password="postgres", host="127.0.0.1", port="5432",
                                  database="daft")
    try:
        cursor = connection.cursor()
        for i in range(100):
            sqlQuery = "select model_id from cars.car ORDER BY RANDOM() LIMIT 3;"
            cursor.execute(sqlQuery)
            records = cursor.fetchall()
            listOfCars = []
            for row in records:
                listOfCars.append(row[0])
            print(str(listOfCars))
            response = requests.post('https://suggestrank.com/api/compare/cars', data='{"criteria":[[{"id":5353,"col_name":"model_engine_cc","displayname":"Engine size (cc)","preference":"False","importance":"5"},{"id":5217,"col_name":"model_weight_kg","displayname":"Weight (Kg)","preference":"False","importance":"3"}]],"cars":'+str(listOfCars)+'}')
            print(response.json())
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