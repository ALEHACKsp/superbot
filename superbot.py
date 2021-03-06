import os
import discord
from discord.ext import commands
import asyncio
import random
import requests

messages = []
client = commands.Bot(command_prefix='.')
answers = ['Sim', 'Não', 'Demais', 'Nem um pouco',
           'Muito', 'Minhas fontes dizem que não', 'É possível']

@client.event
async def on_ready():
    print('%s started.' % client.user.name)

@client.command(pass_context=True)
async def clear(ctx, number: int):
    """Delete old messages."""
    if number < 1:
        pass
    elif number > 99:
        number = 99

    number += 1
    old_messages = []
    async for message in client.logs_from(ctx.message.channel, limit=number):
        old_messages.append(message)
    await client.delete_messages(old_messages)

@client.command()
async def presence(name: str):
    """Set the name of the game which the bot is playing."""
    await client.change_presence(game=discord.Game(name=name))

@client.command(pass_context=True)
async def roll(ctx, dice='1d20'):
    """Rolls a dice."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await client.say('Formato inválido! (Sintaxe: 1d20)')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await client.say('%s rodou ... %s (%s)' % (ctx.message.author.mention, result, dice))

@client.command()
async def img(search: str):
    """Searches for a image on internet."""
    response = requests.get('https://www.googleapis.com/customsearch/v1?q=' + search +
                            '&key=AIzaSyAdEoG6cfZd_vQZrM9S_AlX7HdvFWoJeWM&cx=011823383867387955715%3An29llqfozmi')
    data = response.json()
    await client.say(data["items"][0]["pagemap"]["cse_image"][0]["src"])

@client.command()
async def choose(*choices: str):
    """Choose between specified things."""
    await client.say(random.choice(choices))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # repeat message chain
    if len(messages) > 0 and messages[0] == message.content:
        messages.append(message.content)
        if len(messages) % 3 == 0:
            await client.send_message(message.channel, message.content)
    else:
        messages.clear()
        messages.append(message.content)

    # answering questions
    if client.user in message.mentions:
        if message.content.endswith('?'):
            if ' ou ' in message.content:
                choices = message.content.split(' ou ')
                choices[0] = choices[0].split(' ', 1)[1]
                choices[len(choices) - 1] = choices[len(choices) - 1][:-1]
                await client.send_message(message.channel, random.choice(choices))
            else:
                await client.send_message(message.channel, random.choice(answers))

    await client.process_commands(message)

client.run(os.environ.get('BOT_TOKEN'))
