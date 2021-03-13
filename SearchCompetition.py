'''
Version: 2021.03.13
Script för att söka efter tävlingar i en xml fil från följande api https://eventor.orientering.se/api/events

1. Öppnar filen
2. Fil --> lista med event
3. Sökfunktion (olika funktioner som jämför söksträngen med eventen i listan)
4. Resultat till tabell
'''

import requests
from xml.etree import ElementTree
import datetime 
import time
import os
from difflib import SequenceMatcher
import logging

#logging.basicConfig(filename='app.log', filemode='w+', format='%(asctime)s - %(message)s')

path = os.environ.get('ResBotFilePath')

def search(ss):
    logging.info("Search request")
    # Search in list with dicts
    def search(searchString=None, searchList=None, dictString=None, results=10, minScore=0.6):

        logging.info("Searchparameters: \n ss: " + searchString + " \n ds: " + dictString + " \n r: " + str(results) + " \n ms: " + str(minScore))
        # Compares two strings and returns a score 0-1 how close they are
        def similar(a, b):
            #https://docs.python.org/3/library/difflib.html
            return SequenceMatcher(None, a, b).ratio()

        # Compares words in two strings and returns score 1p for each words thats same
        def compare(a, b):
            def fixS(string):
                string = string.lower() #make charachters lowercase

                characters_to_remove = ",.()-"

                for character in characters_to_remove: # remove "charachters_to_remove" from string
                    string = string.replace(character, " ")
                
                string = string.split(sep=(" ")) # make string into list where each word is one object
                return string

            a = fixS(a)
            b = fixS(b)

            matchCount = 0
            for wordA in a:
                for wordB in b:
                    if wordA == wordB:
                        matchCount += 1

            score = matchCount / len(a)

            return score


        '''
        searchString: search string
        searchList: list with dicts
        dictString: object in dict which will be compared to searchString
        results: number of results that will be returned. If results = 0, whole list will be returned 
        minScore: minimun similarity score to be returned
        '''

        startTime = time.time()

        for event in searchList: #Compare search string with names and store result in list
            score = similar(searchString.lower().strip(), event[dictString].lower().strip()) #Calculate the similarity-score
            score += compare(searchString, event[dictString])

            event["score"] = score

        #Sort list by score
        searchList = sorted(searchList, reverse = True, key = lambda i: i["score"]) #https://www.geeksforgeeks.org/ways-sort-list-dictionaries-values-python-using-lambda-function/

        if results == 0: #if results=0 all objects with greater score than minScore will be returned
            results = len(searchList)
        searchList = searchList[:results]

        res = [] # dict list that will be returned
        for result in searchList:
            if result["score"] > minScore: #Only return search results with greater score than minScore
                res.append(result)
        
        finishTime = time.time()
        totalTime = finishTime - startTime # Calculate time it took to get the search results

        return {"time": totalTime, "results": res}


    def parseXML(events):
        eventList = [] #list which dicts will be added to

        for event in events: #Loops for each event

            template = "An exception of type {0} occurred. Arguments:\n{1!r}" #Error template
            
            try: #Find event id
                eventId = event.find("EventId").text
            except Exception as e:
                logging.warning("EventId")
                  
                message = template.format(type(e).__name__, e.args)
                logging.warning(message)

                eventId = "-----"


            try: #Find eventName
                eventName = event.find("Name").text.encode("latin1").decode("utf-8")
            except Exception as e:
                if type(e).__name__ != "UnicodeDecodeError" and type(e).__name__ != "UnicodeEncodeError":
                    print(type(e).__name__)
                    logging.warning("EventName:")
                    message = template.format(type(e).__name__, e.args)
                    logging.warning(message)

                eventName = event.find("Name").text
                
            try: #Find event date
                eventRace = event.find("EventRace")
                RaceDate = eventRace.find("RaceDate")
                eventDate = datetime.datetime.strptime(RaceDate.find("Date").text, '%Y-%m-%d')
            except Exception as e:
                logging.warning("EventDate:")
                message = template.format(type(e).__name__, e.args)
                logging.warning(message)

                eventDate = "yyyy-mm-dd"
            
            eventList.append({"score": None, "id": eventId, "name": eventName, "date":eventDate}) #Append to list as dict

        return eventList


    # Open and read event-list file
    logging.info("Opening file " + path + "/eventList.xml")
    with open(path + "/eventList.xml", "r", encoding="utf8") as file:
        data = file.read()
    logging.info("done")

    events = ElementTree.fromstring(data) # Data to xml element tree
    eventList = parseXML(events) # Get event id/name/date as dicts in list

    logging.info("Number of competitions: " + str(len(eventList)))

    searchLis = search(searchString=str(ss), searchList=eventList, dictString="name")

    logging.info("Number of results " + str(len(searchLis["results"])))
    if len(searchLis["results"]) > 5:
        msg = str(round(searchLis["time"],3)) + "s" + "\n"
        msg += ("Id    | Date       | SearchMatch | Name\n")
        msg += ("------------------------------------------------------------------\n")
        for i in range(5):
            res = searchLis["results"][i]
            msg += res["id"] + " | " + res["date"].strftime("%Y-%m-%d") + " | " + str(round(res["score"],2)) + "       | " + res["name"] + "\n"
    else:
        msg = "No results"

    return msg