import os
import json
import discord
import requests
import scrambles
from iso3166 import countries
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from translate import Translator
from discord.ext import commands

load_dotenv()

bot_prefix = '-'

intents = discord.Intents.all()
intents.message_content = True

client = commands.Bot(command_prefix=bot_prefix, case_insensitive=True, help_command=None, intents=intents)

th_translate = Translator(to_lang='Thai')

@client.event
async def on_ready():
    #url = 'https://notify-api.line.me/api/notify'
    #headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer ' + os.getenv('LINE_TOKEN')}
    #requests.post(url, headers=headers, data={'message':'THC Bot is now online.'})
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
    commands_list = [
        {'cmd': 'คำสั่งทั่วไป', 'category': True},
        {'cmd': 'help', 'desc': 'คำสั่งบอกรายชื่อคำสั่งทั้งหมด'},
        {'cmd': 'prefix', 'desc': f'คำสั่งเปลี่ยนคำนำหน้าคำสั่ง (ตอนนี้ : {bot_prefix})'},
        {'cmd': 'คำสั่งข้อมูล WCA', 'category': True},
        {'cmd': 'whois [WCA ID]', 'desc': 'คำสั่งบอกรายละเอียดผู้เข้าแข่งขันตาม WCA ID'},
        {'cmd': 'wr [Event] [ประเภทเวลา]', 'desc': 'คำสั่งบอกรายละเอียดสถิติโลกแต่ละรายการ'},
        {'cmd': 'คำสั่งคำนวณเวลา', 'category': True},
        {'cmd': 'mo3 [เวลา 1] [เวลา 2] [เวลา 3]', 'desc': 'คำสั่งคำนวณเวลาแบบ Mo3'},
        {'cmd': 'ao5 [เวลา 1] [เวลา 2] [เวลา 3] [เวลา 4] [เวลา 5]', 'desc': 'คำสั่งคำนวณเวลาแบบ Ao5'},
        {'cmd': 'คำสั่งสร้างโจทย์', 'category': True},
        {'cmd': 'scr [ประเภท] [จำนวนโจทย์]', 'desc': 'คำสั่งสร้างโจทย์'}
    ]
    embed = discord.Embed(title='คำสั่งบอท')
    for cmd in commands_list:
        if 'category' in cmd:
            embed.add_field(name='** **', value='** **', inline=False)
            embed.add_field(name=cmd['cmd'], value='** **', inline=False)
            continue
        embed.add_field(name=f'{bot_prefix}{cmd["cmd"]}', value=cmd['desc'], inline=True)
    embed.set_footer(text='หมายเหตุ : ไม่ต้องใส่ [] เวลาใช้คำสั่ง')
    await ctx.reply(embed=embed)

@client.command()
async def prefix(ctx, new=None):
    global bot_prefix
    if new is None:
        return await ctx.reply(f'ขณะนี้ใช้ {bot_prefix} นำหน้าคำสั่งอยู่ครับ')
    await ctx.reply(f'ได้ทำการเปลี่ยนตัวนำหน้าคำสั่งจาก {bot_prefix} เป็น {new} แล้วครับ')
    bot_prefix = new
    client.command_prefix = new

''' @client.command()
async def events(ctx):
    embed = discord.Embed(title='กิจกรรมที่ผ่านมา', url='https://www.facebook.com/109079973767623/photos/a.110320336976920/679357656739849/', color=discord.Color.blurple())
    embed.add_field(name='กิจกรรม workshop รูบิกศาสตร์', value='กิจกรรมสอนการแก้โจทย์รูบิก', inline=False)
    embed.add_field(name='วันที่จัดกิจกรรม', value='2 เมษายน 2565', inline=True)
    embed.add_field(name='สถานที่', value='สามย่าน โค-ออป', inline=True)
    await ctx.send(embed=embed) '''

