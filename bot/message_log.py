import functools

import discord


def send_command_error_to_discord(func):
    @functools.wraps(func)
    async def wrapper(interaction: discord.Interaction, *args, **kwargs):
        try:
            return await func(interaction, *args, **kwargs)
        except Exception as e:
            # Format the error message
            error_msg = f"⚠️ **An error occurred:** `{str(e)}`"
            await interaction.channel.send(error_msg)
            # Optional: Print to console for debugging
            print(f"Error in {func.__name__}: {e}")

    return wrapper


def send_response_error_to_discord(func):
    @functools.wraps(func)
    async def wrapper(message: discord.Message, *args, **kwargs):
        try:
            return await func(message, *args, **kwargs)
        except Exception as e:
            # Format the error message
            error_msg = f"⚠️ **An error occurred:** `{str(e)}`"
            await message.channel.send(error_msg)
            # Optional: Print to console for debugging
            print(f"Error in {func.__name__}: {e}")

    return wrapper
