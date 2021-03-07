import os
from dotenv import load_dotenv
import discord
from discord import Client
from discord import Game
import asyncio

from db import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


intents = discord.Intents.default()
intents.reactions = True
intents.members  = True
client = Client(intents = intents)

INTRODUCTION = open("Introduction.txt").read()
QUESTION_1 = "**(QUESTION 1/3):** On a scale from 1-5, how much do you like tomato soup?"
QUESTION_2 = "**(QUESTION 2/3):** On a scale from 1-5, how much do you like french onion soup?"
QUESTION_3 = "**(QUESTION 3/3):** On a scale from 1-5, how much do you like clam chowder?"

questions = []
questions.append(QUESTION_1)
questions.append(QUESTION_2)
questions.append(QUESTION_3)


users = {}
emojis_to_int = {
    '1️⃣':1,
    '2️⃣':2,
    '3️⃣':3,
    '4️⃣':4,
    '5️⃣':5,
    '❌':1,
    '✅':5
}

async def begin_survey(target_user):
    msg = await target_user.send(INTRODUCTION)
    await msg.add_reaction('\N{THUMBS UP SIGN}')
    users.append(User(target_user.id))


############################################## BOT #################################################

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
        msg = await message.author.send(INTRODUCTION)
        await msg.add_reaction('✅')

@client.event        
async def on_reaction_add(reaction, user):
    if INTRODUCTION in reaction.message.content and user != client.user and reaction.message.author == client.user:

        print(reaction)
        await reaction.message.delete()
        await user.send("**Excellent! Please answer a few questions about yourself:**")
        current_user = UserData(user.id)
        users[user.id] = current_user
        question_message = await user.send(questions[current_user.next_question()])
        await question_message.add_reaction('1️⃣')
        await question_message.add_reaction('2️⃣')
        await question_message.add_reaction('3️⃣')
        await question_message.add_reaction('4️⃣')
        await question_message.add_reaction('5️⃣')
        
    elif user != client.user:
        if reaction.emoji in emojis_to_int:
            print("adding to database")
            current_user = users[user.id]
            current_user.add_data(current_user.next_question(), emojis_to_int[reaction.emoji])
            
            await reaction.message.delete()
            if not users[user.id].commit_to_database():
                question_message = await user.send(questions[users[user.id].next_question()])
                await question_message.add_reaction('1️⃣')
                await question_message.add_reaction('2️⃣')
                await question_message.add_reaction('3️⃣')
                await question_message.add_reaction('4️⃣')
                await question_message.add_reaction('5️⃣')
            else:
                await user.send("**DONE - DATA SUBMITTED :D**")

client.run(TOKEN)

def next_question(user, ):
    pass
    
