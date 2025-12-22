import os
import random as rd
from datetime import datetime
from enum import Enum

import discord
from discord.ext import commands, tasks
from discord.ext.commands import Context
from dotenv import load_dotenv
from insult import create_insult, create_message_stack
from yt_playlist import get_playlist_diff, save_playlist_txt

load_dotenv()
bot_token = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True  # Optional but good practice

bot = commands.Bot(command_prefix="!", intents=intents)

# Global variables
PLAYLIST_CHANNEL_ID = 804844751320645633  # 1398972120326869022
PROBABILITY_INSULT = 1 / 50


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

    if mentioned or replied_to_bot or rd.random() < PROBABILITY_INSULT:
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


@bot.tree.command(
    name="playlist_diff",
    description="Get diff of play list",
)
async def playlist_diff(interaction: discord.Interaction, playlist_name: PlaylistEnum):
    await interaction.response.defer()
    playlist_id = playlist_name.value
    version_date, list_message = get_playlist_diff(playlist_id)
    if len(list_message) == 0:
        await interaction.followup.send(
            f"No change in the playlist: {playlist_name.name}"
        )
        return
    await interaction.followup.send(
        f"Playlist : {playlist_name.name}, saved version : {version_date}"
    )
    for message in list_message:
        await interaction.channel.send(message)


@bot.tree.command(
    name="save_playlist",
    description="Save the new state of a playlist",
)
async def save_playlist(interaction: discord.Interaction, playlist_name: PlaylistEnum):
    await interaction.response.defer()
    playlist_id = playlist_name.value
    save_playlist_txt(playlist_id)
    await interaction.followup.send(f"Playlist saved")


@tasks.loop(hours=24 * 7)
async def playlist_loop():
    await bot.wait_until_ready()

    for playlist in PlaylistEnum:
        version_date, message_list = get_playlist_diff(playlist.value)
        channel = bot.get_channel(PLAYLIST_CHANNEL_ID)
        if channel is None:
            print("Channel not found")
            return
        await channel.send(
            f"Playlist : {playlist.name}, saved version : {version_date}"
        )
        if len(message_list) == 0:
            await channel.send("No changes")
        for message in message_list:
            await channel.send(message)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot connected as {bot.user}")
    playlist_loop.start()


bot.run(bot_token)
