import os
import discord
from discord.ext import commands
import asyncio
import random
import requests

client = commands.Bot(command_prefix='.')

@client.event
async def on_ready():
    print('%s started.' % client.user.name)

@client.command(pass_context = True)
async def clear(ctx, number : int):
    """Delete old messages."""
    if number < 1: pass
    elif number > 99: number = 99

    number += 1
    messages = []
    async for message in client.logs_from(ctx.message.channel, limit = number):
        messages.append(message)
    await client.delete_messages(messages)

@client.command()
async def presence(name: str):
    """Set the name of the game which the bot is playing."""
    await client.change_presence(game=discord.Game(name=name))

@client.command(pass_context = True)
async def roll(ctx, dice = '1d20'):
    """Rolls a dice."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await client.say('Formato inválido! (Sintaxe: 1d20)')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await client.say('%s rodou ... %s (%s)' % (ctx.message.author.mention, result, dice))

@client.command()
async def img(search : str):
    """Searches for a image on internet."""
    response = requests.get('https://www.googleapis.com/customsearch/v1?q=' + search + '&key=AIzaSyAdEoG6cfZd_vQZrM9S_AlX7HdvFWoJeWM&cx=011823383867387955715%3An29llqfozmi')
    data = response.json()
    await client.say(data["items"][0]["pagemap"]["cse_image"][0]["src"])

@client.command()
async def choose(*choices : str):
    """Choose between specified things."""
    await client.say(random.choice(choices))

@client.event
async def on_message(message):
    await client.process_commands(message)

client.run(os.environ.get('BOT_TOKEN'))
