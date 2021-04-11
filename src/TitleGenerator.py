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
             '$powerkeyword - Which car is most wanted?', '$powerkeyword - Which brand is the winner', '$powerkeyword - Which one is better family car?',
             '$powerkeyword - Which one is fastest?', '$powerkeyword - Which car is cost effective?', '$powerkeyword - Which car is more powerful?', '$powerkeyword - Which car is worth buying?',
             '$powerkeyword - Which car is more reliable?']

allDescriptions = ['$powerkeyword car comparison is complicated. Big engine and more horse power not always the best. Compare cars $make1 and $make2 considering RPM, fuel economy, size and torque.',
                   '$powerkeyword usual car comparison may not suggest you right car. Our car comparison considers your situation and suggest best car for you. Check why $make1 is better/worse than $make2.',
                   '$powerkeyword car comparison. Car power depend on torque and RPM. Check if more RPM makes $make is better/worse than $make2. We compare cars for you only and suggest best one.',
                   '$powerkeyword compare cars side by side. Recent cars comes with manufacturer warranty and technologies. Check if such features make $make1 better than $make2.  ',
                   '$powerkeyword side by side car comparison. More torque is good for smooth drive but thats not the only think that makes $make1 better than $make2. Check which car is better?',
                   '$powerkeyword comparison side by side. Recent cars with small engine produce more power than older bigger engine. Check out if engine size makes $make1 better than $make2',
                   '$powerkeyword comparison based on engine size, torque, year, size, etc., and find out if $make1 is better than $make2. Compare cars with many other factors like engine size, torque, rpm, etc.',
                   '$powerkeyword car comparison and find the winner car. More cylinders, more piston movementm more power. Compare $make1 vs $make2 to see if car with more cylinders is best for you.',
                   'More the torque, better the drive but there are many other factors to compare $powerkeyword. Checkout if $make1 is better than $make2 and compare side by side',
                   '$powerkeyword car comparison to find which one is fastest. Having 2000cc with 3000 rpm is not the only deciding factor. Checkout if $make1 is faster and better than $make2.',
                   'Side by side comparison of $powerkeyword. Having a small engine is more fuel efficient. Is that why $make1 is more cost effective than $make2. Checkout this comparison.',
                   'Compare $powerkeyword for your needs. Compact family car not always less powerful. Checkout why car $make1 is more powerful than $make2 and is this your family car?',
                   'Not sure about $powerkeyword, checkout this comparison. Bigger engine makes car more powerful. Check if big engine makes $make1 better than $make2.']


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
    if car1Make == car2Make and car2Make == car3Make and car1Make == car3Make:
        if car1Make == car2Make:
            if car1Model == car2Model:
                if car1Make == car3Make:
                    if car1Model == car3Model:
                        if car2Make == car3Make:
                            if car2Model == car3Model:
                                if car1Year == car2Year:
                                    if car1Year == car3Year:
                                        if car2Year == car3Year:
                                            powerKeyword = car1Make + ' '+car1Model+ ' vs ' + car3Make +' '+car3Model
                                            car1 = car1Make+ ' '+car1Model
                                            car2 = car3Make+' '+car3Model
                                        else:
                                            powerKeyword = car2Year + ' ' + car2Make + ' '+car2Model+ ' vs '  + ' ' + car3Make +' '+car3Model
                                            car1 = car2Year + ' ' + car2Make+ ' '+car2Model
                                            car2 = car3Year + ' ' + car3Make+' '+car3Model
                                    else:
                                        powerKeyword = car1Year + ' ' + car1Make + ' '+car1Model+ ' vs ' + car3Year + ' ' + car3Make+ ' '+car3Model
                                        car1 = car1Year + ' ' + car1Make + ' '+car1Model
                                        car2 = car3Year + ' ' + car3Make + ' '+car3Model
                                else:
                                    #all three cars are the same make and model
                                    powerKeyword = car1Year +' '+car1Make + ' '+car1Model+ ' vs ' +car2Make+ ' '+car2Model
                                    car1 = car1Year +' '+car1Make+ ' '+car1Model
                                    car2 = car2Year +' '+car2Make+ ' '+car2Model
                            else:
                                powerKeyword = car2Make + ' ' + car2Model + ' vs ' + car3Make + ' ' + car3Model
                                car1 = car2Make + ' ' + car2Model
                                car2 = car3Make + ' ' + car3Model
                        else:
                            powerKeyword = car2Make + ' '+car2Model+ ' vs ' + car3Make+ ' '+car3Model
                            car1 = car2Make+ ' '+car2Model
                            car2 = car3Make+ ' '+car3Model
                    else:
                        powerKeyword = car1Make + ' ' + car1Model + ' vs ' + car3Make + ' ' + car3Model
                        car1 = car1Make + ' ' + car1Model
                        car2 = car3Make + ' ' + car3Model
                else:
                    powerKeyword = car1Make+ ' '+car1Model + ' vs ' + car3Make+ ' '+car3Model
                    car1 = car1Make+ ' '+car1Model
                    car2 = car3Make+ ' '+car3Model
            else:
                powerKeyword = car1Make + ' ' + car1Model + ' vs ' + car2Make + ' ' + car2Model
                car1 = car1Make + ' ' + car1Model
                car2 = car2Make + ' ' + car2Model
        else:
            powerKeyword = car1Make + ' '+car1Model+ ' vs ' + car2Make+ ' '+car2Model
            car1 = car1Make+ ' '+car1Model
            car2 = car2Make+ ' '+car2Model
    else:
        if car1Make != car2Make:
            powerKeyword = car1Make + ' '+car1Model+' vs ' + car2Make+ ' '+car2Model
            car1 = car1Make+ ' '+car1Model
            car2 = car2Make+ ' '+car2Model
        elif car1Make != car3Make:
            powerKeyword = car1Make + ' '+car1Model+ ' vs ' + car3Make+ ' '+car3Model
            car1 = car1Make+ ' '+car1Model
            car2 = car3Make+ ' '+car3Model
        else:
            powerKeyword = car2Make + ' '+car2Model+' vs ' + car3Make+ ' '+car3Model
            car1 = car2Make+ ' '+car2Model
            car2 = car3Make+ ' '+car3Model
    if (listOfCars[0].make == listOfCars[1].make):
        keywords.append(listOfCars[0].make +' '+listOfCars[0].model+' vs '+listOfCars[1].model)
    else:
        keywords.append(listOfCars[0].make +' '+listOfCars[0].model+ ' vs ' + listOfCars[1].make+' '+listOfCars[1].model)

    if (listOfCars[1].make == listOfCars[2].make):
        keywords.append(listOfCars[1].make +' '+listOfCars[1].model+' vs '+listOfCars[2].model)
    else:
        keywords.append(listOfCars[1].make +' '+listOfCars[1].model +' vs ' + listOfCars[2].make+' '+listOfCars[2].model)

    if (listOfCars[0].make == listOfCars[2].make):
        keywords.append(listOfCars[0].make +' '+listOfCars[0].model+' vs '+listOfCars[2].model)
    else:
        keywords.append(listOfCars[0].make +' '+listOfCars[0].model+ ' vs ' + listOfCars[2].make+' '+listOfCars[2].model)


    newTitle = Template(title).substitute(powerkeyword=powerKeyword)
    newDescription = Template(description).substitute(powerkeyword=powerKeyword, make1=car1, make2=car2)

    return {'title':newTitle,
              'description':newDescription, 'keywords':keywords, 'powerKeyword':powerKeyword}
