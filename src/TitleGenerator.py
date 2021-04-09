from string import Template
from random import randrange
import json

#Bigger Engine
# Benefits
#smaller engine better efficiency.
#only engine size does not matter, how many cylinders and how much is the engine rpm.

# 2000 cc with 4 cylinders mean  each cylinder with 500cc
#3000 rpm means a piston inside the cylinder will move 3000 times in a minute to produce power.
#larger engine produce more fuel.
#large engines are more suitable for motorways and smaller for towns.

#more torque, more is the accelaration.
#torque is the power to rotate the engine's axis
#benefits of torque:
# If low torque, better power in lower gears and smooth driving in low gears.
# you can carry heavy loads.
# good for mountain roads as it given more power is lower gears and you can have smooth ride

allTitles = ['$powerkeyword - Which should you buy?', '$powerkeyword - Which brand is better?', '$powerkeyword - Which car is better?',
             '$powerkeyword - Battle of brands','$powerkeyword - Which one is better', '$powerkeyword - Which car is preferred?',
             '$powerkeyword - Which car is most wanted?', '$powerkeyword - Which brand is the winner', '$powerkeyword - which one is better family car?',
             '$powerkeyword - Which one is fastest?', '$powerkeyword - which car is cost effective?', '$powerkeyword - Which car is more powerful?', '$powerkeyword - Which car is worth buying?',
             '$powerkeyword - Which car is more reliable?']

allDescriptions = ['$powerkeyword car comparison complicated. Sometimes $make1 is better, sometimes $make2. This car comparison considers specific criteria, compare and rank so you can decide whats best for you.',
                   'Car comparison of $powerkeyword was never this simple. User worlds most advanced car comparison tool to find out why $make1 is better/worse than $make2.',
                   'Compare $powerkeyword and many many more cars. We compare $make1 and $make2 specs to help you understand why $make is better/worse than $make2. ',
                   'Compare cars $powerkeyword side by side and see all its specs and reviews. Bigger engine produces more power but does that make $make1 better than $make2.  ',
                   'Compare side by side $powerkeyword. More torque is good for smooth drive but thats not the only think that makes $make1 better than $make2. Check which car is better?',
                   '$powerkeyword comparison side by side. Recent cars with small engine produce more power than older bigger engine. Check out if engine size makes $make1 better than $make2',
                   'Compare $powerkeyword based on years and find out if $make1 is better than $make2. Compare cars with many other factors like engine size, torque, rpm, etc.',
                   'Compare $powerkeyword and find the winner car. Compare $make1 and $make2 on 9 specs and find out which car you should buy?',
                   'More the torque, better the drive but there are many other factors to compare $powerkeyword. Checkout if $make1 is better than $make2 and compare side by side',
                   'Compare $powerkeyword to find which one is fastest. Having 2000cc with 3000 rpm is not the only deciding factor. Checkout if $make1 is faster and better than $make2.',
                   'Side by side comparison of $powerkeyword. Having a small engine is more fuel efficient. Is that why $car is more cost effective than $make2. Checkout this comparison.',
                   'Comparing $powerkeyword is not easy. Many factors such as engine size, torque, rpm etc., need to be compared. Checkout if $make1 is more powerful than $make2?',
                   'Not sure about $powerkeyword, checkout this comparison. Compare $make1 vs $make2 on several specs and find out which one is most suitable for you. ']


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
    titleRandomIndex = randrange(len(allTitles))
    descRandomIndex = randrange(len(allDescriptions))
    title = allTitles[titleRandomIndex]
    description = allDescriptions[descRandomIndex]
    jRankData = json.loads(rankData)
    listOfCars = []
    keywords = []
    for i in range(len(jRankData['rnk_consolidate_final'])):
        make = jRankData['model_make_display'][str(i)].replace('-', ' ')
        model = jRankData['model_name'][str(i)].replace('-', ' ')
        year = jRankData['model_year'][str(i)]
        listOfCars.append(LightCar(make, model, year, jRankData['rnk_consolidate_final'][str(i)]))



    listOfCars.sort(key=lambda x:x.rank, reverse=False)
    powerKeyword = ""
    car1Make = listOfCars[0].make
    car1Model = listOfCars[0].model
    car1Year = str(listOfCars[0].year)

    car2Make = listOfCars[1].make
    car2Model = listOfCars[1].model
    car2Year = str(listOfCars[1].year)

    car3Make = listOfCars[2].make
    car3Model = listOfCars[2].model
    car3Year = str(listOfCars[2].year)

    car1 = ""
    car2 = ""

    if car1Make != car2Make:
        powerKeyword = car1Make+' vs '+car2Make
        car1 = car1Make
        car2 = car2Make
    elif car1Make != car3Make:
        powerKeyword = car1Make + ' vs ' + car3Make
        car1 = car1Make
        car2 = car3Make
    elif car2Make != car3Make:
        powerKeyword = car2Make + ' vs ' + car3Make
        car1 = car2Make
        car2 = car3Make
    elif (car1Make +' '+car1Model) != (car2Make +' '+car2Model):
        powerKeyword = car1Make +' '+car1Model + ' vs ' + car2Make+' '+car2Model
        car1 = car1Make + ' ' + car1Model
        car2 = car2Make + ' ' + car2Model
    elif (car1Make +' '+car1Model) != (car3Make +' '+car3Model):
        powerKeyword = car1Make +' '+car1Model + ' vs ' + car3Make+' '+car3Model
        car1 = car1Make + ' ' + car1Model
        car2 = car3Make + ' ' + car3Model
    elif (car2Make +' '+car2Model) != (car3Make +' '+car3Model):
        powerKeyword = car2Make +' '+car2Model + ' vs ' + car3Make+' '+car3Model
        car1 = car2Make + ' ' + car2Model
        car2 = car3Make + ' ' + car3Model
    elif (car1Make + ' ' + car1Model + ' ' + car1Year) != (car2Make + ' ' + car2Model + ' ' + car2Year):
        powerKeyword = car1Make + ' ' + car1Model + ' ' + car1Year + ' vs ' + car2Make + ' ' + car2Model + ' ' + car2Year
        car1 = car1Year +' '+car1Make + ' ' + car1Model
        car2 = car2Year +' '+car2Make + ' ' + car2Model
    elif (car1Make +' '+car1Model+' '+car1Year) != (car3Make +' '+car3Model+' '+car3Year):
        powerKeyword = car1Make +' '+car1Model+' '+car1Year + ' vs ' + car3Make +' '+car3Model+' '+car3Year
        car1 = car1Year + ' ' + car1Make + ' ' + car1Model
        car2 = car3Year + ' ' + car3Make + ' ' + car3Model
    elif (car2Make +' '+car2Model+' '+car2Year) != (car3Make +' '+car3Model+' '+car3Year):
        powerKeyword = car2Make +' '+car2Model+' '+car2Year + ' vs ' + car3Make +' '+car3Model+' '+car3Year
        car1 = car2Year + ' ' + car2Make + ' ' + car2Model
        car2 = car3Year + ' ' + car3Make + ' ' + car3Model
    else:
        powerKeyword = car1Make + ' ' + car1Model + ' vs ' + car2Make + ' ' + car2Model
        car1 = car1Year + ' ' + car1Make + ' ' + car1Model
        car2 = car2Year + ' ' + car2Make + ' ' + car2Model

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


    newTitle = Template(title).substitute(powerkeyword=powerKeyword)
    newDescription = Template(description).substitute(powerkeyword=powerKeyword, make1=car1, make2=car2)

    return {'title':newTitle,
              'description':newDescription, 'keywords':keywords, 'powerKeyword':powerKeyword}
