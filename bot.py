import os
from dotenv import load_dotenv
from discord import Client
from discord import Game

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = Client()

INTRODUCTION = open("Introduction.txt").read()


@client.event
async def on_ready():
    print('Currently logged in as:')
    print(client.user.name)
    print(client.user.id)
    print('Guilds that I am currently a member of')
    for guild in client.guilds:
        print(guild)

    await client.change_presence(activity=Game('Chilling'))


@client.event
async def on_message(message):
    if message.author.bot:
        return

    # checks if the bot has been @ed
    if message.content == f'<@!{client.user.id}>':
        msg = await message.author.send(INTRODUCTION)
        await message.channel.send(f'<@!{message.author.id}> Check your DM\'s')
        await msg.add_reaction('\N{THUMBS UP SIGN}')
        await msg.add_reaction('\N{THUMBS DOWN SIGN}')

client.run(TOKEN)
