import discord
import requests
import re
import os
from xml.etree import ElementTree as ET
import datetime
from tabulate import tabulate
import datetime
import logging

import parseXML
import downloadResults
import SearchCompetition

TOKEN = os.environ.get('spurtResBot') #Get token from systemvariables
client = discord.Client()

@client.event
async def on_message(message):
    print(message.author)
    print(message.content)


    # The bot is not supposed to answer its own messages.
    if message.author == client.user:
        return


    if message.content.startswith('!Hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(msg)
    

    if message.content.startswith('!Res'):
        try:
            print(message.content)

            eventId = message.content.split(" ")[1]
            print(eventId)

            try:
                results = parseXML.parse(eventId)
                print(results)
                if results == False:
                    downloadResults.download(eventId)
                    results = parseXML.parse(eventId)

            except Exception as e:
                print(e)
                
            try:
                res = []
                for i in range(10):
                    runner = results["results"][i]
                    res.append((runner["name"], runner["lastSplitTime"], runner["lastCcode"]))

                def Sort(sub_li): 
                    sub_li.sort(key = lambda x: x[1]) 
                    return sub_li 

                l = Sort(res)
                print("")

                msg = "Topp 10 tider på spurten på: " + results["name"] + "\n"
                msg += "i Järfälla OK" + "\n"
                msg += "Datum: " + results["raceDate"] + "\n"

                msg += tabulate(l, headers=['Namn', 'Tid (s)', 'Sista kontroll'])
            
            except Exception as e:
                msg = "error"
                print(e)
        except Exception as e:
            print(e)
            msg = "error"
    
        await message.channel.send(msg)


    if message.content.startswith('!Sök'):
        s = message.content.replace("!Sök", " ").strip()
        msg = SearchCompetition.search(s)
            
        await message.channel.send(msg)


@client.event
async def on_ready():

    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------------')


client.run(TOKEN)