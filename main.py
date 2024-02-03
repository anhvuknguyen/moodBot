import discord
import openai
from discord.ext import commands
from openai import OpenAI
from .gitignore import BOT_TOKEN
from .gitignore import CHANNEL_ID
from .gitignore import OPENAI_API_KEY


client = OpenAI(
  organization='moodBotBrain',
)

bot = commands.Bot(command_prefix = "mb!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print("Hello World!")

bot.run(BOT_TOKEN)