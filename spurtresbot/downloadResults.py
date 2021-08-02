'''
Version: 2021-08-02
laddar ned sträcktider för alla löpare från samma klubb från en tävling.
'''

import os
import requests
import config

def download(eventId):
    # get api-key
    apiKEY = os.environ.get(config.keys["EventorApiName"])
    path = config.paths["downloadsPath"]
    baseURL = "https://eventor.orientering.se/api"


    # save as xml
    def saveXML(fileName, content):
        with open(fileName, 'wb') as file:
            file.write(content)


    # build url and add parameters
    def urlBuilder(kwargs, apiUrl, baseUrl):
            url = baseUrl + apiUrl
            for key, value in kwargs.items():
                if url[-1] != "?":
                    url = url + "&"
                url = url + (str(key) + "=" + str(value))
            return url


    # organization id must be same as the club the api-key belongs to
    parameters = {"organisationIds": config.settings["organisationid"],     
                "eventId": str(eventId),         
                "includeSplitTimes": "true"}


    url = urlBuilder(parameters, "/results/organisation?", baseURL)
    response = requests.get(url, headers={'ApiKey': apiKEY})
    saveXML(path + "/" + parameters["eventId"] + ".xml", response.content)

    return response.status_code