import discord
import openai
from discord.ext import commands
from openai import OpenAI
#MAKE THIS HACKK PROOF
#OPENAI_API_KEY = "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"
BOT_TOKEN = "MTIwMzIzMTc1ODAxNjA1NzM2NQ.G0QNjl.UsCsq_XFQwPzcIP3AT3ACqvVQuchIS7PbnZgMY"
CHANNEL_ID = 1203237203627737142
client = OpenAI(api_key = "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")

assistant = client.beta.assistants.create(
    name="Therapist",
    instructions="You are a therapist. Read messages and determine the emotion felt",
    tools=[{"type": "code_interpreter"}],
    model="gpt-3.5-turbo-1106"
)


thread = client.beta.threads.create()
print(thread)

#client = OpenAI(
#  organization='moodBotBrain',
#)

bot = commands.Bot(command_prefix = "mb!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("moodbot online motherfucker")


@bot.command()
async def hello(ctx):
    await ctx.send("Hello world "+ getAuthor(ctx).mention)
    
@bot.command()
async def mood(ctx, *arr):
    msg = ""
    for i in arr:
        msg += i + " "

    message = client.beta.threads.messages.create(
        thread_id = thread.id,
        role = "user",
        content = "What emotion is this message displaying? " + msg
    )
    print("What emotion is this message displaying " + msg)
    
    run = client.beta.threads.runs.create(
        thread_id = thread.id,
        assistant_id = assistant.id
    )
    run = client.beta.threads.runs.retrieve(
        thread_id = thread.id,
        run_id = run.id
    )
    messages = client.beta.threads.messages.list(
        thread_id = thread.id
    )
    for message in reversed(messages.data):
        await ctx.send(message.role + ": " + message.content[0].text.value)
        

@bot.command()
async def letter(ctx, messages):
    await ctx.send(messages)

@bot.command()
async def getMsg(ctx):
    channelID = getChannelId(ctx)
    string =""
    channel = bot.get_channel(channelID)
    async for msg in channel.history(limit=100):
        if msg.author.id == getAuthor(ctx).id:
            string = string +" "+ msg.content
    await ctx.send(string)

def getChannelId(ctx):
    return ctx.message.channel.id
def getAuthor(ctx):
    return ctx.message.author

def getMessages(ctx):
    ret = ""
    
    
    return ret


bot.run(BOT_TOKEN)