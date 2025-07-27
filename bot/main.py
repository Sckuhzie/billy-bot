import asyncio
import os
import random as rd
from datetime import datetime

import discord
from discord.ext import commands, tasks
from discord.ext.commands import Context
from dotenv import load_dotenv
from insult import create_insult

load_dotenv()
bot_token = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True  # Optional but good practice

bot = commands.Bot(command_prefix="!", intents=intents)

PROBABILITY_INSULT = 1 / 30
TARGET_CHANNEL_ID = 1398972120326869022  # TODO: Change to witcher channel
AVERAGE_DELAY_WITCHER = (
    3.5 * 24 * 60 * 60  # Half a week, the bot will say it twice a week
)  # Average time between each "When the witcher in seconds"


@bot.event
async def on_message(message: discord.Message):

    mentioned = bot.user in message.mentions
    replied_to_bot = (
        message.reference
        and isinstance(message.reference.resolved, discord.Message)
        and message.reference.resolved.author == bot.user
    )

    if message.author == bot.user:
        pass

    elif message.content.startswith(bot.command_prefix):
        await bot.process_commands(message)

    elif rd.random() < PROBABILITY_INSULT or mentioned or replied_to_bot:
        username = message.author.display_name
        message_content = message.content
        try:
            response = await create_insult(username, message_content)
            await message.channel.send(response)
        except Exception as e:
            await message.channel.send(
                f"⚠️ An error has occured when generating the answer :\n{e}"
            )


@bot.command()
async def insult(ctx: Context, *, message: str):
    username = ctx.author.display_name
    response = await create_insult(username, message)
    await ctx.send(response)


@bot.command()
async def ping(ctx: Context):
    username = ctx.author.display_name
    date = datetime.now()
    await ctx.send(f"pong - {username} - {date} ")


@tasks.loop(seconds=60)
async def when_the_witcher():
    await bot.wait_until_ready()

    do_witcher = rd.random()
    if do_witcher < 60 / AVERAGE_DELAY_WITCHER:
        channel = bot.get_channel(TARGET_CHANNEL_ID)
        if channel is None:
            print("Channel not found.")
            return
        await channel.send("When the witcher ?")


@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user}")
    # when_the_witcher.start() # Uncomment if you want to casser les couilles d'Adrien


bot.run(bot_token)
