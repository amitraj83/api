import requests
import psycopg2
from random import randrange

def main():
    connection = psycopg2.connect(user="postgres", password="postgres", host="127.0.0.1", port="5432",
                                  database="daft")
    try:
        yearsArray = [2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008, 2007, 2006, 2005, 2004, 2003, 2002, 2001]
        makesArray = ["westfield", "daewoo", "McLaren", "hummer", "mg", "Ford","Ford","Ford","Ford","Ford","Ford","Ford","Ford", "xedos", "oldsmobile", "reliant", "Dodge", "Maserati", "Maserati", "Maserati", "Maserati", "Maserati", "Maserati", "Maserati", "Maserati", "Infiniti", "ac", "checker", "tatra", "Audi", "Lexus", "Audi", "Lexus", "Audi", "Lexus", "Audi", "Lexus", "Audi", "Lexus", "Audi", "Lexus", "Audi", "Lexus", "Audi", "Lexus", "Audi", "Lexus", "Audi", "Lexus", "Audi", "Lexus", "tvr", "simca", "avanti", "willys-overland", "Jeep", "alpina", "Cadillac", "samsung", "dacia", "bizzarrini", "gaz", "panoz", "italdesign", "riley", "lotus", "abarth", "brilliance", "monteverdi", "GMC", "Lincoln", "ascari", "Honda", "Honda", "Honda", "Honda", "Honda", "Honda", "Honda", "Honda", "Honda", "Honda", "Honda", "Honda", "Honda", "singer", "autobianchi", "holden", "Chevrolet", "dkw", "seat", "pontiac", "seat", "pontiac", "seat", "pontiac", "seat", "pontiac", "seat", "pontiac", "seat", "pontiac", "Porsche", "caterham", "Rolls-Royce", "Rolls-Royce", "Rolls-Royce", "Rolls-Royce", "Rolls-Royce", "Rolls-Royce", "Rolls-Royce", "Rolls-Royce", "Rolls-Royce", "Rolls-Royce", "Rolls-Royce", "Rolls-Royce", "donkervoort", "Jaguar", "zenvo", "Kia", "Kia", "Kia", "Kia", "Kia", "Kia", "Kia", "Kia", "Kia", "Kia", "Kia", "Kia", "Kia", "Kia", "alpine", "packard", "mercury", "humber", "plymouth", "mahindra", "Buick", "saturn", "marcos", "isuzu", "zaz", "datsun", "matra-simca", "peugeot", "daimler", "Toyota", "peugeot", "daimler", "Toyota", "peugeot", "daimler", "Toyota", "peugeot", "daimler", "Toyota", "peugeot", "daimler", "Toyota", "peugeot", "daimler", "Toyota", "peugeot", "daimler", "Toyota", "peugeot", "daimler", "Toyota", "peugeot", "daimler", "Toyota", "peugeot", "daimler", "Toyota", "peugeot", "daimler", "Toyota", "peugeot", "daimler", "Toyota", "fisker", "auverland", "armstrong-siddeley", "citroen", "saleen", "vauxhall", "saab", "renault", "vauxhall", "saab", "renault", "vauxhall", "saab", "renault", "vauxhall", "saab", "renault", "vauxhall", "saab", "renault", "vauxhall", "saab", "renault", "vauxhall", "saab", "renault", "vauxhall", "saab", "renault", "vauxhall", "saab", "renault", "vauxhall", "saab", "renault", "vauxhall", "saab", "renault", "vector", "MINI", "talbot", "Bentley", "morgan", "zil", "proton", "lada", "studebaker", "sunbeam", "trabant", "suzuki", "suzuki", "suzuki", "suzuki", "suzuki", "suzuki", "suzuki", "suzuki", "mcc", "allard", "triumph", "pininfarina", "beijing", "nsu", "de-tomaso", "austin-healey", "Volvo", "tesla", "Volvo", "tesla", "Volvo", "tesla", "Volvo", "tesla", "Volvo", "tesla", "Volvo", "tesla", "Volvo", "tesla", "Volvo", "tesla", "Volvo", "tesla", "Volvo", "tesla", "Volvo", "tesla", "eagle", "Acura", "venturi", "hudson", "pagani", "spyker", "Aston Martin", "Mitsubishi", "Aston Martin", "Mitsubishi", "Aston Martin", "Mitsubishi", "Aston Martin", "Mitsubishi", "daf", "maybach", "austin", "ginetta", "ssangyong", "Chrysler", "ariel", "Ram", "berkeley", "noble", "Scion", "morris", "jensen", "innocenti", "bugatti", "bugatti", "bugatti", "bugatti", "bugatti", "bugatti", "bugatti", "bugatti", "zastava", "steyr", "geely", "lancia", "Alfa Romeo",  "Alfa Romeo",  "Alfa Romeo",  "Alfa Romeo",  "Alfa Romeo", "smart", "tata", "skoda", "tata", "skoda", "tata", "skoda", "tata", "skoda", "tata", "skoda", "tata", "skoda", "tata", "skoda", "tata", "skoda", "tata", "skoda", "tata", "skoda", "koenigsegg", "bristol", "rover", "Mercedes-Benz", "Lamborghini", "rover", "Mercedes-Benz", "Lamborghini", "rover", "Mercedes-Benz", "Lamborghini", "rover", "Mercedes-Benz", "Lamborghini", "rover", "Mercedes-Benz", "Lamborghini", "rover", "Mercedes-Benz", "Lamborghini", "rover", "Mercedes-Benz", "Lamborghini", "rover", "Mercedes-Benz", "Lamborghini", "rover", "Mercedes-Benz", "Lamborghini", "rover", "Mercedes-Benz", "Lamborghini", "rover", "Mercedes-Benz", "Lamborghini", "rover", "Mercedes-Benz", "Lamborghini", "rover", "Mercedes-Benz", "Lamborghini", "rover", "Mercedes-Benz", "Lamborghini", "rover", "Mercedes-Benz", "Lamborghini", "rover", "Mercedes-Benz", "Lamborghini", "bitter", "Land Rover", "Land Rover", "Land Rover", "Land Rover", "Land Rover", "Land Rover", "Land Rover", "Land Rover", "Land Rover", "Land Rover", "zagato", "Nissan", "Nissan", "Nissan", "Nissan", "Nissan", "Nissan", "Nissan", "Nissan", "Nissan", "Nissan", "Nissan", "Nissan", "Nissan", "Nissan", "Nissan", "Nissan", "Nissan", "Nissan", "alvis", "lotec", "Hyundai", "Hyundai", "Hyundai", "Hyundai", "Hyundai", "Hyundai", "Hyundai", "Hyundai", "Hyundai", "Hyundai", "Hyundai", "Hyundai", "Hyundai", "Hyundai", "Hyundai", "Hyundai", "Hyundai", "Hyundai", "Hyundai", "luxgen", "ssc", "moretti", "FIAT", "FIAT", "FIAT", "FIAT", "FIAT", "FIAT", "FIAT", "FIAT", "FIAT", "FIAT", "FIAT", "Subaru", "wartburg", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "daihatsu", "amc", "fairthorpe"]
        cursor = connection.cursor()
        cursor2 = connection.cursor()
        count = 0
        totalIterations = 0;
        while count < 5 and totalIterations < 50000:
            totalIterations += 1
            # print("Total Iterations: ", totalIterations)

            year = yearsArray[randrange(len(yearsArray) - 1)]
            make = makesArray[randrange(len(makesArray) - 1)]
            print(make)
            sqlQuery = "select model_id from cars.car where model_make_id = '"+make+"' and model_year = "+str(year)+"  ORDER BY RANDOM() LIMIT 3;"
            cursor.execute(sqlQuery)
            records = cursor.fetchall()
            listOfCars = []
            for row in records:
                listOfCars.append(row[0])
            carsCheckStr = "'{"
            COMMA = ","
            for j in range(len(listOfCars)):
                if j == len(listOfCars)-1:
                    COMMA = ""
                carsCheckStr += str(int(listOfCars[j]))+COMMA
            carsCheckStr += "}'"
            carsCheckQuery = " select count(*) as found  from cars.car_links where car_ids::text = "+carsCheckStr+" "
            # print(carsCheckQuery)
            cursor2.execute(carsCheckQuery)
            carCheckRecords = cursor2.fetchall()
            if carCheckRecords[0] and int(carCheckRecords[0][0]) > 0:
                print("Existing record found")
            else:
                if len(listOfCars) == 3:

                    # print(str(listOfCars))
                    response = requests.post('http://localhost:5000/api/compare/cars', data='{"criteria":[{"id":880,"col_name":"model_year","displayname":"Model Year","preference":"False","importance":"5"},{"id":8900,"col_name":"model_engine_cc","displayname":"Engine size (cc)","preference":"False","importance":"5"},{"id":6294,"col_name":"model_engine_cyl","displayname":"Engine Cylinder","preference":"False","importance":"3"},{"id":367,"col_name":"model_engine_power_rpm","displayname":"Engine power (rpm)","preference":"False","importance":"2"},{"id":8245,"col_name":"model_engine_torque_rpm","displayname":"Engine Torque (rpm)","preference":"False","importance":"2"},{"id":1234,"col_name":"model_seats","displayname":"Seats","preference":"True","importance":"4"},{"id":4567,"col_name":"model_doors","displayname":"Doors","preference":"True","importance":"3"},{"id":765,"col_name":"model_width_mm","displayname":"Width (mm)","preference":"True","importance":"5"},{"id":3756,"col_name":"model_height_mm","displayname":"Height (mm)","preference":"True","importance":"5"}],"cars":'+str(listOfCars)+'}')
                    count += 1
                    # print(response.json())
                    # print(count)
            print("Total Comparisons: ", count, totalIterations)
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