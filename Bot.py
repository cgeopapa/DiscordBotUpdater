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

token = 'NjIzNTQyNDA1MjgyMzk4MjA4.XYTdKA.JEN_RW_OYstum-itXM7SVRydxpA'
client = discord.Client()  # starts the discord client.
url = 'http://www.phys.uoa.gr/grammateia.html'
sleepTime = 3600
curLast = 'init'

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

        print(f'>>> Time to check for updates with user agent: {str(header)}')

        # Get the html from the website
        response = requests.get(url, header)

        # Parse the html so we can easily search it
        soup = bs.BeautifulSoup(response.text, 'lxml')

        # Get the most recent news title in the parsed html format
        first = True
        newsList = []
        for c in soup.find_all('div', class_='news-list-item'):
            newLast = (c.find('a').get('title'), c.find('a').get('href'))

            if curLast == 'init':
                curLast = newLast      #We got the latest news title
                print(f'Initialized with {curLast}')
                break
            else:
                if curLast == newLast:
                    print('This has been shown before')
                    break
                else:
                    newsList.append(newLast)

        if len(newsList) > 0:
            for new in newsList:
                await channel.send(f'{newsMessage}*{new[0]}*\nhttp://www.phys.uoa.gr/{new[1]}')
            curLast = newsList[0]
        time.sleep(sleepTime)


client.loop.create_task(monitor_webpage())
client.run(token)
