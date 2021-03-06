import discord
import os
import requests
import json
from keep_alive import keep_alive
from logic import login
from logic import get_with_userid,setup,updateToLatestGames
from replit import db


client = discord.Client()

rankMap = {
  "0": "Unrated",
  "1": "Unknown 1",
  "2": "Unknown 2",
  "3": "Iron 1",
  "4": "Iron 2",
  "5": "Iron 3",
  "6": "Bronze 1",
  "7": "Bronze 2",
  "8": "Bronze 3",
  "9": "Silver 1",
  "10": "Silver 2",
  "11": "Silver 3",
  "12": "Gold 1",
  "13": "Gold 2",
  "14": "Gold 3",
  "15": "Platinum 1",
  "16": "Platinum 2",
  "17": "Platinum 3",
  "18": "Diamond 1",
  "19": "Diamond 2",
  "20": "Diamond 3",
  "21": "Immortal",
  "22": "Immortal",
  "23": "Immortal",
  "24": "Radiant"
}


def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='!help'))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    
    if message.content.startswith('!server'):
        await message.channel.send(f'Currently, ValoElo Bot is active at {len(client.guilds)} servers')
    
    if message.content.startswith('!quote'):
        quote = get_quote()
        await message.channel.send(quote)
    
    if message.content.startswith('!setup'): 
        msg_in = message.content.split(" ")
        try:
          await setup(msg_in,message.author.mention)
        except:
          await message.channel.send("Player not found!!! Use !setup again")
        else:
          await message.channel.send('Information saved! Now you can use command !rank')

    if message.content.startswith('!help'):
        embedVar = discord.Embed(title='ValoElo Help', description="To know your rank, you first have to configure the bot", color=0x0099ff)
        embedVar.add_field(name="To setup use :", value='**!setup** <user-id> <region-code>', inline=False)
        embedVar.add_field(name="Example", value='!setup playername#tagline ap', inline=False)
        embedVar.add_field(name="Then you can use command", value='**!rank**', inline=False)
        embedVar.add_field(name="Region Codes", value='use these code during setup', inline=False)
        embedVar.add_field(name="Asia", value='ap', inline=True)
        embedVar.add_field(name="Europe", value='eu', inline=True)
        embedVar.add_field(name="America", value='na', inline=True)
        embedVar.add_field(name="Korea", value='kr', inline=True)
        embedVar.set_footer(text='This bot is not affliated with Riot Games. This bot is not injecting or modifying the game in any sort of way. It is simply just making a webrequest to your API which then returns a json that I parse and display. If Riot Games have any issue then I am ready to take this project down.')
        await message.channel.send(embed=embedVar)

    if message.content.startswith('!rank'):
        try:
            user = db[message.author.mention]
        except:
            await message.channel.send('Use !setup first')
        try:
            data = await get_with_userid(os.getenv('USERNAME'), os.getenv('PASSWORD'), user['puuid'], user['region'])
            matches = data['Matches']
        except:
            await message.channel.send('error: userid not found or invalid, check your region too')
        for element in matches:
            if(element['RankedRatingAfterUpdate'] != 0):
                match = element
                break
            else:
                match = element
        TierAfterUpdate = match['TierAfterUpdate'] * 100
        rr = match['RankedRatingAfterUpdate'];
        rank = rankMap[f"{match['TierAfterUpdate']}"]
        embedVar = discord.Embed(title=user['name'], description=rank, color=0x0099ff)
        embedVar.set_thumbnail(url=f'https://firebasestorage.googleapis.com/v0/b/cloud-storage-test-ac898.appspot.com/o/{match["TierAfterUpdate"]}.png?alt=media')
        embedVar.add_field(name="Rank Rating", value=rr, inline=True)
        embedVar.add_field(name="Elo", value=TierAfterUpdate - 300 + rr, inline=True)
        embedVar.add_field(name="Rating for last 3 match", value=updateToLatestGames(matches), inline=True)
        await message.channel.send(embed=embedVar)
        
keep_alive()
client.run(os.getenv('TOKEN'))