@client.command()
async def whois(ctx, wcaid = None):
    await ctx.typing()
    if wcaid is None:
        return await ctx.reply('กรุณาใส่ WCA ID ด้วยครับ')
    else:
        link = requests.get(f'https://www.worldcubeassociation.org/persons/{wcaid.upper()}').text
        bs = BeautifulSoup(link, 'lxml')
        name = bs.find('h2').text
        pfp = bs.find('img', class_='avatar')['src']
        country_name = bs.find('td', class_='country')
        country = th_translate.translate(country_name.text)
        comp_num = bs.find_all('td')[3].text
        have_medal = bs.find('div', class_='medal-collection')
        have_badge = bs.find_all('span', class_='badge')
        embed = discord.Embed(title=name, url=f'https://www.worldcubeassociation.org/persons/{wcaid.upper()}')
        embed.set_image(url=pfp)
        embed.add_field(name='สัญชาติ', value=country, inline=True)
        if have_badge != []:
            position = []
            for badge in have_badge:
                position.append(badge.a.text)
            embed.add_field(name='ตำแหน่ง', value=', '.join(position), inline=True)
        embed.add_field(name='จำนวนการแข่งขัน', value=comp_num, inline=True)
        if have_medal is not None:
            gold_num = bs.find_all('a', class_='highlight-medal')[0].text
            silver_num = bs.find_all('a', class_='highlight-medal')[1].text
            bronze_num = bs.find_all('a', class_='highlight-medal')[2].text
            embed.add_field(name='** **', value='** **', inline=False)
            embed.add_field(name='จำนวนเหรียญทอง', value=gold_num, inline=True)
            embed.add_field(name='จำนวนเหรียญเงิน', value=silver_num, inline=True)
            embed.add_field(name='จำนวนเหรียญทองแดง', value=bronze_num, inline=True)
        embed.set_footer(text='ข้อมูลเมื่อวันที่ 15 เมษายน 2565')
        await ctx.reply(embed=embed)

@client.command()
async def wr(ctx, event = None, time = None):
    event_keys = {'3x3x3 Cube': '333', '2x2x2 Cube': '222', '4x4x4 Cube': '444', '5x5x5 Cube': '555', '6x6x6 Cube': '666', '7x7x7 Cube': '777', '3x3x3 Blindfolded': '3bld', '3x3x3 Fewest Moves': 'fmc', '3x3x3 One-Handed': 'oh', 'Clock': 'clock', 'Megaminx': 'mega', 'Pyraminx': 'pyra', 'Skewb': 'skewb', 'Square-1': 'sq1', '4x4x4 Blindfolded': '4bld', '5x5x5 Blindfolded': '5bld', '3x3x3 Multi-Blind': 'mbld'}
    inv_event_keys = {val: key for key, val in event_keys.items()}
    time_list = ['single', 'average', 'avg']
    if event is None or time is None or event.lower() not in inv_event_keys or time.lower() not in time_list or event.lower() == 'mbld' and time.lower() == 'avg':
        times = [
            {'format': 'Single', 'events': 'ทุกรายการ'},
            {'format': 'Average / AVG', 'events': 'เกือบทุกรายการยกเว้น 3x3x3 ปิดตาหลายลูก'},
        ]
        embed = discord.Embed(title='รายชื่อรายการและประเภทเวลา', url='https://www.worldcubeassociation.org/results/records')
        embed.add_field(name='รายการแข่งขันทั้งหมด', value='** **', inline=False)
        dict_key = list(event_keys.keys())
        dict_value = list(event_keys.values())
        for i in range(len(event_keys)):
            embed.add_field(name=dict_key[i], value=dict_value[i], inline=True)
        embed.add_field(name='ประเภทเวลาทั้งหมด', value='** **', inline=False)
        for time in times:
            embed.add_field(name=time['format'], value=time['events'], inline=True)
        return await ctx.reply(embed=embed)
    link = requests.get('https://www.worldcubeassociation.org/results/records').text
    bs = BeautifulSoup(link, 'lxml')
    wr_name = bs.find_all('td', class_='name')
    wr_time = bs.find_all('td', class_='result')
    wr_country = bs.find_all('td', class_='country')
    wr_comp = bs.find_all('td', class_='competition')
    wr_data = [wr_name, wr_time, wr_country, wr_comp]
    wr_title = ['ชื่อผู้เข้าแข่งขัน', 'เวลาที่ได้', 'สัญชาติ', 'ชื่อการแข่งขัน']
    event_index = {'333': 0, '222': 2, '444': 4, '555': 6, '666': 8, '777': 10, '3bld': 12, 'fmc': 14, 'oh': 16, 'clock': 18, 'mega': 20, 'pyra': 22, 'skewb': 24, 'sq1': 26, '4bld': 28, '5bld': 30, 'mbld': 32}
    all_index = event_index[event.lower()] + (0 if time.lower() == 'single' else 1)
    special_id = {'3bld': '333bf', 'fmc': '333fm', 'oh': '333oh', 'mega': 'minx', 'pyra': 'pyram', '4bld': '444bf', '5bld': '555bf', 'mbld': '333mbf'}
    event_id = event.lower() if event.lower() not in special_id else special_id[event.lower()]
    embed = discord.Embed(title=f'สถิติโลกรายการ {inv_event_keys[event]} ประเภท {"Single" if time.lower() == "single" else "Average"}', url=f'https://www.worldcubeassociation.org/results/records?event_id={event_id}')
    for i in range(len(wr_data)):
        if i == 0:
            link = requests.get(f"https://www.worldcubeassociation.org/{wr_data[i][all_index].a['href']}").text
            bs2 = BeautifulSoup(link, 'lxml')
            pfp = bs2.find('img', class_='avatar')['src']
            embed.set_image(url=pfp)
        elif i == 2:
            country = wr_data[i][all_index].text
            th_country = th_translate.translate(country)
            embed.add_field(name='สัญชาติ', value=th_country)
            continue
        embed.add_field(name=wr_title[i], value=wr_data[i][all_index].text)
    await ctx.reply(embed=embed)

