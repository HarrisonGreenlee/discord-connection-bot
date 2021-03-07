import os
from dotenv import load_dotenv
import discord
from discord import Client
from discord import Game
import asyncio
import fileparser as fp

from db import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.reactions = True
intents.members = True
client = Client(intents=intents)

introduction = fp.get_intro()
questions = fp.get_questions()

user_progress = {

}

possible_reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']

emojis_to_int = {
    '1️⃣': 1,
    '2️⃣': 2,
    '3️⃣': 3,
    '4️⃣': 4,
    '5️⃣': 5,
    '❌': 1,
    '✅': 5
}


async def begin_survey(target_user):
    msg = await target_user.send(INTRODUCTION)
    await msg.add_reaction('\N{THUMBS UP SIGN}')
    users.append(User(target_user.id))


@client.event
async def on_ready():
    print('Currently logged in as:')
    print(client.user.name)
    print(client.user.id)
    print('Guilds that I am currently a member of')
    for guild in client.guilds:
        print(guild)

    await client.change_presence(activity=Game('Send me a message!'))


@client.event
async def on_message(message):
    if message.author.bot:
        return

    if not UserData(message.author.id).survey_already_submitted:
        msg = await message.author.send(introduction)
        await msg.add_reaction('✅')


@client.event
async def on_reaction_add(reaction, user):
    if introduction in reaction.message.content and user != client.user and reaction.message.author == client.user:

        print(reaction)
        await reaction.message.delete()
        await user.send("**Excellent! Please answer a few questions about yourself:**")
        current_user = UserData(user.id)
        users[user.id] = current_user
        question_message = await user.send(questions[current_user.next_question()])
        for reaction in possible_reactions:
            await question_message.add_reaction(reaction)

    elif user != client.user:
        if reaction.emoji in emojis_to_int:
            print("adding to database")
            current_user = users[user.id]
            current_user.add_data(current_user.next_question(), emojis_to_int[reaction.emoji])

            await reaction.message.delete()
            if not users[user.id].commit_to_database():
                question_message = await user.send(questions[users[user.id].next_question()])
                for reaction in possible_reactions:
                    await question_message.add_reaction(reaction)
            else:
                await user.send("**DONE - DATA SUBMITTED :D**")


client.run(TOKEN)


async def next_question(user):
    pass
