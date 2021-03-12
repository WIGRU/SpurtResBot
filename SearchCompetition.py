import requests
from xml.etree import ElementTree
import datetime 
import time
import os
from difflib import SequenceMatcher
import logging

logging.basicConfig(filename='SClog.log', filemode='w', format='%(asctime)s - %(message)s')

path = os.environ.get('ResBotFilePath')

def search(ss):
    # Compares two strings and returns a score 0-1 how close they are
    def similar(a, b):
        #https://docs.python.org/3/library/difflib.html
        return SequenceMatcher(None, a, b).ratio()


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

    # Search in list with dicts
    def search(searchString=None, searchList=None, dictString=None, results=10, minScore=0.6):
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

        searchList = sorted(searchList, reverse = True, key = lambda i: i["score"]) #https://www.geeksforgeeks.org/ways-sort-list-dictionaries-values-python-using-lambda-function/

        if results == 0: #if  results=0 all objects with greater score than minScore will be returned
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

            try: #Find event id
                eventId = event.find("EventId").text
            except Exception as e:
                logging.warning(e)
                eventId = "-----"

            try: #Find eventName
                eventName = event.find("Name").text.encode("latin1").decode("utf-8")
            except Exception as e:
                logging.warning(e)
                eventName = event.find("Name").text

            try: #Find event date
                eventRace = event.find("EventRace")
                RaceDate = eventRace.find("RaceDate")
                eventDate = datetime.datetime.strptime(RaceDate.find("Date").text, '%Y-%m-%d')
            except Exception as e:
                logging.warning(e)
                eventDate = "yyyy-mm-dd"
            
            eventList.append({"score": None, "id": eventId, "name": eventName, "date":eventDate}) #Append to list as dict

        return eventList


    # Open and read event-list file
    logging.warning("Opening file " + path + "/eventList.xml")
    with open(path + "/eventList.xml", "r", encoding="utf8") as file:
        data = file.read()
    logging.warning("done")

    events = ElementTree.fromstring(data) # Data to xml element tree
    eventList = parseXML(events) # Get event id/name/date as dicts in list

    logging.warning("Number of competitions: " + str(len(eventList)))

    searchLis = search(searchString=str(ss), searchList=eventList, dictString="name")

    logging.warning("Number of results " + str(len(searchLis["results"])))
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

#print(search("test"))