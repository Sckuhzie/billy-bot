import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
bot_token = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Bot connected as {bot.user}")


@bot.command()
async def hello(ctx):
    await ctx.send("Hello!")


bot.run(bot_token)
