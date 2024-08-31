import discord
import openai
from discord.ext import commands
from openai import OpenAI
import responses as r
import asyncio
import keys

#the best bot discord has
BOT_TOKEN = keys.BOT_TOKENsec
CHANNEL_ID = keys.CHANNEL_IDsec
client = OpenAI(api_key = keys.OPENAI_API_KEYsec)

assistant = client.beta.assistants.create(
    name="Therapist",
    instructions="You are a therapist. Read messages and determine the emotion felt. If needed uplift the user's emotion.",
    tools=[{"type": "code_interpreter"}],
    model="gpt-3.5-turbo-0125"   
)

async def messageAssistant(msg):
    thread = client.beta.threads.create()
    message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content="What emotion is this message display? Respond with happy phrase if it's negative." + msg
        )
        
    #Execute the thread
    run = client.beta.threads.runs.create(
        thread_id = thread.id,
        assistant_id = assistant.id,
        model="gpt-3.5-turbo-0125",
        instructions = "Respond with the emotion in this message. Use your vast knowledge on emotions and personality to choose the correct feeling. Keep responses one word, use a complex word. If the emotion seems to be negative IGNORE the one word response rule, please respond with the emotion and an uplifting phrase.",
        tools=[{"type": "code_interpreter"}]
    )
    return thread,message,run

def messageAssistant2(thread,message,run):
    #Retrive the run result
    run = client.beta.threads.runs.retrieve(
        thread_id = thread.id,
        run_id = run.id
    )   
        #Get the last message from the thread which is assumed to be the answer
    messages = client.beta.threads.messages.list(
        thread_id = thread.id
    )
    print(messages)
        #response = r.create_response(assistant, msg)
        #await ctx.send(response)
    for message in reversed(messages.data):
        print(message.role + ": " + message.content[0].text.value)
    return messages

bot = commands.Bot(command_prefix = "mb!", intents=discord.Intents.all())

@bot.event
async def on_ready():
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("MoodBot Online")

@bot.command()
async def hello(ctx):
    await ctx.send("Hello world "+ getAuthor(ctx).mention)
    
        
@bot.command()
async def mood(ctx, *arr):
        messageCall = "mb!"
        userID = ""
        for i in arr:
            userID += i + " "
        userID = userID[userID.index("@")+1:userID.index(">")]
        channelID = getChannelId(ctx)
        string =""
        channel = bot.get_channel(channelID)
        count = 0
        async for msg in channel.history(limit=500):
            msgID = str(msg.author.id)
            if msgID == userID:
                if messageCall in msg.content:
                    continue 
                if msg.content == "":
                    continue
                if "https" in msg.content:
                    continue
                string = string +" "+ msg.content
                count += 1
                if count >= 5:
                    break
        msg = " " + string 
        thread,messageRun,Run = await messageAssistant(msg)
        await asyncio.sleep(3)
        mood = messageAssistant2(thread,messageRun,Run)
        for message in (mood.data):
            await ctx.send("Your mood for the last five messages: " + message.content[0].text.value)
            break

@bot.command()
async def letter(ctx, messages):
    await ctx.send(messages)

@bot.command()
async def getMsg(ctx, *arr):
    userID = ""
    for i in arr:
        userID += i + " "
    userID = userID[userID.index("@")+1:userID.index(">")]
    channelID = getChannelId(ctx)
    string =""
    channel = bot.get_channel(channelID)
    count = 0
    async for msg in channel.history(limit=500):
        print(msg.author.id)
        print(userID)
        msgID = str(msg.author.id)
        if msgID == userID:
            string = string +" "+ msg.content
            print("we are here")
            count += 1
            if count >= 5:
                break
    print(string)
    return string

def getChannelId(ctx):
    return ctx.message.channel.id
def getAuthor(ctx):
    return ctx.message.author

bot.run(BOT_TOKEN)