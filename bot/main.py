import os
import random as rd
from datetime import datetime, timedelta
from enum import Enum
import discord
from discord.ext import commands, tasks
from discord.ext.commands import Context
from dotenv import load_dotenv
from global_var import GlobalVars
from insult import create_insult, create_message_stack
from yt_playlist import get_playlist_diff, save_playlist_txt

load_dotenv()
bot_token = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True  # Optional but good practice

bot = commands.Bot(command_prefix="!", intents=intents)


# Mutable global variable
PROBABILITY_INSULT = 1 / 30
global_var = GlobalVars()
global_var.add("PROBABILITY_INSULT", PROBABILITY_INSULT)
global_var.add("DO_WITCHER", False)


class PlaylistEnum(Enum):
    LOOSE = "PLs5RvnKyJmy74KrJ0YdR_W3zFvKRfMwTE"
    SURPLUS = "PLs5RvnKyJmy55bJR-uYQHyZk4DMoqZGAg"
    INCLUSION = "PLs5RvnKyJmy6g8B2LcllOMMQkIQUwS-VX"
    CLAQUES = "PL0p2EkWqwO1Ac7EvGTsKjJl2Kgp7Q7WFv"
    RETOMBEES = "PL0p2EkWqwO1Bb2eKwvBjFWtX4JQ-k5r0Y"


@bot.event
async def on_message(message: discord.Message):

    mentioned = bot.user in message.mentions
    replied_to_bot = (
        message.reference
        and isinstance(message.reference.resolved, discord.Message)
        and message.reference.resolved.author == bot.user
    )

    if message.author == bot.user:
        return

    if message.content.startswith(bot.command_prefix):
        await bot.process_commands(message)
        return

    if (
        mentioned
        or replied_to_bot
        or rd.random() < global_var.get("PROBABILITY_INSULT")
    ):
        messages_stack = create_message_stack(message, bot.user)

        try:
            response = await create_insult(messages_stack)
            await message.reply(response, mention_author=False)
        except Exception as e:
            await message.channel.send(
                f"⚠️ An error has occured when generating the answer :\n{e}"
            )
    return


@bot.command()
async def ping(ctx: Context):
    username = ctx.author.display_name
    date = datetime.now()
    await ctx.send(f"pong - {username} - {date} ")


@bot.command()
async def get_variables(ctx: Context):
    await ctx.send(f"```{global_var.all}```")


@bot.command()
async def set_variable_float(ctx: Context, key: str, value: float):
    global_var.set(key, value)
    await ctx.send(f"{key} set successfully set to {value}")


@bot.tree.command(
    name="playlist_diff",
    description="Get diff of play list",
)
async def playlist_diff(interaction: discord.Interaction, playlist_name: PlaylistEnum):
    playlist_id = playlist_name.value
    message = get_playlist_diff(playlist_id)
    await interaction.response.send_message(message)


@bot.tree.command(
    name="save_playlist",
    description="Save the new state of a playlist",
)
async def playlist_diff(interaction: discord.Interaction, playlist_name: PlaylistEnum):
    playlist_id = playlist_name.value
    output = save_playlist_txt(playlist_id)
    await interaction.response.send_message(f"Playlist saved")


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot connected as {bot.user}")


bot.run(bot_token)
