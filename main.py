import discord
from discord.ext import tasks, commands
from discord.utils import get
import random

#get token from file
f = open("token", "r")
token = f.read()
f.close()

client = discord.Client()
client = commands.Bot(command_prefix = ",")

#https://stackoverflow.com/a/3540315
def random_line(afile):
    line = next(afile)
    for num, aline in enumerate(afile, 2):
        if random.randrange(num):
            continue
        line = aline
    return line

@client.event
async def on_ready():
    print("We've logged in as {0.user}".format(client))

@client.command(name = "mute")
async def mute(ctx):
    if ctx.message.author.guild_permissions.administrator:
        if get(ctx.guild.roles, name="muted"):
            print("Role exists!")
        else:
            await ctx.guild.create_role(name="muted", colour=discord.Colour(0xffffff))
            perms = discord.Permissions(send_messages=False)
            await get(ctx.guild.roles, name="muted").edit(permissions = perms)
        if ctx.message.mentions:
            muteRole = get(ctx.guild.roles, name="muted")
            await ctx.message.mentions[0].add_roles(muteRole)
            await ctx.message.channel.send('Wyciszono użytkownika')
        else:
            await ctx.message.channel.send("Nie oznaczono żadnego użytkownika")
    else:
        await ctx.message.channel.send("Nie posiadasz wymaganych uprawnień")

@client.command(name = "unmute")
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

@client.command(name = "avatar")
async def avatar(ctx):
    if ctx.message.mentions:
      user = ctx.message.mentions[0]

      embed = discord.Embed(title = "avatar:")
      embed.set_author(name = user)
      embed.set_image(url = user.avatar_url)
@client.command(name = "cytat")
async def cytat(ctx):
    file = open("quotes", "r")
    quote = random_line(file)
    file.close()
    await ctx.message.channel.send('"' + quote + '" - Jan Paweł II')

client.run(token)
