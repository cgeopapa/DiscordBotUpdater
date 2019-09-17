#   id: 623542405282398208
#   token: NjIzNTQyNDA1MjgyMzk4MjA4.XYD9SQ.piOfXayZS1qyjyO96Ir2XyTA4v8
#   permissions: 67584
#
#   url: https://discordapp.com/oauth2/authorize?client_id=623542405282398208&scope=bot&permissions=67584
#
#   site: http://www.phys.uoa.gr/grammateia.html

import discord

token = 'NjIzNTQyNDA1MjgyMzk4MjA4.XYD9SQ.piOfXayZS1qyjyO96Ir2XyTA4v8'
client = discord.Client()  # starts the discord client.


@client.event
async def on_ready():  # method expected by client. This runs once when connected
    print(f'We have logged in as {client.user}')  # notification of login.


@client.event
async def on_message(message):  # event that happens per any message.
    if str(message.author) != str(client.user):
        await message.channel.send('Ναι!')


client.run(token)
