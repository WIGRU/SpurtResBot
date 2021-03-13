'''
Version: 2021.03.13
Används för att läsa in resultatfil få resultat i en "dict-list"
'''

from xml.etree import ElementTree as ET
import datetime
import os
import logging

SysVarDownloadFPkey = 'ResBotFilePath'

def parse(c):
    logging.info("Parse request")

    logging.info("getting token with key: " + SysVarDownloadFPkey)
    path = os.environ.get(SysVarDownloadFPkey)
    if path == None:
        logging.info("Could not get path with key " + SysVarDownloadFPkey)
        quit()

    try:
        f = path + "\\" + str(c) + '.xml'
        tree = ET.parse(f)
    except Exception as e:
        logging.info("Could not find file: " + f)
        return False

    root = tree.getroot()

    Event = root.find("Event")
    competitionName = Event.find("Name")
    logging.info("event name: " + competitionName)
    EventRace = Event.find("StartDate")
    raceDate = EventRace.find("Date")

    results = []

    classes = root.findall("ClassResult")
    for c in classes:
        EventClass = c.find("EventClass")
        className = EventClass.find("Name")

        runners = c.findall("PersonResult")
        for runner in runners:
            person = runner.find("Person")
            name = person.find("PersonName")
            runnerName = name[1].text + " " + name[0].text

            result = runner.find("Result")
            status = result.find("CompetitorStatus").attrib["value"]
            #print(status)
            if status == "OK":
                runnerTime = result.find("Time").text
                pos = result.find("ResultPosition").text
            else:
                runnerTime = "--:--:--"
                pos = "-"

            if status == "OK":
            
                sp = result.findall("SplitTime")

                cSplits = []
                for s in sp:
                    code = sp[-1][0].text
                    time = sp[-1][1].text
                    cSplits.append({"code": code, "time": time})

                finish = runnerTime
                last = sp[-1][1].text
                lastCode = sp[-1][0].text

                if len(finish) == 5:
                    finish_time = datetime.datetime.strptime(finish, '%M:%S')
                else:
                    finish_time = datetime.datetime.strptime(finish, '%H:%M:%S')


                if len(last) == 5:
                    last_time = datetime.datetime.strptime(last, '%M:%S')
                else:
                    last_time = datetime.datetime.strptime(last, '%H:%M:%S')

                spurttid = (finish_time - last_time).total_seconds()
    
            else:
                sp = []
                cSplits = []

            try:
                results.append({"name": runnerName, "class": className.text, "status": status, "time": runnerTime, "pos": pos, "splits": cSplits, "lastCcode": lastCode, "lastSplitTime": spurttid})
            except Exception as e:
                logging.info(e)

    return {"name": competitionName.text, "raceDate": raceDate.text, "results": results}