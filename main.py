import discord
import openai
from discord.ext import commands
from openai import OpenAI

#MAKE THIS HACKK PROOF
OPENAI_API_KEY = "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"
BOT_TOKEN = "MTIwMzIzMTc1ODAxNjA1NzM2NQ.G0QNjl.UsCsq_XFQwPzcIP3AT3ACqvVQuchIS7PbnZgMY"
CHANNEL_ID = 1203237203627737142

#client = OpenAI(
#  organization='moodBotBrain',
#)

bot = commands.Bot(command_prefix = "mb!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("its because im moodbot")

@bot.command()
async def hello(ctx):
    await ctx.send("Hello!")

async def mood(ctx):
    await ctx.send("You are sad")

bot.run(BOT_TOKEN)
