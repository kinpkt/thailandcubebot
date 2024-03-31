import os
import json
import random
import asyncio
import pymongo
import discord
import lang_str
import requests
import scrambles
from dotenv import load_dotenv
from translate import Translator
from discord.ext import commands
from pythainlp.transliterate import puan as spooner

load_dotenv()

ADMIN_DISCORD_ID = [492332351561400320, 336475825601904641]
WCA_API_LINK = 'https://www.worldcubeassociation.org/api/v0'
CONTINENT_ID = {'_Africa': 'แอฟริกา', '_Asia': 'เอเชีย', '_Europe': 'ยุโรป', '_North America': 'อเมริกาเหนือ', '_Oceania': 'โอเชียเนีย', '_South America': 'อเมริกาใต้'}
EVENT_ID = {'333': '3x3x3 Cube', '222': '2x2x2 Cube', '444': '4x4x4 Cube', '555': '5x5x5 Cube', '666': '6x6x6 Cube', '777': '7x7x7 Cube', '3bld': '3x3x3 Blindfolded', 'fmc': '3x3x3 Fewest Moves', 'oh': '3x3x3 One-Handed', 'clock': 'Clock', 'mega': 'Megaminx', 'pyra': 'Pyraminx', 'skewb': 'Skewb', 'sq1': 'Square-1', '4bld': '4x4x4 Blindfolded', '5bld': '5x5x5 Bilndfolded'}
EVENT_CODE = ['333', '222', '444', '555', '666', '777', '3bld', 'fmc', 'oh', 'clock', 'mega', 'pyra', 'skewb', 'sq1', '4bld', '5bld']
AO5_EVENTS = ['333', '222', '444', '555', 'oh', 'clock', 'mega', 'pyra', 'skewb', 'sq1']
MO3_EVENTS = ['666', '777']
BOX_EVENTS = ['3bld', 'fmc', '4bld', '5bld']
PREFIX = '-'

CLIENT = pymongo.MongoClient(os.getenv('DB_AUTH'))
DATABASE = CLIENT['thcbot']
LANG_TABLE = DATABASE['lang']
RESULTS_TABLE = DATABASE['weeklyresult']

def GET_USER_LANG(id):
    id_query = {'user_id': id}
    query_result = LANG_TABLE.find_one(id_query)
    if query_result is None:
        lang = 'th'
    else:
        lang = query_result['lang_id']
    return lang

def IS_VALID_ATTEMPT(attempt):
    try:
        float(attempt)
        return True
    except ValueError:
        if attempt.upper() == 'DNF' or attempt.upper() == 'DNS':
            return True
        else:
            return False
    except TypeError:
        if attempt is None:
            return True

