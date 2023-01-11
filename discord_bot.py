import discord
from discord.ext import commands, tasks
import aiohttp
import sys

# CMC API Key, discord bot token
API_KEY = ''
BOT_TOKEN = ''

# Command prefix to command the bot 
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
@bot.event
async def on_ready():
    # Once bot is ready, start fetching prices
    print("Beep Boop")
    cmcData.start()

async def getCMCData():
    # returns price from CMC
    # Change slug to whatever is appropriate, check CMC's documentation 
    params = {'slug': 'cardano',
              'convert': 'USD'}
    headers = {'Accepts': 'application/json',
               'X-CMC_PRO_API_KEY': API_KEY}
    url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url=url, params=params) as response:
            resp = await response.json()
            if resp['status']['error_code'] == 0:
                print(resp)
                # 2010 is the ID given by CMC for ADA, less logic to hardcode it
                return resp['data']['2010']['quote']['USD']['price']

@bot.command()
async def rename(currentPrice):
    name = str(round(currentPrice, 2))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"ADA @ ${name}"))

# Set to 5 minute intervals to coincide with limits to CMC's free api calls
@tasks.loop(seconds=300)
async def cmcData():
    currentPrice = await getCMCData()
    await rename(currentPrice)

bot.run(BOT_TOKEN)
