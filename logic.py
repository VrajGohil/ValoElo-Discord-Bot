import re
import aiohttp
import json
from replit import db

async def login(username, password):
    session = aiohttp.ClientSession()
    data = {
        'client_id': 'play-valorant-web-prod',
        'nonce': '1',
        'redirect_uri': 'https://playvalorant.com/opt_in',
        'response_type': 'token id_token',
    }
    await session.post('https://auth.riotgames.com/api/v1/authorization', json=data)

    data = {
        'type': 'auth',
        'username': username,
        'password': password
    }
    async with session.put('https://auth.riotgames.com/api/v1/authorization', json=data) as r:
        data = await r.json()
    pattern = re.compile('access_token=((?:[a-zA-Z]|\d|\.|-|_)*).*id_token=((?:[a-zA-Z]|\d|\.|-|_)*).*expires_in=(\d*)')
    data = pattern.findall(data['response']['parameters']['uri'])[0]
    access_token = data[0]
    print('Access Token: ' + access_token)
    id_token = data[1]
    expires_in = data[2]

    headers = {
        'Authorization': f'Bearer {access_token}',
        'X-Riot-ClientPlatform':'ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9'
    }
    async with session.post('https://entitlements.auth.riotgames.com/api/token/v1', headers=headers, json={}) as r:
        data = await r.json()
    entitlements_token = data['entitlements_token']
    print('Entitlements Token: ' + entitlements_token)

    async with session.post('https://auth.riotgames.com/userinfo', headers=headers, json={}) as r:
        data = await r.json()
    user_id = data['sub']
    print('User ID: ' + user_id)
    headers['X-Riot-Entitlements-JWT'] = entitlements_token
    
    async with session.get(f'https://pd.eu.a.pvp.net/mmr/v1/players/{user_id}/competitiveupdates?startIndex=0&endIndex=20', headers=headers) as r:
        data = json.loads(await r.text())
    print(data)

    await session.close()
    return(data)

def updateToLatestGames(matches):
    points = []
    if (len(matches) != 0):
        count = 0
        for game in matches:
            if (game["TierAfterUpdate"] == 0):
                print("No movement")
            else:
                points.append(game["RankedRatingEarned"])
                count+=1

            if (count >= 3):
                break
    return points

async def setup(msg_in,discord_user):
    session = aiohttp.ClientSession()
    player_name = msg_in[1].split("#")[0]
    tagline = msg_in[1].split("#")[1]
    async with session.get(f'https://api.henrikdev.xyz/valorant/v1/puuid/{player_name}/{tagline}') as r:
        data = json.loads(await r.text())
        puuid = data['data']['puuid']
    await session.close()
    db[discord_user] = {"name":msg_in[1],"region": msg_in[2],"puuid": puuid}
    return data

async def get_with_userid(username, password,user_id,region):
    session = aiohttp.ClientSession()
    data = {
        'client_id': 'play-valorant-web-prod',
        'nonce': '1',
        'redirect_uri': 'https://playvalorant.com/opt_in',
        'response_type': 'token id_token',
    }
    await session.post('https://auth.riotgames.com/api/v1/authorization', json=data)

    data = {
        'type': 'auth',
        'username': username,
        'password': password
    }
    async with session.put('https://auth.riotgames.com/api/v1/authorization', json=data) as r:
        data = await r.json()
    pattern = re.compile('access_token=((?:[a-zA-Z]|\d|\.|-|_)*).*id_token=((?:[a-zA-Z]|\d|\.|-|_)*).*expires_in=(\d*)')
    data = pattern.findall(data['response']['parameters']['uri'])[0]
    access_token = data[0]
    print('Access Token: ' + access_token)
    id_token = data[1]
    expires_in = data[2]

    headers = {
        'Authorization': f'Bearer {access_token}',
        'X-Riot-ClientPlatform':'ew0KCSJwbGF0Zm9ybVR5cGUiOiAiUEMiLA0KCSJwbGF0Zm9ybU9TIjogIldpbmRvd3MiLA0KCSJwbGF0Zm9ybU9TVmVyc2lvbiI6ICIxMC4wLjE5MDQyLjEuMjU2LjY0Yml0IiwNCgkicGxhdGZvcm1DaGlwc2V0IjogIlVua25vd24iDQp9'
    }
    async with session.post('https://entitlements.auth.riotgames.com/api/token/v1', headers=headers, json={}) as r:
        data = await r.json()
    entitlements_token = data['entitlements_token']
    print('Entitlements Token: ' + entitlements_token)
    print('User ID: ' + user_id)
    headers['X-Riot-Entitlements-JWT'] = entitlements_token
    
    # Example Request. (Access Token and Entitlements Token needs to be included!)
    async with session.get(f'https://pd.{region}.a.pvp.net/mmr/v1/players/{user_id}/competitiveupdates?startIndex=0&endIndex=20', headers=headers) as r:
        data = json.loads(await r.text())
    print(data)

    await session.close()
    return(data)