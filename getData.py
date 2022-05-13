import requests
import os
import json
import random


#Nastavení requestu
base = "https://onemocneni-aktualne.mzcr.cz/api/v3/"
headers = {'accept': "application/ld+json"}

def update_dataset(key):
    print("0/3")
    deaths(key)
    print("1/3")
    deathsOckovaniPrumer(key)
    print("2/3")
    casesWithCat(key)
    print("3/3")


#GetUmrtí
def deaths(key):
    page = 1
    data = []
    #Načtení všech položek
    while True:
        url = base+"umrti?page={0}&itemsPerPage=10000&apiToken={1}".format(page,key)

        r = requests.get(url, headers=headers)
        
        dataP = r.json()
        #last page check
        if len(dataP["hydra:member"]) == 0:
            break
        data += dataP["hydra:member"]
        page+=1

    #Ulozit do Jsonu
    with open("deaths.json", "w") as outfile:
        json.dump(data, outfile)


#GetPripady
def deathsOckovaniPrumer(key):
    page = 1
    data = []
    #Načtení všech položek
    while True:
        url = base+"ockovani-umrti?page={0}&itemsPerPage=10000&apiToken={1}".format(page,key)

        r = requests.get(url, headers=headers)
        
        dataP = r.json()
        #last page check
        if len(dataP["hydra:member"]) == 0:
            break
        data += dataP["hydra:member"]
        page+=1

    #Ulozit do Jsonu
    with open("deathsOckovaniPrumer.json", "w") as outfile:
        json.dump(data, outfile)


def casesWithCat(key):
    page = 1
    data = []
    #Načtení všech položek
    while True:
        url = base+"nakazeni-hospitalizace-testy?page={0}&itemsPerPage=10000&apiToken={1}".format(page,key)

        r = requests.get(url, headers=headers)
        
        dataP = r.json()
        #last page check
        if len(dataP["hydra:member"]) == 0:
            break
        data += dataP["hydra:member"]
        page+=1
    #Ulozit do Jsonu
    with open("casesWithCat.json", "w") as outfile:
        json.dump(data, outfile)








#NEMOZNE ZATIM
"""def deathsOckovani():
    with open("deaths.json") as f:
        deaths = json.load(f)
    with open("deathsOckovaniPrumer.json") as f:
        ockovani = json.load(f)

    for zapis in ockovani:

        Ockovani = []
        Neockovani = []


        osobyVek = [item["vek"] for item in deaths if item["datum"] == zapis["datum"]]
        
        print(zapis["datum"])

        Celkem = zapis["zemreli_celkem"]

        zTohoN = zapis["zemreli_bez_ockovani"]
        prumerN = zapis["zemreli_bez_ockovani_vek_prumer"]

        zTohoO = zapis["zemreli_nedokoncene_ockovani"]+zapis["zemreli_dokoncene_ockovani"]+zapis["zemreli_posilujici_davka"]
        if zTohoO == 0:
            Neockovani = Celkem
            continue

        pocetNedok = zapis["zemreli_nedokoncene_ockovani"]
        pocetDok = zapis["zemreli_dokoncene_ockovani"]
        pocetPos = zapis["zemreli_posilujici_davka"]

        prumerO = 1-prumerN
        
        while True:
            celkem = 0
            firstCh = random.sample(osobyVek, zTohoN)
            for x in firstCh:
                celkem += x            
            if celkem/zTohoN == prumerN:
                print(firstCh)
                Neockovani = firstCh
                for x in firstCh:
                    osobyVek.remove(x)
                print(osobyVek)
                Ockovani = osobyVek
                break
"""





