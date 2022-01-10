import discord
import nekos
import json
from datetime import datetime
from discord.ext import tasks, commands
from discord.utils import get
import random

# get token from file

f = open("token", "r")
token = f.read()
f.close()

client = commands.Bot(command_prefix=",")


# https://stackoverflow.com/a/3540315

def timestamp():
    today = datetime.now()
    print(today)

def random_line(afile):
    line = next(afile)
    for num, aline in enumerate(afile, 2):
        if random.randrange(num):
            continue
        line = aline
    return line

def randomQuote():
    file = open("quotes", "r")
    quote = random_line(file)
    file.close()
    return '"' + quote + '" - Jan Paweł II'

nword = {}
f = open('nword.json')
nwordCounter = json.load(f)
f.close()

@client.event
async def on_ready():
    timestamp()
    print("We've logged in as {0.user}".format(client))
    game = discord.Game("Linux > Windows")
    await client.change_presence(status=discord.Status.idle, activity=game)

# don't touch it works
@client.event
async def on_message(message):
    text = message.content.lower()
    if 'nigger' in text.split():
        f = open('nword.json')
        nwordCounter = json.load(f)
        try:
            currentCounter = nwordCounter[str(message.author.id)]['counter']
            num = int(currentCounter)
        except:
            num = 0
        num += 1
        nword[str(message.author.id)] = {'counter': str(num)}
        with open('nword.json', 'w') as f:
            json.dump(nword, f)
        f.close()
    else:
        await client.process_commands(message)

# dwudziesta pierwsza dwadzieścia siedem
async def djts():
    guildID = 871450821936693348
    channelID = 871450821936693350
    guild = client.get_guild(guildID)
    embed = discord.Embed(title=randomQuote())
    embed.set_author(name="Adam Corp")
    embed.set_image(url="https://a.allegroimg.com/s1024/0cfcd2/89fdbb4644eeb8eecb07dada22c3")
    await guild.get_channel(channelID).send(embed=embed)


@tasks.loop(minutes=1)
async def papiezowa():
    print("Odliczanie do papiezowej trwa")
    tragetH = 21
    targetM = 37
    currentTime = datetime.now()
    await client.wait_until_ready()
    if currentTime.hour == tragetH and currentTime.minute == targetM:
        await djts()
    else:
        print('Minuta blizej do papiezowej')


papiezowa.start()

# Moderacja

@client.command(name = "ban")
async def ban(ctx):
    if ctx.message.author.guild_permissions.administrator:
      if ctx.message.mentions:
        await ctx.message.mentions[0].ban()
        await ctx.message.channel.send('Użytkownik został zbanowany')
      else:
        await ctx.message.channel.send('Nie wybrano użytkownika')
    else:
      await ctx.message.channel.send('Nie masz uprawnień by wykonać tą komendę')

@client.command(name = "kick")
async def kick(ctx):
    if ctx.message.author.guild_permissions.administrator:
      if ctx.message.mentions:
        await ctx.message.mentions[0].kick()
        await ctx.message.channel.send('Użytkownik został wyrzucony z serwera')
      else:
        await ctx.message.channel.send('Nie wybrano użytkownika')
    else:
      await ctx.message.channel.send('Nie masz uprawnień by wykonać tą komendę')

@client.command(name="mute")
async def mute(ctx):
    if ctx.message.author.guild_permissions.administrator:
        if get(ctx.guild.roles, name="muted"):
            print("Role exists!")
        else:
            await ctx.guild.create_role(name="muted", colour=discord.Colour(0xffffff))
            perms = discord.Permissions(send_messages=False)
            await get(ctx.guild.roles, name="muted").edit(permissions=perms)
        if ctx.message.mentions:
            muteRole = get(ctx.guild.roles, name="muted")
            await ctx.message.mentions[0].add_roles(muteRole)
            await ctx.message.channel.send('Wyciszono użytkownika')
        else:
            await ctx.message.channel.send("Nie oznaczono żadnego użytkownika")
    else:
        await ctx.message.channel.send("Nie posiadasz wymaganych uprawnień")


@client.command(name="unmute")
async def unmute(ctx):
    if ctx.message.author.guild_permissions.administrator:
        if ctx.message.mentions:
            muteRole = get(ctx.guild.roles, name="muted")
            await ctx.message.mentions[0].remove_roles(muteRole)
            await ctx.message.channel.send('Zakończono wyciszenie użytkownika')
        else:
            await ctx.message.channel.send("Nie oznaczono żadnego użytkownika")
    else:
        await ctx.message.channel.send("Nie posiadasz wymaganych uprawnień")

@client.command(name="purge")
async def purge(ctx, arg: int):
    if ctx.message.author.guild_permissions.administrator:
        await ctx.channel.purge(limit=arg + 1)
    else:
        await ctx.channel.send('Nie posiadasz uprawnień')

# Narzędzia
@client.command(name="avatar")
async def avatar(ctx):
    if ctx.message.mentions:
        user = ctx.message.mentions[0]

        embed = discord.Embed(title="avatar:")
        embed.set_author(name=user)
        embed.set_image(url=user.avatar_url)

        await ctx.message.channel.send(embed=embed)
    else:
        user = ctx.message.author

        embed = discord.Embed(title="Your avatar:")
        embed.set_author(name=user)
        embed.set_image(url=user.avatar_url)

        await ctx.message.channel.send(embed=embed)

@client.command(name="counter")
async def counter(ctx):
    if ctx.message.mentions:
        f = open('nword.json')
        nword = json.load(f)
        f.close()
        userID = str(ctx.message.mentions[0].id)
        user = ctx.message.mentions[0].name
        counter = nword[userID]['counter']
        await ctx.message.channel.send(user + " napisał nworda " + str(counter) + " razy")
    else:
        await ctx.message.channel.send("Nie oznaczono użytkownika")

# Fun

@client.command(name="cytat")
async def cytat(ctx):
    await ctx.message.channel.send(randomQuote())

@client.command(name="neko")
async def neko(ctx):
    await ctx.message.channel.send(nekos.img("neko"))


@client.command(name="cycki")
async def cycki(ctx):
    if ctx.message.channel.is_nsfw():
        await ctx.message.channel.send(nekos.img("boobs"))
    else:
        await ctx.message.channel.send("Aby użyć tej komendy kanał musi być oznaczony jako NSFW")

@client.command(name="pusia")
async def cycki(ctx):
    if ctx.message.channel.is_nsfw():
        await ctx.message.channel.send(nekos.img("pussy"))
    else:
        await ctx.message.channel.send("Aby użyć tej komendy kanał musi być oznaczony jako NSFW")

@client.command(name="test")
async def test(ctx):
    await ctx.message.channel.send("test")
    
client.run(token)