def SEC2MIN(seconds):
    minutes = int(seconds // 60)
    remaining_seconds = int(seconds % 60)
    milliseconds = int((seconds % 1) * 1000)
    return "{:02d}:{:02d}.{:02d}".format(minutes, remaining_seconds, milliseconds) if minutes >= 10 else "{:01d}:{:02d}.{:02d}".format(minutes, remaining_seconds, milliseconds)

print('Successfully connected to the database.')

intents = discord.Intents.all()
intents.message_content = True

client = commands.Bot(command_prefix=PREFIX, case_insensitive=True, help_command=None, intents=intents)

th_translate = Translator(to_lang='Thai')

@client.event
async def on_ready():
    print('THC Bot is now online.')

@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as file:
        prefixes = json.load(file)
    prefixes[str(guild.id)] = '-'
    with open('prefixes.json', 'w') as file:
        json.dump(prefixes, file, indent=4)

@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as file:
        prefixes = json.load(file)
    prefixes.pop(str(guild.id))
    with open('prefixes.json', 'w') as file:
        json.dump(prefixes, file, indent=4)

@client.command()
async def help(ctx):
    lang = GET_USER_LANG(ctx.author.id)
    return await ctx.send('https://drive.google.com/file/d/15pgT27nR8yvBQO3x8YdDbk3EU54YgW6M/view?usp=sharing') if lang == 'en' else await ctx.send('https://drive.google.com/file/d/1aSeI5s415Q1hszS7ndpLrCMuMwX1ZeKx/view?usp=sharing')

@client.command()
async def puan(ctx, word):
    if word == 'ชายสี่':
        return await ctx.reply('หมี่เกี๊ยว')
    elif word == '1212312121':
        return await ctx.reply('เฮ้!')
    elif word == 'หมี่เกี๊ยว':
        return await ctx.reply('ซายสี่')
    elif word == 'ไวพจน์เพชรสุพรรณ':
        await ctx.send('เอ้ย')
        return await ctx.reply('ถูกแล้ว!')
    await ctx.reply(spooner(word, False))

@client.command()
async def whois(ctx, wcaid = None):
    user_lang = GET_USER_LANG(ctx.author.id)
    await ctx.typing()
    if wcaid is None:
        return await ctx.reply(lang_str.no_wca_id(ctx.author.id))
    PERSONS_LINK = WCA_API_LINK + '/persons/' + wcaid.upper()
    data = requests.get(PERSONS_LINK).json()
    if 'error' in data:
        return await ctx.reply(lang_str.incr_wca_id(ctx.author.id))
    name = data['person']['name']
    pfp = data['person']['avatar']['url']
    country = th_translate.translate(data['person']['country']['name']) if user_lang == 'th' else data['person']['country']['name']
    comp_num = data['competition_count']
    content_lang = lang_str.whois_embed_conts(user_lang)
    embed = discord.Embed(title=name, url=f'https://www.worldcubeassociation.org/persons/{wcaid.upper()}')
    embed.set_image(url=pfp)
    embed.add_field(name=content_lang[0], value=country, inline=True)
    embed.add_field(name=content_lang[1], value=comp_num, inline=True)
    if data['medals']['total'] > 0:
        gold_num = data['medals']['gold']
        silver_num = data['medals']['silver']
        bronze_num = data['medals']['bronze']
        embed.add_field(name='** **', value='** **', inline=False)
        embed.add_field(name=content_lang[2], value=gold_num, inline=True)
        embed.add_field(name=content_lang[3], value=silver_num, inline=True)
        embed.add_field(name=content_lang[4], value=bronze_num, inline=True)
    if data['records']['total'] > 0:
        wr = data['records']['world']
        cr = data['records']['continental']
        nr = data['records']['national']
        embed.add_field(name='** **', value='** **', inline=False)
        embed.add_field(name=content_lang[5], value=wr, inline=True)
        embed.add_field(name=content_lang[6], value=cr, inline=True)
        embed.add_field(name=content_lang[7], value=nr, inline=True)
    embed.set_footer(text=content_lang[8])
    await ctx.reply(embed=embed)

@client.command()
async def mo3(ctx, a1 = None, a2 = None, a3 = None):
    attempts = [a1, a2, a3]
    if None in attempts:
        return await ctx.reply(lang_str.calculator_missing_attempt(ctx.author.id, 3))
    attempts = [i.lower() for i in attempts]
    if 'dnf' in attempts or 'dns' in attempts:
        result = 'DNF'
    else:
        attempts = [float(i) for i in attempts]
        result = sum(attempts) / len(attempts)
        result = f'{result:.2f}'
    await ctx.reply(f'Mo3 of {a1}, {a2}, {a3} = {result}')

@client.command()
async def ao5(ctx, a1 = None, a2 = None, a3 = None, a4 = None, a5 = None):
    attempts = [a1, a2, a3, a4, a5]
    dnf_count = 0
    if None in attempts:
        return await ctx.reply(lang_str.calculator_missing_attempt(ctx.author.id, 5))
    attempts = [i.lower() for i in attempts]
    for i in attempts:
        if i == 'dnf' or i == 'dns':
            dnf_count += 1
        if dnf_count > 1:
            result = 'DNF'
    if dnf_count == 1:
        attempts.remove('dnf' if 'dnf' in attempts else 'dns')
        attempts = [float(i) for i in attempts]
        attempts.sort()
        result = sum(attempts[1:]) / len(attempts[1:])
        result = f'{result:.2f}'
    elif dnf_count == 0:
        attempts = [float(i) for i in attempts]
        attempts.sort()
        result = sum(attempts[1:-1]) / len(attempts[1:-1])
        result = f'{result:.2f}'
    await ctx.reply(f'Ao5 of {a1}, {a2}, {a3}, {a4}, {a5} = {result}')

@client.command()
async def getbpawpa(ctx, a1 = None, a2 = None, a3 = None, a4 = None):
    attempts = [a1, a2, a3, a4]
    dnf_count = 0
    if None in attempts:
        return await ctx.reply(lang_str.calculator_missing_attempt(ctx.author.id, 4))
    attempts = [i.lower() for i in attempts]
    if attempts == ['5.41', 'dnf', 'dnf', 'dnf']:
        return await ctx.reply("Is that you Yindee?")
    for i in attempts:
        if i == 'dnf' or i == 'dns':
            dnf_count += 1
        if dnf_count > 1:
            result = 'DNF'
    if dnf_count == 1:
        attempts.remove('dnf' if 'dnf' in attempts else 'dns')
        attempts = [float(i) for i in attempts]
        attempts.sort()
        bpa = sum(attempts) / 3
        bpa = f'{bpa:.2f}'
        wpa = 'DNF'
    elif dnf_count == 0:
        attempts = [float(i) for i in attempts]
        attempts.sort()
        bpa = sum(attempts[:-1]) / 3
        bpa = f'{bpa:.2f}'
        wpa = sum(attempts[1:]) / 3
        wpa = f'{wpa:.2f}'
    await ctx.reply(f'Your BPA is {bpa} and WPA is {wpa}.')

@client.command()
async def generate(ctx, event, attempts):
    scr = scrambles.gen(event, attempts)
    for i in range(len(scr)):
        await ctx.send(scr[i])

@client.command()
async def togglelang(ctx):
    id_query = {'user_id': ctx.author.id}
    query_result = LANG_TABLE.find_one(id_query)
    if query_result is None:
        data = {'user_id': ctx.author.id, 'lang_id': 'en'}
        LANG_TABLE.insert_one(data)
        return await ctx.reply(f'Successfully change the language to English for <@{ctx.author.id}>.')
    elif query_result['lang_id'] == 'en':
        LANG_TABLE.update_one(id_query, {'$set': {'lang_id': 'th'}})
        return await ctx.reply(f'Successfully change the language to Thai for <@{ctx.author.id}>.')
    else:
        LANG_TABLE.update_one(id_query, {'$set': {'lang_id': 'en'}})
        return await ctx.reply(f'Successfully change the language to English for <@{ctx.author.id}>.')

@client.command()
async def getlang(ctx):
    id_query = {'user_id': ctx.author.id}
    query_result = LANG_TABLE.find(id_query)
    print(len(query_result))
    
@client.command()
async def submit(ctx, event, a1, a2 = None, a3 = None, a4 = None, a5 = None):
    attempts = [a1, a2, a3, a4, a5]
    for i in range(len(attempts)):
        if IS_VALID_ATTEMPT(attempts[i]):
            continue
        else:
            return await ctx.reply(lang_str.invalid_attempt(ctx.author.id, i + 1))
    none_count = len([True for i in attempts if i is None])
    if event.lower() not in EVENT_CODE:
        await ctx.reply('กรุณาใส่รหัสรายการแข่งขันให้ถูกต้อง')
    elif event.lower() in AO5_EVENTS:
        if None in attempts:
            await ctx.reply(lang_str.submit_not_n(ctx.author.id, 5))
        else:
            # Calculating Ao5
            attempts = [i.lower() for i in attempts]
            dnf_count = len([True for i in attempts if i == 'dnf' or i == 'dns'])
            for i in attempts:
                if i == 'dnf' or i == 'dns':
                    dnf_count += 1
                if dnf_count > 1:
                    result = -1
            if dnf_count == 1:
                attempts.remove('dnf' if 'dnf' in attempts else 'dns')
                attempts = [float(i) for i in attempts]
                attempts.sort()
                result = sum(attempts[1:]) / len(attempts[1:])
                result = f'{result:.2f}'
            elif dnf_count == 0:
                attempts = [float(i) for i in attempts]
                attempts.sort()
                result = sum(attempts[1:-1]) / len(attempts[1:-1])
                result = float(f'{result:.2f}')
            result_dict = {'user_id': ctx.author.id, 'event': event, 'a1': a1, 'a2': a2, 'a3': a3, 'a4': a4, 'a5': a5, 'result': result}
            RESULTS_TABLE.insert_one(result_dict)
            await ctx.reply(lang_str.success_submit(ctx.author.id))
    elif event.lower() in MO3_EVENTS:
        if none_count >= 3:
            return await ctx.reply(lang_str.submit_not_n(ctx.author.id, 3))
        else:
            attempts = [i.lower() for i in attempts if i is not None]
            if 'dnf' in attempts or 'dns' in attempts:
                result = -1
            else:
                attempts = [float(i) for i in attempts]
                result = sum(attempts) / len(attempts)
                result = float(f'{result:.2f}')
            result_dict = {'user_id': ctx.author.id, 'event': event, 'a1': a1, 'a2': a2, 'a3': a3, 'a4': a4, 'a5': a5, 'result': result}
            RESULTS_TABLE.insert_one(result_dict)
            await ctx.reply(lang_str.success_submit(ctx.author.id))
    elif event.lower() == '3bld':
        if none_count >= 3:
            await ctx.reply(lang_str.submit_not_n(ctx.author.id, 3))
        else:
            attempts = [-1 if attempt.lower() == 'dnf' else -2 if attempt.lower() == 'dns' else float(attempt) for attempt in attempts[:3]]
            result = attempts
            result.sort()
            result = result[0]
            result_dict = {'user_id': ctx.author.id, 'event': event, 'a1': a1, 'a2': a2, 'a3': a3, 'a4': a4, 'a5': a5, 'result': result}
            RESULTS_TABLE.insert_one(result_dict)
            await ctx.reply(lang_str.success_submit(ctx.author.id))
    else:
        result = float(a1) if a1.lower() != 'dnf' else 0 if a1.lower() != 'dns' else -1
        result_dict = {'user_id': ctx.author.id, 'event': event, 'a1': a1, 'a2': a2, 'a3': a3, 'a4': a4, 'a5': a5, 'result': result}
        RESULTS_TABLE.insert_one(result_dict)
        await ctx.reply(lang_str.success_submit(ctx.author.id))

@client.command()
async def display(ctx, deldb=False, title='Weekly Contest'):
    await ctx.typing()
    if ctx.author.id not in ADMIN_DISCORD_ID:
        await ctx.author.send('Invalid user.')
        return await ctx.channel.purge(limit=1)
    else:
        print('Querying for data...')
        all_results = RESULTS_TABLE.find().sort([('event', pymongo.ASCENDING), ('result', pymongo.ASCENDING)])
        events_results = {}
        podium_results = {}
        for i in range(RESULTS_TABLE.count_documents({})):
            if i > 0:
                if all_results[i]['event'] != all_results[i - 1]['event']:
                    events_results[all_results[i]['event']] = [all_results[i]]
                else:
                    events_results[all_results[i]['event']].append(all_results[i])
            else:
                events_results[all_results[i]['event']] = [all_results[i]]
        for event in events_results:
            submitted_num = len(events_results[event])
            if submitted_num >= 3 :
                podium_results[event] = events_results[event][:3]
            else:
                podium_results[event] = events_results[event][:submitted_num]
        print('Done!')
        await ctx.channel.purge(limit=1)
        embed = discord.Embed(title=f'Results for {title}', url='https://discord.gg/JAAJsZY')
        for event in podium_results:
            ev = ''
            for indv in podium_results[event]:
                if indv['result'] <= 0:
                    continue
                if indv['result'] >= 60:
                    indv['result'] = SEC2MIN(indv['result'])
                ev += f'<@{indv["user_id"]}>\t({indv["result"]})\n'
            embed.add_field(name=EVENT_ID[event], value=ev)
        embed.set_footer(text='This system was made by kinpkt#2815 \nIf any rankings are incorrect, please contact kinpkt#2815.')
        await ctx.send(f'<@&1043103408011366450> **{title} results are here.**\n', embed=embed)
        if deldb:
            await ctx.author.send('Results are successfully resetted.')
            RESULTS_TABLE.delete_many({})

@client.command()
async def getwcif(ctx, comp_id):

    def check(msg):
        return msg.author == ctx.author

    await ctx.author.send('Please type in your WCA account e-mail below.')
    
    email_input = await client.wait_for('message', check=check)
    email = email_input.content

    await ctx.author.send('Please type in your WCA account password below (make sure to delete the message after finished).')

    pw_input = await client.wait_for('message', check=check)
    password = pw_input.content

    LOGIN_URL = 'https://www.worldcubeassociation.org/oauth/token'
    DATA = {
        'grant_type': 'password',
        'client_id': 'qWbPYiJZZzqOAFmcOxBacUR-7Mu2Gt2uMJumg6xvyNc',
        'client_secret': 'nNOS__iR-60Xikpa-4bFZjDZi0_5pPT-9VJKqCz2wRM',
        'username': email,
        'password': password,
        'scope': 'manage_competitions'
    }

    response = requests.post(LOGIN_URL, data=DATA)
    if response.status_code == 200:
        TOKEN = response.json()['access_token']
        TYPE = response.json()['token_type']
        WCIF_URL = f'https://www.worldcubeassociation.org/api/v0/competitions/{comp_id}/wcif'
        headers = {'Authorization': f'{TYPE} {TOKEN}'}
        wcif = requests.get(WCIF_URL, headers=headers)
        if wcif.status_code == 200:
            print(f'Downloading file for {comp_id}...')
            wcif_json = json.dumps(wcif.json(), indent=4, ensure_ascii=False)
            with open(f'{comp_id}.json', 'w', encoding='utf-8') as file:
                file.write(wcif_json)
            await client.send_file(ctx.message.channel, open(f'{comp_id}.json'))
            print('Downloaded successfully.')
            print('---------------------------------------------------------')
        else:
            print(wcif.status_code)
            print("Sorry, but you aren't the organizer / delegate of this competition.")
            print('Request failed with status code: ', response.status_code)
    else:
        print('Login failed with status code: ', response.status_code)

client.run(os.getenv('TOKEN'))