import discord
import asyncio
import time
import random
import requests
from bs4 import BeautifulSoup
import youtube_dl


client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name="with Pokar's Nuts"))

@client.event
async def on_member_join(member):
    for r in roles:
        if r.name == 'Citizen':
            await client.add_roles(message.author, r)
            await client.send_message(message.channel, '```' + 'Role ' + 'Citizen' + ' has been added to your role list```')

@client.event
async def on_message(message):
    words = message.content.split('-')
    roles = message.server.roles
    if words[0] == '.buy':
        item = words[1]
        for word in words[2:]:
            item =  item + '+' + word
        url = 'https://www.flipkart.com/search?q=' + item
        sourceCode = requests.get(url)
        text = sourceCode.text
        soup = BeautifulSoup(text, features = "html.parser")
        links = []
        hrefs = []
        for link in soup.findAll('a', {'class': '_2cLu-l'}): 
            href = 'https://www.flipkart.com' + str(link.get('href'))
            links.append(link)
            hrefs.append(href)
        for link in soup.findAll('a', {'class': '_3wU53n'}):
            href = 'https://www.flipkart.com' + str(link.get('href'))
            links.append(link)
            hrefs.append(href)
        for r in range(0,5):
             await client.send_message(message.channel, hrefs[r] + '\n' + links[r].string)  
    if words[0] == '.play':
        song = words[1]
        for word in words[2:]:
            song =  song + '+' + word
        for channel in client.get_all_channels():
            if channel.name == message.author.voice.voice_channel.name:
                voice = await client.join_voice_channel(channel)
                print(song)
                url = 'https://www.youtube.com/results?search_query=' + song
                sourceCode = requests.get(url)
                text = sourceCode.text
                soup = BeautifulSoup(text, features = "html.parser")
                href = ''
                for link in soup.findAll('a'):
                    if 'watch' in  link.get('href'):
                        href = 'http://www.youtube.com/' + str(link.get('href'))
                        await client.send_message(message.channel, href)
                        break
                player = await voice.create_ytdl_player(href)
                player.start()
    
    if message.content == '.hello':
        rand = random.randint(1,5)
        if rand == 1:
            await client.send_message(message.channel, '```' + 'I have a riddle for you.' + '```')
            time.sleep(2)
            await client.send_message(message.channel, '```' + 'A tree which is planted on Monday and doubles in size each day is fully grown on the following Sunday. On what day is it half grown?' + '```')
            reply = await client.wait_for_message(author = message.author, timeout = 10)
            if reply.content == 'Saturday':
                await client.send_message(message.channel, '```Correct. You can go now.```')
            else:
                await client.send_message(message.channel, '```You big folk really are not the quickest```')
        if rand == 2:
            await client.send_message(message.channel,'```Hello, would you like a worm?```')
            reply = await client.wait_for_message(author = message.author, timeout = 10)
            if reply.content in ['Yes','Ok','yes','ok']:
                await client.send_message(message.channel,'```*The Gnome gives you a worm.*```')
                await client.send_message(message.channel,'```In the gnome village those who are needy receive what they need, and those who are able give what they can.```')
            else:
                await client.send_message(message.channel,'```Sometimes we do not realise what we need until the moment we have it```')
        if rand == 3:
            await client.send_message(message.channel, '```My mum says: A friendly look, a kindly smile one good act, and life is worthwhile!```')
        if rand == 4:
            await client.send_message(message.channel, '```A little inaccuracy sometimes saves tons of explanation!```')
        if rand == 5:
            await client.send_message(message.channel, '```Top of the morning to you...```')
            await client.wait_for_message(author = message.author, timeout = 10)
            await client.send_message(message.channel, '```...And bottom of the afternoon.```')   

    if message.content == '.help':
        await client.send_message(message.channel, '```' + 'You want something to happen? I want something to happen. Try saying .hello\nset-[Usermame]-[Nickname]\niam-[Role]\niamnot-[Role]\n[Member]-is-[Role]\n[Member]-isnot-[Role]\nNooneis-[Role]\n.clear - Clean chat\n' + '```')
    if message.channel.name == 'spoilers':
        time.sleep(5)
        await client.delete_message(message)
    if words[0] == '.clear':
        await client.send_message(message.channel, '```Clearing Chatlog```')
        time.sleep(2)
        messages = []
        async for m in client.logs_from(message.channel, limit=int(words[1])+2):
            messages.append(m)
        await client.delete_messages(messages)
    if words[0] == 'set' or words[0] == 'Set':
        await client.change_nickname(message.server.get_member_named(words[1]), words[2])
        await client.send_message(message.channel, '```' + 'Nickname for ' + words[1] + ' changed to ' + words[2] + '```')
    if words[0] == 'kick' or words[0] == 'Kick':
        await client.kick(message.server.get_member_named(words[1]))
        await client.send_message(message.channel, '```Kicking ' + words[1] + ' from the server..```')
    if words[0] == 'iam' or words[0] == 'Iam':
        found = 0     
        for r in roles:
            if r.name == words[1]:
                await client.add_roles(message.author, r)
                await client.send_message(message.channel, '```' + 'Role ' + words[1] + ' has been added to your role list```')
                found = 1
        if found == 0:
            kwargs = {'name': words[1], 'hoist': 1, 'mentionable': 1}
            NewRole = await client.create_role(message.server, **kwargs)
            await client.add_roles(message.author, NewRole)
            await client.send_message(message.channel, '```' + 'Role ' + words[1] + ' has been added to your role list```')
    if words[0] == 'iamnot' or words[0] == 'Iamnot':
        for r in roles:    
            if r.name == words[1]:    
                await client.remove_roles(message.author, r)
                await client.send_message(message.channel, '```' + 'Role ' + words[1] + ' has been removed from your role list```')
    if words[1] == 'is':
        found = 0
        for r in roles:       
            if r.name == words[2]:    
                await client.add_roles(message.server.get_member_named(words[0]), r)
                await client.send_message(message.channel, '```' + 'Role ' + words[2] + ' has been added to ' + message.server.get_member_named(words[0]).name + "'s role list```")
                found = 1
        if found == 0:
            kwargs = {'name': words[2], 'hoist': 1, 'mentionable': 1}
            NewRole = await client.create_role(message.server, **kwargs)
            await client.add_roles(message.server.get_member_named(words[0]), NewRole)
            await client.send_message(message.channel, '```' + 'Role ' + words[2] + ' has been added to ' + message.server.get_member_named(words[0]).name + "'s role list```")
                
    if words[1] == 'isnot':
        for r in roles:
            if r.name == words[2]:        
                await client.remove_roles(message.server.get_member_named(words[0]), r)
                await client.send_message(message.channel, '```' + 'Role ' + words[2] + ' has been removed from ' + message.server.get_member_named(words[0]).name + "'s role list```")
    if words[0] == 'nooneis' or words[0] == 'Nooneis' and words[1] != 'Citizen':
        for r in roles:
            if r.name == words[1]:
                await client.delete_role(message.server, r)
                await client.send_message(message.channel, '```' + 'Role ' + words[1] + ' has been removed from existence```') 


        
      
  


client.run('', bot=True)