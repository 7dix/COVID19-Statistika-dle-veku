"""
Covid statistiky podle věku

-- Vypočítá šance obecné šance na hospitalizaci, JIP, nebo úmrtí podle věku a dostupných statistik
-- v0.2
-- Marek Tenora

"""





import math
import random
import json
from datetime import datetime
import getData




p1 = int()
p2 = int()
p3 = int()
list = [] #DATA
top = () #VRCHNI HRANICE
bot = () #SPODNI HRANICE


vekKategorie = [[0,11],[12,15],[16,17],[18,24],[25,29],[30,34],[35,39],[40,44],[45,49],[50,54],[55,59],[60,64],[65,69],[70,74],[75,79],[80,84],[85,110]]


def probCalc(p1, p2, p3):
    calc = ((p1*100)/p2)-100
    return calc

def totCalc(list, **kwargs):
    calc = sum(list[bot:top])/10
    return calc



def getCovidStats(age, dateAfter):
    global vekKategorie
    ageCat = []
    dateAfter = datetime.strptime(dateAfter, "%Y-%m-%d")

    for x in vekKategorie:
        if age in range(x[0],x[1]+1):
            ageCat = x    
            ageCatString = str(x[0])+"-"+str(x[1])
            if ageCat[1] == 110:
                ageCatString = str(x[0])+"+"

    print("vek:",age)
    print("vekova kategorie:",ageCatString)

    #CASES
    with open("casesWithCat.json") as f:
        casesWithCat = json.load(f)
    
    casesAge = [{"pocet":x["potvrzene_pripady"],"pocetHospitalizaci":x["nove_hospitalizace"],"pocetJip":x["nove_jip"],"vek":x["vekova_kategorie"]} for x in casesWithCat if str(x["vekova_kategorie"]) == ageCatString and datetime.strptime(x["datum"], "%Y-%m-%d") >= dateAfter]
    casesCount = int()
    hospCount = int()
    JIPCount = int()
    for x in casesAge:
        if x["pocet"] != None:
                casesCount+=x["pocet"]
        if x["pocetHospitalizaci"] != None:
                hospCount+=x["pocetHospitalizaci"]
        if x["pocetJip"] != None:
                JIPCount+=x["pocetJip"]


    #UMRTI
    with open("deaths.json") as f: 
        deaths = json.load(f)

    deathsAge = [{"vek": x["vek"], "datum": x["datum"]} for x in deaths if x["vek"] in range(ageCat[0],ageCat[1]+1) and datetime.strptime(x["datum"], "%Y-%m-%d") >= dateAfter]
    deathsCount = len(deathsAge)



    print("datum od:", dateAfter.strftime("%d.%m.%Y"))
    print("pocet pripadu:",casesCount)
    print("\n")
    print("pocet hospitalizaci:",hospCount)
    print("pocet JIP:",JIPCount)
    print("pocet umrti:", deathsCount) 
    print("\n")
    print("sance na hospitalizaci kategorie:",hospCount/casesCount*100,"%")
    print("sance na JIP kategorie:",JIPCount/casesCount*100,"%")
    print("umrtnost kategorie:", deathsCount/casesCount*100,"%")
    print("\n")
    print("sance prezit covid je tedy:", 100-deathsCount/casesCount*100,"%")

    #for y in range(ageCat[0],ageCat[1]+1):
    #    print(y, len([x for x in deathsAge if x["vek"] == y]))

def main():
    if int(input("Chcete spustit aktualizaci datového balíčku Covid statistik? 1 = ANO, 0 = NE: ")) == 1:
        apiKey = int(input("Zadej prosím API klíč (je zdarma na https://onemocneni-aktualne.mzcr.cz/api/v3/docs):"))
        getData.update_dataset(apiKey)


    ageInput = int(input("Zadej věk pro který chceš vypočítat Covid statistiky: "))
    dateInput = input("Zadej datum, odkdy chceš statistiku počítat(ve tvaru např. 2020-10-31): ")

    getCovidStats(ageInput,dateInput)


if __name__ == '__main__':
    main()