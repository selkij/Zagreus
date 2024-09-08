import discord
import os

from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands

load_dotenv()

bot = commands.Bot(command_prefix='.', intents=discord.Intents.all())


@bot.event
async def on_ready():
    game = discord.Game("My father annoys me.")
    await bot.change_presence(status=discord.Status.idle, activity=game)
    print(f"Logged on as {bot.user}!")


@bot.tree.command(name="sync", description="Sync all commands.")
@commands.is_owner()
async def sync(interaction: discord.Interaction) -> None:
    try:
        await interaction.response.send_message("Syncing...", ephemeral=True)
        try:
            synced = await bot.tree.sync(guild=None)
            await interaction.response.edit_original_message(content=f"Synced {len(synced)} command(s).")
            print(f"Synced {len(synced)} command(s)")
        except Exception as e:
            await interaction.response.edit_original_message(content=f"Syncing command(s) failed.")
            print(f"Failed to sync command(s) {e}.")

    except Exception as e:
        print(f"Error occurred syncing command(s): {e}")


@bot.tree.command(name="ping", description="Pong!")
async def ping(interaction: discord.Interaction) -> None:
    await interaction.response.send_message(f"Pong! {round(bot.latency * 1000)}ms", ephemeral=True)


bot.run(os.getenv('TOKEN'))