@client.command()
async def cr(ctx, continent = None, event = None, time = None):
    await ctx.typing()
    event_keys = {'3x3x3 Cube': '333', '2x2x2 Cube': '222', '4x4x4 Cube': '444', '5x5x5 Cube': '555', '6x6x6 Cube': '666', '7x7x7 Cube': '777', '3x3x3 Blindfolded': '3bld', '3x3x3 Fewest Moves': 'fmc', '3x3x3 One-Handed': 'oh', 'Clock': 'clock', 'Megaminx': 'mega', 'Pyraminx': 'pyra', 'Skewb': 'skewb', 'Square-1': 'sq1', '4x4x4 Blindfolded': '4bld', '5x5x5 Blindfolded': '5bld', '3x3x3 Multi-Blind': 'mbld'}
    inv_event_keys = {val: key for key, val in event_keys.items()}
    continent_keys = {'af': 'Africa', 'as': 'Asia', 'eu': 'Europe', 'na': 'North America', 'oc': 'Oceania', 'sa': 'South America'}
    inv_continent_keys = {val: key for key, val in continent_keys.items()}
    time_list = ['single', 'average', 'avg']
    if continent is None or event is None or time is None or continent not in continent_keys or event not in inv_event_keys or time not in time_list:
        times = [
            {'format': 'Single', 'events': 'ทุกรายการ'},
            {'format': 'Average / AVG', 'events': 'เกือบทุกรายการยกเว้น 3x3x3 ปิดตาหลายลูก'},
        ]
        embed = discord.Embed(title='รายชื่อทวีป, รายการและประเภทเวลา', url='https://www.worldcubeassociation.org/results/records')
        embed.add_field(name='รายชื่อทวีปทั้งหมด', value='** **', inline=False)
        ct_dict_key = list(inv_continent_keys.keys())
        ct_dict_value = list(inv_continent_keys.keys())
        for i in range(len(continent_keys)):
            embed.add_field(name=ct_dict_key[i], value=ct_dict_value[i], inline=True)
        embed.add_field(name='รายการแข่งขันทั้งหมด', value='** **', inline=False)
        ev_dict_key = list(event_keys.keys())
        ev_dict_value = list(event_keys.values())
        for i in range(len(event_keys)):
            embed.add_field(name=ev_dict_key[i], value=ev_dict_value[i], inline=True)
        embed.add_field(name='ประเภทเวลาทั้งหมด', value='** **', inline=False)
        for time in times:
            embed.add_field(name=time['format'], value=time['events'], inline=True)
        return await ctx.reply(embed=embed)
    link = requests.get(f'https://www.worldcubeassociation.org/results/records?=_{continent_keys[continent.lower()]}').text
    bs = BeautifulSoup(link, 'lxml')
    cr_name = bs.find_all('td', class_='name')
    cr_time = bs.find_all('td', class_='result')
    cr_country = bs.find_all('td', class_='country')
    cr_comp = bs.find_all('td', class_='competition')
    cr_data = [cr_name, cr_time, cr_country, cr_comp]
    cr_title = ['ชื่อผู้เข้าแข่งขัน', 'เวลาที่ได้', 'สัญชาติ', 'ชื่อการแข่งขัน']
    event_index = {'333': 0, '222': 2, '444': 4, '555': 6, '666': 8, '777': 10, '3bld': 12, 'fmc': 14, 'oh': 16, 'clock': 18, 'mega': 20, 'pyra': 22, 'skewb': 24, 'sq1': 26, '4bld': 28, '5bld': 30, 'mbld': 32}
    all_index = event_index[event.lower()] + (0 if time.lower() == 'single' else 1)
    special_id = {'3bld': '333bf', 'fmc': '333fm', 'oh': '333oh', 'mega': 'minx', 'pyra': 'pyram', '4bld': '444bf', '5bld': '555bf', 'mbld': '333mbf'}
    event_id = event.lower() if event.lower() not in special_id else special_id[event.lower()]
    embed = discord.Embed(title=f'สถิติทวีป{th_translate.translate(continent_keys[continent.lower()])}รายการ {inv_event_keys[event]} ประเภท {"Single" if time.lower() == "single" else "Average"}', url=f'https://www.worldcubeassociation.org/results/records?event_id={event_id}&region=_{continent_keys[continent.lower()]}')
    for i in range(len(cr_data)):
        if i == 0:
            link = requests.get(f"https://www.worldcubeassociation.org/{cr_data[i][all_index].a['href']}").text
            bs2 = BeautifulSoup(link, 'lxml')
            pfp = bs2.find('img', class_='avatar')['src']
            embed.set_image(url=pfp)
        elif i == 2:
            country = cr_data[i][all_index].text
            th_country = th_translate.translate(country)
            embed.add_field(name='สัญชาติ', value=th_country)
            continue
        embed.add_field(name=cr_title[i], value=cr_data[i][all_index].text)
    await ctx.reply(embed=embed)

