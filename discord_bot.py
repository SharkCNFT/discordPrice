import discord # import the discord module
from discord.ext import commands, tasks # import the commands and tasks module from the discord.ext package
import aiohttp #import aiohttp module for handling asyncronous http requests

# CMC API Key and discord bot token, these will be used to authorize the requests to coinmarketcap and the bot
API_KEY = ''
BOT_TOKEN = ''

# Initialize the bot with command prefix "!" and all intents
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# bot event that runs when bot is ready
@bot.event
async def on_ready():
    # Once bot is ready, start fetching prices
    print("Beep Boop")
    cmcData.start()

# function to get the price data from coinmarketcap and return the latest ADA price
async def getCMCData():
    # Perform a GET request to the coinmarketcap API to get the latest price of ADA
    # Pass in the necessary parameters and headers for the request
    params = {'slug': 'cardano', 'convert': 'USD'}
    headers = {'Accepts': 'application/json', 'X-CMC_PRO_API_KEY': API_KEY}
    url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url=url, params=params) as response:
            resp = await response.json()
            # check if the API returns an error code of 0, indicating a successful request
            if resp['status']['error_code'] == 0:
                # 2010 is the ID given by CMC for ADA
                return resp['data']['2010']['quote']['USD']['price']

# command to rename the bot's status with the latest ADA price
@bot.command()
async def rename(currentPrice):
    # round the current price to 2 decimal places and convert it to string
    name = f"{currentPrice:.2f}"
    # change the bot's presence with the current ADA price
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"ADA @ ${name}"))

# Set to 5 minute intervals to coincide with limits to CMC's free api calls
@tasks.loop(seconds=300)
async def cmcData():
    # get the current ADA price and update the bot's presence
    await rename(await getCMCData())

# run the bot with the given token
bot.run(BOT_TOKEN)

