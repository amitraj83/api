from string import Template
from random import randrange
import json

allTitles = [{'title':'$year $carName - 9 awesome specs and reviews',
              'description':'9 awesome specs that makes $year $carName better than others. View $carName specs, reviews and comparison before buying used cars for sale.'},
             {'title':'$year $carName - 9 unbelievable specs and reviews',
              'description':'9 unbelievable specs that makes $year $carName better than others. View $carName specs, reviews and comparison before buying used cars for sale.'},
             {'title':'$year $carName - 9 amazing specs and reviews',
              'description':'9 amazing specs that makes $year $carName better than others. View $carName specs, reviews and comparison before buying used cars for sale.'},
             {'title':'$year $carName - 9 facts making it great car',
              'description':'9 amazing facts that makes $year $carName better than others. View $carName specs, reviews and comparison before buying used cars for sale.'},
             {'title':'$year $carName - 9 facts making it the best car',
              'description':'9 amazing facts that makes $year $carName better than others. View $carName specs, reviews and comparison before buying used cars for sale.'},
             {'title':'$year $carName - Do not miss these 9 facts',
              'description':'9 awesome facts that makes $year $carName better than others. View $carName specs, reviews and comparison before buying used cars for sale.'},
             {'title':'$year $carName - 9 amazing reasons to buy this car',
              'description':'9 amazing reasons that makes $year $carName better than others. View $carName specs, reviews and comparison before buying used cars for sale.'},
             {'title':'$year $carName - 9 amazing facts to buy this car',
              'description':'9 amazing facts that makes $year $carName better than others. View $carName specs, reviews and comparison before buying used cars for sale.'}
             ]

allKeywords = ['$year $carName', '$year $carName specs', '$year $carName review', '$year $carName price']


class LightCar:
    def __init__(self, make, model, year, rank):
        self.make = make
        self.model = model
        self.year = year
        self.rank = rank
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,sort_keys=True, indent=4)


def generateSEOTitleDescriptionKeywords(rankData):
    randomIndex = randrange(len(allTitles))
    randomObject = allTitles[randomIndex]
    title = randomObject['title']
    description = randomObject['description']
    jRankData = json.loads(rankData)
    listOfCars = []
    keywords = []
    for i in range(len(jRankData['rnk_consolidate_final'])):
        make = jRankData['model_make_display'][str(i)].replace('-', ' ')
        model = jRankData['model_name'][str(i)].replace('-', ' ')
        year = jRankData['model_year'][str(i)]
        listOfCars.append(LightCar(make, model, year, jRankData['rnk_consolidate_final'][str(i)]))
        keywords.append(make+' '+model)
        keywords.append(str(year)+' '+make+' '+model)
        keywords.append(make+' '+model+' specs')
        keywords.append(make+' '+model+' review')


    listOfCars.sort(key=lambda x:x.rank, reverse=False)
    powerKeyword = listOfCars[0].make+' '+listOfCars[0].model

    if (listOfCars[0].make == listOfCars[1].make):
        keywords.append(listOfCars[0].make +' '+listOfCars[0].model+' vs '+listOfCars[1].model)
    else:
        keywords.append(listOfCars[0].make + ' vs ' + listOfCars[1].make)

    if (listOfCars[1].make == listOfCars[2].make):
        keywords.append(listOfCars[1].make +' '+listOfCars[1].model+' vs '+listOfCars[2].model)
    else:
        keywords.append(listOfCars[1].make + ' vs ' + listOfCars[2].make)

    if (listOfCars[0].make == listOfCars[2].make):
        keywords.append(listOfCars[0].make +' '+listOfCars[0].model+' vs '+listOfCars[2].model)
    else:
        keywords.append(listOfCars[1].make + ' vs ' + listOfCars[2].make)

    carName = listOfCars[0].make+' '+listOfCars[0].model
    year = listOfCars[0].year
    newTitle = Template(title).substitute(carName=carName, year=str(year))
    newDescription = Template(description).substitute(carName=carName, year=str(year))

    return {'title':newTitle,
              'description':newDescription, 'keywords':keywords, 'powerKeyword':powerKeyword}
