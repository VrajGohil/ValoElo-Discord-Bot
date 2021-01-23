import discord
import os
import requests
import json
from keep_alive import keep_alive
from logic import login
from logic import updateToLatestGames
from logic import get_with_userid
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
  "22": "Radiant"
}


def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    
    if message.content.startswith('!quote'):
        quote = get_quote()
        await message.channel.send(quote)
    
    if message.content.startswith('!setup'): 
        msg_in = message.content.split(" ") 
        db[message.author.mention] = {"name":msg_in[1],"region": msg_in[2]}
        await message.channel.send('Information saved! Now you can use command !rank')

    if message.content.startswith('!help'):
        await message.channel.send('To know your rank use, first add your details using command : !setup <user-id> <region-code>\n\n Then you can user command !rank\n\nRegion Codes :\n  Asia - ap\n  Europe- eu\n  America - na\n  Korea - kr')

    if message.content.startswith('!rank'):
        try:
            user = db[message.author.mention]
        except:
            await message.channel.send('Use !setup first')
        data = await get_with_userid('forthepain', 'Microstar1', user['name'], user['region'])
        matches = data['Matches']
        for element in matches:
            if(element['RankedRatingAfterUpdate'] != 0):
                match = element
                break
            else:
                match = element
        TierAfterUpdate = match['TierAfterUpdate'] * 100
        rr = match['RankedRatingAfterUpdate'];
        rank = rankMap[f"{match['TierAfterUpdate']}"]
        msg_out = f'https://firebasestorage.googleapis.com/v0/b/cloud-storage-test-ac898.appspot.com/o/{match["TierAfterUpdate"]}.png?alt=media\nRank : {rank}\nRank Rating : {rr}\nElo : {TierAfterUpdate - 300 + rr}\nRating for last 3 match : {updateToLatestGames(matches)}'
        await message.channel.send(msg_out)
    
    # if message.content.startswith('!rank'):
    #     msg_in = message.content.split(" ")
    #     data = await login(msg_in[1],msg_in[2])
    #     matches = data['Matches']
    #     for element in matches:
    #         if(element['RankedRatingAfterUpdate'] != 0):
    #             match = element
    #             break
    #         else:
    #             match = element
    #     TierAfterUpdate = match['TierAfterUpdate'] * 100
    #     rr = match['RankedRatingAfterUpdate'];
    #     msg_out = f'Rank Rating : {rr}\nElo : {TierAfterUpdate - 300 + rr}\nRating for last 3 match : {updateToLatestGames(matches)}'
    #     await message.channel.send(msg_out)
        
keep_alive()
client.run(os.getenv('TOKEN'))