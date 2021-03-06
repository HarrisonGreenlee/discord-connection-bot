import os
from dotenv import load_dotenv
from discord import Client
from discord import Game

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = Client()


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
        await message.author.send('**Hi, I\'m DiscMatch! Thank you for reaching out** :wink: '
                                  '\n*You\'re moments away from being matched with people !*  :eyes:')
        message = await message.channel.send(f'<@!{message.author.id}> Check your DM\'s')
        await message.add_reaction(':eyes:')

client.run(TOKEN)
