import asyncio
import os

import discord
import fileparser as fp
from db import *
from discord import Client
from discord import Game
from dotenv import load_dotenv

MIN_USERS_TO_START_MATCHING = 2

# load our environment variable to access the discord token
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# adding necessary intents so that our program functions properly
intents = discord.Intents.default()
intents.reactions = True
intents.members = True
client = Client(intents=intents)

# gets the introduction and questions
introduction = fp.get_intro()
# questions = fp.get_questions(client.user.avatar_url)
questions = fp.get_questions()

# a dictionary of users { user.id : user }
users = {}

# provides a list for us to iterate over, reducing redundancy
possible_reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣']

# basically is a means of converting our emoji
# values to an int for our sqlite database
emojis_to_int = {
    '1️⃣': 1,
    '2️⃣': 2,
    '3️⃣': 3,
    '4️⃣': 4,
    '5️⃣': 5,
    '❌': 1,
    '✅': 5
}


# performs key start-up tasks
@client.event
async def on_ready():
    print('Currently logged in as:')
    print(client.user.name)
    print(client.user.id)
    print('Guilds that I am currently a member of')
    for guild in client.guilds:
        print(guild)

    # changes the presence of the user
    await client.change_presence(activity=Game('Send me a message!'))


# performs tasks when a message is received
@client.event
async def on_message(message):
    if message.author.bot:
        return

    print(message.content == f'<@!{client.user.id}>')
    if not UserData(message.author.id).survey_already_submitted \
            and (message.content == f'<@!{client.user.id}>' or message.guild is None):
        print('Sending introduction')
        msg = await message.author.send(introduction)
        await msg.add_reaction('✅')


# performs tasks when a reaction is added
@client.event
async def on_reaction_add(reaction, user):

    if introduction in reaction.message.content and user != client.user and reaction.message.author == client.user:

        await reaction.message.delete()
        print(reaction)
        current_user = UserData(user.id)
        users[user.id] = current_user
        question_message = await user.send(embed=questions[current_user.next_question()])
        for reaction in possible_reactions:
            await question_message.add_reaction(reaction)

    elif user != client.user:
        if reaction.emoji in emojis_to_int:
            print("adding to database")
            current_user = users[user.id]
            current_user.add_data(current_user.next_question(), emojis_to_int[reaction.emoji])
            print(current_user.survey_data)

            await reaction.message.delete()
            if not users[user.id].commit_to_database():
                print("Next Q: " + str(users[user.id].next_question()))
                question_message = await user.send(embed=questions[users[user.id].next_question()])
                for reaction in possible_reactions:
                    await question_message.add_reaction(reaction)
            else:
                database_cursor.execute("SELECT * FROM userdata")
                if len(database_cursor.fetchall()) >= MIN_USERS_TO_START_MATCHING:
                    matching_user = users[user.id].get_nearest_user()
                    await user.send("Here is a user who has similar interests - try sending them a friend request!")
                    await user.send(client.get_user(matching_user.id).name)
                else:
                    await user.send("Thank you for completing the survey. We don't have "
                                    "enough users to begin matching yet, but we will soon! "
                                    "You can expect some other users to reach out to you shortly!")


client.run(TOKEN)