@client.command()
async def mo3(ctx, a1 = None, a2 = None, a3 = None):
    attempts = [a1, a2, a3]
    if None in attempts:
        return await ctx.reply('กรุณาใส่เวลาให้ครบ 3 ครั้งครับ')
    attempts = [i.lower() for i in attempts]
    if 'dnf' in attempts or 'dns' in attempts:
        result = 'DNF'
    else:
        attempts = [float(i) for i in attempts]
        result = sum(attempts) / len(attempts)
        result = f'{result:.2f}'
    await ctx.reply(f'เวลา Mo3 ของ {a1}, {a2} และ {a3} คือ {result}')

@client.command()
async def ao5(ctx, a1 = None, a2 = None, a3 = None, a4 = None, a5 = None):
    attempts = [a1, a2, a3, a4, a5]
    dnf_count = 0
    if None in attempts:
        return await ctx.reply('กรุณาใส่เวลาให้ครบ 5 ครั้งครับ')
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
    await ctx.reply(f'เวลา Ao5 ของ {a1}, {a2}, {a3}, {a4} และ {a5} คือ {result}')

@client.command()
async def generate(ctx, event, attempts):
    scr = scrambles.gen(event, attempts)
    for i in range(len(scr)):
        await ctx.send(scr[i])

client.run(os.getenv('TOKEN'))