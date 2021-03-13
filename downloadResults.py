'''
Version: 2021.03.13
Används för att ladda ned sträcktider för all löparen från samma klubb från en tävling.
'''

import os
import requests

def download(eventId):
    #Lägg till klubbens api nyckel i miljövariabler>systemvariabler med namnet "eventorAPI"
    apiKEY = os.environ.get('eventorAPI')
    path = os.environ.get('ResBotFilePath')

    baseURL = "https://eventor.orientering.se/api"


    #Spara som xml-fil
    def saveXML(fileName, content):
        with open(fileName, 'wb') as file:
            file.write(content)


    def urlBuilder(kwargs, apiUrl, baseUrl):
            url = baseUrl + apiUrl #Bygg url
            for key, value in kwargs.items(): #lägg till fråge-parametrar
                if url[-1] != "?":
                    url = url + "&"
                url = url + (str(key) + "=" + str(value))
            return url


    parameters = {"organisationIds": "198",     #Måste vara samma som den organisation api-nyckeln tillhör
                "eventId": str(eventId),         
                "includeSplitTimes": "true"}

    url = urlBuilder(parameters, "/results/organisation?", baseURL) #Bygg url
    response = requests.get(url, headers={'ApiKey': apiKEY}) #Skicka begäran

    saveXML(path + "/" + parameters["eventId"] + ".xml", response.content) #Spara data som xml fil