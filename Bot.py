#   id: 623542405282398208
#   token: NjIzNTQyNDA1MjgyMzk4MjA4.XYD9SQ.piOfXayZS1qyjyO96Ir2XyTA4v8
#   permissions: 67584
#
#   url: https://discordapp.com/oauth2/authorize?client_id=623542405282398208&scope=bot&permissions=67584
#
#   site: http://www.phys.uoa.gr/grammateia.html

import discord
import requests
import time
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import Popularity
import bs4 as bs
import lxml

token = 'NjIzNTQyNDA1MjgyMzk4MjA4.XYD9SQ.piOfXayZS1qyjyO96Ir2XyTA4v8'
client = discord.Client()  # starts the discord client.
url = 'http://www.phys.uoa.gr/grammateia.html'
sleepTime = 3600
curLast = 'ΑΝΑΚΟΙΝΩΣΗ ΓΙΑ ΤΟΥΣ ΝΕΟΕΙΣΑΧΘΕΝΤΕΣ ΦΟΙΤΗΤΕΣ ΑΚΑΔ. ΕΤΟΥΣ 2019-2020'

newsMessage = '>>> **!!Holly Shit!!** \nΝέα Ανακοίνωση στο εξτρα φοβερό ιστότοπο της εξτρα φοβερής σχολής μας. \nΚαι σας ακούω να ρωτάτε: *Ποιό είναι το θέμα της;* Ε ΠΑΡΤΟ:\n\n'


@client.event
async def on_ready():  # method expected by client. This runs once when connected
    print(f'We have logged in as {client.user}')  # notification of login.


async def monitor_webpage():
    #Generate fake user agent so we dont get banned
    userAgent = UserAgent(100, Popularity.POPULAR.value)
    global curLast

    await client.wait_until_ready()
    channel = client.get_channel(622867078839402525)

    #Check every hour or so
    while(True):
        header = userAgent.get_random_user_agent()

        await channel.send(f'>>> Time to check for updates with user agent: {str(header)}')

        # Get the html from the website
        response = requests.get(url, header)

        # Parse the html so we can easily search it
        soup = bs.BeautifulSoup(response.text, 'lxml')

        # Get the most recent news title in the parsed html format
        first = True
        for c in soup.find_all('div', class_='news-list-item'):
            newLast = c.find('a').get('title')      #We got the latest news title
            # Are new and cur news titles different?
            if curLast == 'init':
                curLast = newLast
                break

            if curLast != newLast:
                if first:                      #If this is the first headline we found
                    comingUpCur = newLast
                    first = False
                link = 'http://www.phys.uoa.gr/' + c.find('a').get('href')
                messageToSend = f'{newsMessage}*{newLast}* \n{link}'
                await channel.send(messageToSend)
            elif first:
                await channel.send(f'>>> Checked and found this title: {newLast}.\nIt isnt new.')
            else:
                curLast = comingUpCur
                break

        time.sleep(sleepTime)


client.loop.create_task(monitor_webpage())
client.run(token)
