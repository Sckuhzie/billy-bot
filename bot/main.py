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
from when_the_witcher import create_list_polls_witcher, secure_when_the_witcher

load_dotenv()
bot_token = os.getenv("DISCORD_BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True  # Optional but good practice

bot = commands.Bot(command_prefix="!", intents=intents)

# Non mutable global variable
WITCHER_CHANNEL_ID = 1398972120326869022  # TODO: Change to witcher channel


# Mutable global variable
PROBABILITY_INSULT = 1 / 30
AVERAGE_DELAY_WITCHER = (
    3.5 * 24 * 60 * 60  # Half a week, the bot will say it twice a week
)  # Average time between each "When the witcher in seconds"
global_var = GlobalVars()
global_var.add("PROBABILITY_INSULT", PROBABILITY_INSULT)
global_var.add("AVERAGE_DELAY_WITCHER", AVERAGE_DELAY_WITCHER)
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


@bot.command()
async def toggle_witcher(ctx: Context, state: bool):
    print(state)
    print(type(state))
    global_var.set("DO_WITCHER", state)
    if state:
        await ctx.send("When witcher enabled")
    else:
        await ctx.send("When witcher disabled")


@tasks.loop(seconds=60)
async def when_the_witcher_loop():
    await bot.wait_until_ready()

    do_witcher = rd.random()
    if global_var.get("DO_WITCHER") and do_witcher < 60 / global_var.get(
        "AVERAGE_DELAY_WITCHER"
    ):
        channel = bot.get_channel(WITCHER_CHANNEL_ID)
        if channel is None:
            print("Channel not found.")
            return
        await channel.send("When the witcher ?")


# Tentative de commandes propre
@bot.tree.command(name="when_the_witcher", description="WhEn tHe WiTcHeR ???")
# @bot.command()
async def when_the_witch(interaction: discord.Interaction):
    await interaction.response.send_message("WHEN ?")


# @bot.tree.command(name="when_the_witcher")
@bot.command()
async def when_the_witcher(ctx: Context, start_date: str = None, end_date: str = None):
    """Create poll for each week-end until the end of the next month for planning future Witcher sessions"""
    try:
        start_date, end_date = secure_when_the_witcher(start_date, end_date)
    except ValueError as err:
        ctx.send(err)

    print(start_date, end_date)
    list_polls = create_list_polls_witcher(start_date, end_date)
    for p in list_polls:
        await ctx.send(poll=p)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot connected as {bot.user}")
    # when_the_witcher_loop.start()


bot.run(bot_token)
