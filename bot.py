import asyncio
import discord
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print("Successfully connected to discord.")

@client.event
async def on_message(message):
    
    # Avoid replying to it's own messages
    if(message.author.bot):
        return
    
    # Wait for a user to send the first message
    if(message.content):
        await message.channel.send("Hello, I am a bot. React with a thumbs up to confirm that you want to use this service.")    
        
client.run(TOKEN)