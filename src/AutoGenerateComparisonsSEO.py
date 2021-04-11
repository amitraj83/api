import requests
import psycopg2
from random import randrange

def main():
    connection = psycopg2.connect(user="postgres", password="postgres", host="127.0.0.1", port="5432",
                                  database="daft")
    try:
        yearsArray = [2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011, 2010, 2009, 2008, 2007, 2006, 2005, 2004, 2003, 2002, 2001]
        makesArray = ["McLaren", "hummer", "Ford","Ford","Ford","Ford","Ford","Ford","Ford","Ford", "oldsmobile", "reliant", "Dodge", "Maserati", "Maserati", "Maserati", "Maserati", "Maserati", "Maserati", "Maserati", "Maserati", "Infiniti", "ac", "checker", "tatra", "Audi", "Lexus", "Audi", "Lexus", "Audi", "Lexus", "Audi", "Lexus", "Audi", "Lexus", "Audi", "Lexus", "Audi", "Lexus", "Audi", "Lexus", "Audi", "Lexus", "Audi", "Lexus", "Audi", "Lexus", "tvr", "simca", "avanti", "willys-overland", "Jeep", "alpina", "Cadillac", "samsung", "dacia", "bizzarrini", "gaz", "panoz", "italdesign", "riley", "lotus", "abarth", "brilliance", "monteverdi", "GMC", "Lincoln", "ascari", "Honda", "Honda", "Honda", "Honda", "Honda", "Honda", "Honda", "Honda", "Honda", "Honda", "Honda", "Honda", "Honda", "singer", "autobianchi", "holden", "Chevrolet", "dkw", "seat", "pontiac", "seat", "pontiac", "seat", "pontiac", "seat", "pontiac", "seat", "pontiac", "seat", "pontiac", "Porsche", "caterham", "Rolls-Royce", "Rolls-Royce", "Rolls-Royce", "Rolls-Royce", "Rolls-Royce", "Rolls-Royce", "Rolls-Royce", "Rolls-Royce", "Rolls-Royce", "Rolls-Royce", "Rolls-Royce", "Rolls-Royce", "donkervoort", "Jaguar", "zenvo", "Kia", "Kia", "Kia", "Kia", "Kia", "Kia", "Kia", "Kia", "Kia", "Kia", "Kia", "Kia", "Kia", "Kia", "alpine", "packard", "mercury", "humber", "plymouth", "mahindra", "Buick", "saturn", "marcos", "isuzu", "zaz", "datsun", "matra-simca", "peugeot", "daimler", "Toyota", "peugeot", "daimler", "Toyota", "peugeot", "daimler", "Toyota", "peugeot", "daimler", "Toyota", "peugeot", "daimler", "Toyota", "peugeot", "daimler", "Toyota", "peugeot", "daimler", "Toyota", "peugeot", "daimler", "Toyota", "peugeot", "daimler", "Toyota", "peugeot", "daimler", "Toyota", "peugeot", "daimler", "Toyota", "peugeot", "daimler", "Toyota", "fisker", "auverland", "armstrong-siddeley", "citroen", "saleen", "vauxhall", "saab", "renault", "vauxhall", "saab", "renault", "vauxhall", "saab", "renault", "vauxhall", "saab", "renault", "vauxhall", "saab", "renault", "vauxhall", "saab", "renault", "vauxhall", "saab", "renault", "vauxhall", "saab", "renault", "vauxhall", "saab", "renault", "vauxhall", "saab", "renault", "vauxhall", "saab", "renault", "vector", "MINI", "talbot", "Bentley", "morgan", "zil", "proton", "lada", "studebaker", "sunbeam", "trabant", "suzuki", "suzuki", "suzuki", "suzuki", "suzuki", "suzuki", "suzuki", "suzuki", "mcc", "allard", "triumph", "pininfarina", "beijing", "nsu", "de-tomaso", "austin-healey", "Volvo", "tesla", "Volvo", "tesla", "Volvo", "tesla", "Volvo", "tesla", "Volvo", "tesla", "Volvo", "tesla", "Volvo", "tesla", "Volvo", "tesla", "Volvo", "tesla", "Volvo", "tesla", "Volvo", "tesla", "eagle", "Acura", "venturi", "hudson", "pagani", "spyker", "Aston Martin", "Mitsubishi", "Aston Martin", "Mitsubishi", "Aston Martin", "Mitsubishi", "Aston Martin", "Mitsubishi", "daf", "maybach", "austin", "ginetta", "ssangyong", "Chrysler", "ariel", "Ram", "berkeley", "noble", "Scion", "morris", "jensen", "innocenti", "bugatti", "bugatti", "bugatti", "bugatti", "bugatti", "bugatti", "bugatti", "bugatti", "zastava", "steyr", "geely", "lancia", "Alfa Romeo",  "Alfa Romeo",  "Alfa Romeo",  "Alfa Romeo",  "Alfa Romeo", "smart", "tata", "skoda", "tata", "skoda", "tata", "skoda", "tata", "skoda", "tata", "skoda", "tata", "skoda", "tata", "skoda", "tata", "skoda", "tata", "skoda", "tata", "skoda", "koenigsegg", "bristol", "rover", "Mercedes-Benz", "Lamborghini", "rover", "Mercedes-Benz", "Lamborghini", "rover", "Mercedes-Benz", "Lamborghini", "rover", "Mercedes-Benz", "Lamborghini", "rover", "Mercedes-Benz", "Lamborghini", "rover", "Mercedes-Benz", "Lamborghini", "rover", "Mercedes-Benz", "Lamborghini", "rover", "Mercedes-Benz", "Lamborghini", "rover", "Mercedes-Benz", "Lamborghini", "rover", "Mercedes-Benz", "Lamborghini", "rover", "Mercedes-Benz", "Lamborghini", "rover", "Mercedes-Benz", "Lamborghini", "rover", "Mercedes-Benz", "Lamborghini", "rover", "Mercedes-Benz", "Lamborghini", "rover", "Mercedes-Benz", "Lamborghini", "rover", "Mercedes-Benz", "Lamborghini", "bitter", "Land Rover", "Land Rover", "Land Rover", "Land Rover", "Land Rover", "Land Rover", "Land Rover", "Land Rover", "Land Rover", "Land Rover", "zagato", "Nissan", "Nissan", "Nissan", "Nissan", "Nissan", "Nissan", "Nissan", "Nissan", "Nissan", "Nissan", "Nissan", "Nissan", "Nissan", "Nissan", "Nissan", "Nissan", "Nissan", "Nissan", "alvis", "lotec", "Hyundai", "Hyundai", "Hyundai", "Hyundai", "Hyundai", "Hyundai", "Hyundai", "Hyundai", "Hyundai", "Hyundai", "Hyundai", "Hyundai", "Hyundai", "Hyundai", "Hyundai", "Hyundai", "Hyundai", "Hyundai", "Hyundai", "luxgen", "ssc", "moretti", "FIAT", "FIAT", "FIAT", "FIAT", "FIAT", "FIAT", "FIAT", "FIAT", "FIAT", "FIAT", "FIAT", "Subaru", "wartburg", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "Mazda", "BMW", "opel", "Volkswagen", "ferrari", "daihatsu", "amc", "fairthorpe"]
        counterMakes = {"McLaren":["Lamborghini","McLaren", "ferrari", "Porsche", "bugatti", "tesla"],
                        "hummer":["Jeep", "hummer", "Lamborghini", "Honda", "rover", "Toyota" ],
                        "Ford":["ferrari", "Ford", "Chevrolet", "Dodge", "GMC", "Mazda"],
                        "oldsmobile":["Buick", "oldsmobile", "BMW", "Ford"],
                        "Dodge": ["Dodge", "Ford", "Jeep", "Kia", "Chevrolet", "Toyota"],
                        "Maserati":["Maserati", "Aston Martin", "Porsche", "tesla", "BMW", "Jaguar", "ferrari", "Lamborghini", "Bentley", "Mercedes-Benz", "Audi", "Alfa Romeo", "bugatti"],
                        "tatra":["tatra", "skoda", "Porsche"],
                        "Audi":["Audi", "BMW", "Mercedes-Benz", "Volvo", "Lexus", "Acura", "Porsche", "tesla", "Volkswagen", "Lamborghini", "Jaguar", "ferrari","Subaru",  "Ford", "Jeep", "Kia", "Chevrolet", "Toyota", "bugatti", "Mazda"],
                        "Lexus":["Lexus", "Acura", "BMW","Toyota","Mercedes-Benz", "Nissan", "Honda", "Hyundai"],
                        "Cadillac":["Cadillac", "BMW", "Buick","Mercedes-Benz","Acura","Jaguar", "Chevrolet"],
                        "Honda":["Honda", "Toyota", "Mazda", "Acura", "Jeep"],
                        "Chevrolet":["Chevrolet", "Ford", "Toyota", "Honda", "Nissan", "Dodge", "Ford", "Jeep", "Kia","Buick", "Hyundai", "renault"],
                        "pontiac":["pontiac",  "Toyota", "Honda","Chevrolet", "Kia","Buick",  "Ford", "Mazda",  "BMW","ferrari","Honda", "Nissan","opel"],
                        "seat":["seat", "skoda", "peugeot"],
                        "Rolls-Royce":["Rolls-Royce", "Bentley", "Audi", "BMW", "Mercedes-Benz", "Volvo", "Lexus","Lamborghini","McLaren", "ferrari", "Porsche", "bugatti", "tesla", "Cadillac","Toyota"],
                        "Jaguar":["Jaguar", "Lamborghini","McLaren", "ferrari", "Porsche", "bugatti","Audi", "BMW", "Mercedes-Benz", "Ford", "Cadillac", "Lexus" ],
                        "Kia":["Kia", "Hyundai", "Honda", "Toyota", "Mazda", "Ford", "Nissan", "Mazda",  "BMW", "Dodge"],
                        "mahindra":["mahindra", "tata", "Ford", "Toyota", "Honda",  "renault", "Chevrolet"],
                        "Buick":["Honda", "Toyota", "Buick",  "Hyundai", "Honda","Ford", "Acura", "Subaru"],
                        "peugeot":["peugeot", "Honda", "Toyota","renault", "skoda", "Ford", "Nissan", "Hyundai", "opel", "seat"],
                        "Toyota":["Toyota", "Honda","Ford", "Nissan", "Mazda", "Jeep", "Hyundai", "Dodge", "Chevrolet", "Acura", "Audi", "BMW", "Mercedes-Benz"],
                        "citroen":["citroen", "renault", "Toyota", "Honda","Ford", "Nissan", "Mazda",  "Hyundai", "Audi", "BMW", "Mercedes-Benz", "skoda", "ferrari", "FIAT", "Volkswagen", "Lamborghini", "opel"],
                        "vauxhall":["vauxhall", "opel", "seat", "Ford", "skoda", "renault"],
                        "saab":["saab", "Audi", "BMW", "Mercedes-Benz", "Cadillac", "Porsche"],
                        "renault":["renault", "Honda","Ford", "Nissan", "Mazda", "opel", "Mercedes-Benz", "Honda", "Volkswagen", "mahindra", "Toyota"],
                        "Bentley":["Bentley", "Rolls-Royce", "Aston Martin", "Audi", "BMW", "Mercedes-Benz", "Maserati", "Lamborghini","McLaren", "ferrari", "Porsche", "bugatti", "Hyundai", "Nissan", "tesla"],
                        "suzuki":["suzuki", "Honda","Ford", "Nissan", "BMW", "Toyota","Hyundai", "Honda"],
                        "Volvo":["Volvo", "Audi", "BMW", "Mercedes-Benz", "Honda","Ford", "Nissan", "Volkswagen", "saab", "tesla"],
                        "tesla":["tesla", "Audi", "BMW", "Mercedes-Benz", "Porsche", "bugatti", "Lamborghini","McLaren", "ferrari", "Dodge", "Ford", "Toyota", "Honda"],
                        "Acura":["Acura", "Audi", "BMW", "Mercedes-Benz", "Honda","Ford","Nissan", "Toyota", "Subaru", "Cadillac", "Buick", "Hyundai"],
                        "Aston Martin":["Lamborghini","McLaren", "ferrari", "Porsche", "bugatti","Audi", "BMW", "Mercedes-Benz", "tesla", "Toyota"],
                        "Chrysler":["Chrysler", "Dodge", "Honda","Ford", "Cadillac", "Nissan", "Kia", "Rolls-Royce", "Hyundai", "BMW", "Chevrolet", "Kia"],
                        "bugatti":["bugatti", "Lamborghini","McLaren", "ferrari", "Porsche", "bugatti", "tesla", "Audi", "BMW", "Mercedes-Benz"],
                        "skoda":["skoda", "Toyota", "Volkswagen", "BMW", "Kia", "opel", "Honda","Ford"],
                        "tata":["tata", "mahindra", "Honda", "suzuki"],
                        "Mercedes-Benz":["Mercedes-Benz", "Audi", "BMW", "Lexus", "Cadillac", "Lamborghini","McLaren", "ferrari", "Porsche", "Volkswagen"],
                        "Lamborghini":["Lamborghini","McLaren", "ferrari", "Porsche", "bugatti","Ford", "Cadillac", "Nissan", "Kia","BMW", "Toyota","Audi", "BMW", "Lexus", "Honda"  ],
                        "Nissan":["Nissan", "Toyota","Hyundai", "Honda", "Kia", "Audi", "BMW", "bugatti", "Chevrolet","Toyota", "Honda","Ford", "Subaru"],
                        "Hyundai":["Hyundai",  "Honda", "Kia", "Audi", "BMW", "Honda","Ford","Nissan", "Toyota", "Chevrolet", "Mitsubishi"],
                        "BMW":["BMW", "Audi", "BMW", "Mercedes-Benz", "Volvo", "Lexus", "Acura", "Porsche", "tesla", "Volkswagen", "Lamborghini", "Jaguar", "ferrari","Honda","Ford","Nissan", "Toyota","Cadillac"],
                        "Volkswagen":["Volkswagen", "Honda","Ford","Nissan", "Toyota","BMW", "Hyundai", "Jeep", "Chevrolet", "Mercedes-Benz", "skoda", "Chrysler", "seat", "Mazda"],
                        "ferrari":["ferrari", "Lamborghini","McLaren", "ferrari", "Porsche", "bugatti", "tesla", "Ford"]
                        }
        cursor = connection.cursor()

        count = 0
        totalIterations = 0;
        while count < 5000 and totalIterations < 50000:
            totalIterations += 1
            # print("Total Iterations: ", totalIterations)
            make1 = None
            make2 = None
            make3 = None
            selectedModelID1 = None
            selectedModelID2 = None
            selectedModelID3 = None
            listOfCars = []
            while selectedModelID1 == None or selectedModelID2 == None or selectedModelID3 == None:
                listOfCars = []

                while make1 == None  or make2 == None or make3 == None:
                    randomMake = makesArray[randrange(len(makesArray) - 1)]
                    if randomMake in counterMakes:
                        counterCarsArray = counterMakes[randomMake]
                        if counterCarsArray:
                            make1 = randomMake
                            make2 = counterCarsArray[randrange(len(counterCarsArray)-1)]
                            make3 = counterCarsArray[randrange(len(counterCarsArray)-1)]
                    else:
                        make1 = None
                        continue
                year = yearsArray[randrange(len(yearsArray) - 1)]

                sqlQuery1 = "select model_id, model_name from cars.car where model_make_display ilike '"+make1+"'  and model_year = "+str(year)+" ORDER BY RANDOM() LIMIT 1"
                sqlQuery2 = "select model_id, model_name from cars.car where model_make_display ilike '"+make2+"'  and model_year = "+str(year)+" ORDER BY RANDOM() LIMIT 1"
                sqlQuery3 = "select model_id, model_name from cars.car where model_make_display ilike '"+make3+"'  and model_year = "+str(year)+" ORDER BY RANDOM() LIMIT 1"

                cursor.execute(sqlQuery1)
                selectedModelID1 = cursor.fetchone()
                if selectedModelID1 == None:
                    make1 = None
                    continue
                listOfCars.append(selectedModelID1[0])
                cursor.execute(sqlQuery2)
                selectedModelID2 = cursor.fetchone()
                if selectedModelID2 == None:
                    make1 = None
                    continue
                listOfCars.append(selectedModelID2[0])
                cursor.execute(sqlQuery3)
                selectedModelID3 = cursor.fetchone()
                if selectedModelID3 == None:
                    make1 = None
                    continue
                listOfCars.append(selectedModelID3[0])
                if selectedModelID1[1] == selectedModelID2[1] or selectedModelID2[1] == selectedModelID3[1] or selectedModelID3[1] == selectedModelID1[1]:
                    selectedModelID3 = None
                    selectedModelID2 = None
                    selectedModelID1 = None
                    make1 = None
                    continue


            carsCheckStr = "'{"
            COMMA = ","
            for j in range(len(listOfCars)):
                if j == len(listOfCars)-1:
                    COMMA = ""
                carsCheckStr += str(int(listOfCars[j]))+COMMA
            carsCheckStr += "}'"
            carsCheckQuery = " select count(*) as found  from cars.car_links where car_ids::text = "+carsCheckStr+" "
            # print(carsCheckQuery)
            cursor2 = connection.cursor()
            cursor2.execute(carsCheckQuery)
            carCheckRecords = cursor2.fetchall()
            if carCheckRecords[0] and int(carCheckRecords[0][0]) > 0:
                print("Existing record found")
            else:
                if len(listOfCars) == 3:

                    # print(str(listOfCars))
                    response = requests.post('http://localhost:5000/api/compare/cars', data='{"criteria":[{"id":880,"col_name":"model_year","displayname":"Model Year","preference":"False","importance":"5"},{"id":8900,"col_name":"model_engine_cc","displayname":"Engine size (cc)","preference":"False","importance":"5"},{"id":6294,"col_name":"model_engine_cyl","displayname":"Engine Cylinder","preference":"False","importance":"3"},{"id":367,"col_name":"model_engine_power_rpm","displayname":"Engine power (rpm)","preference":"False","importance":"2"},{"id":8245,"col_name":"model_engine_torque_rpm","displayname":"Engine Torque (rpm)","preference":"False","importance":"2"},{"id":1234,"col_name":"model_seats","displayname":"Seats","preference":"True","importance":"4"},{"id":4567,"col_name":"model_doors","displayname":"Doors","preference":"True","importance":"3"},{"id":765,"col_name":"model_width_mm","displayname":"Width (mm)","preference":"True","importance":"5"},{"id":3756,"col_name":"model_height_mm","displayname":"Height (mm)","preference":"True","importance":"5"}],"cars":'+str(listOfCars)+'}')
                    count += 1
                    #print(count)
                    #quit(0)
                    #print(response.json())
                    # print(count)
            cursor2.close()
            print("Total Comparisons: ", count, totalIterations)
    except (Exception, psycopg2.Error) as error:
        print("Error: ", error)
    finally:
        if (connection):
            connection.commit()
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")


if __name__ == "__main__":
    main()
