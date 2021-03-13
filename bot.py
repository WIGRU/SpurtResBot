'''
Version 2021.02.13
En discord-bot som gör en resultatlista över bästa spurttider inom en klubb

Kommandon:
!Hej --> Hej <namn>
!Hjälp --> List på kommandon
!Res <tävlingsID> --> Topp tio bästa spurttider i klubben
!Sök <tävling> --> Lista på tävlingar och dess Id:n
'''

import discord
import os
from tabulate import tabulate
import logging

import parseXML
import downloadResults
import SearchCompetition

SysVarTokenKey = 'spurtResBot'

# Config log
logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s - %(message)s')
logging.getLogger().setLevel(logging.INFO)


#get discord token
logging.info("getting token with key: " + SysVarTokenKey)
TOKEN = os.environ.get(SysVarTokenKey) #Get token from system variables
if TOKEN == None:
    logging.warning("Could not get Token")
    quit()


client = discord.Client()


@client.event
async def on_message(message):
    logging.info(str(message.author) + ": " + str(message.content)) 


    # The bot is not supposed to answer its own messages.
    if message.author == client.user:
        return


    if message.content.startswith('!Hej'):
        msg = 'Hej {0.author.mention}'.format(message)
        await message.channel.send(msg)


    if message.content.startswith('!Hjälp'):
        msg = 'Sök efter tävling "!Sök <tävlingsnamn>" \n' + 'Hämta spurttider "!Res <tävlingsId>" t.ex. "!Res 30549" '.format(message)
        await message.channel.send(msg)
    

    if message.content.startswith('!Res'):
        try:
            eventId = message.content.split(" ")[1]
            logging.info(eventId)

            try:
                results = parseXML.parse(eventId)
                logging.info(results)
                if results == False:
                    downloadResults.download(eventId)
                    results = parseXML.parse(eventId)

            except Exception as e:
                logging.info(e)
                
            try:
                res = []
                for i in range(10):
                    runner = results["results"][i]
                    res.append((runner["name"], runner["lastSplitTime"], runner["lastCcode"]))

                def Sort(sub_li): 
                    sub_li.sort(key = lambda x: x[1]) 
                    return sub_li 

                l = Sort(res)

                msg = "Topp 10 tider på spurten på: " + results["name"] + "\n"
                msg += "i Järfälla OK" + "\n"
                msg += "Datum: " + results["raceDate"] + "\n"

                msg += tabulate(l, headers=['Namn', 'Tid (s)', 'Sista kontroll'])
            
            except Exception as e:
                msg = "error"
                logging.info(e)
        except Exception as e:
            logging.info(e)
            msg = "error"
    
        await message.channel.send(msg)


    if message.content.startswith('!Sök'):
        s = message.content.replace("!Sök", " ").strip()
        msg = SearchCompetition.search(s)
            
        await message.channel.send(msg)


@client.event
async def on_ready():
    logging.info('Logged in as')
    logging.info(client.user.name)
    logging.info(client.user.id)


client.run(TOKEN)