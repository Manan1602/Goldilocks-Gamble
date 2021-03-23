import discord
import random
import os
from discord.ext import commands
import pandas as pd

intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
client = commands.Bot(command_prefix = '.', intents = intents)

def convert(lst):
    res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
    return res_dct


def buy_resource(id,resource):
    df=pd.read_csv('data.csv')
    cred=0
    amount=0
    era=int(df.loc[df['id']==id,'era'])
    with open('resources.csv') as resource_file:
        for row in resource_file:
            if row.split(sep=',')[0]==resource:
                cred=row.split(sep=',')[era+1]
                print(cred)
                amount=row.split(sep=',')[1]
                print(amount)
    
    print("out of the loop")
    df.loc[df['id']==id,'credits']=float(df.loc[df['id']==id,'credits'])-float(df.loc[df['id']==id,'multiplier'])*cred
    df.loc[df['id']==id,str(resource)]=float(df.loc[df['id']==id,str(resource)])+amount
    df.to_csv('data.csv')
    print(df)           

                

@client.event
async def on_member_join(member):
    print(f"{member} has joined the server.")

@client.event
async def on_member_remove(member):
    print(f"{member} has left the server.")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command doesn't exist")

@client.command()
async def buy(ctx, resource):
    team=ctx.channel.id
    print(team,resource)
    buy_resource(team,resource)

@client.command()
async def start(ctx):
    with open('./start_message.txt', 'r') as start_message:
        embed = discord.Embed(color=discord.Colour.red(), description='r[A]men')
        embed.set_thumbnail(url=ctx.author.avatar_url)
        ct=0
        for line in start_message:
            ct=ct+1
            embed.add_field(name=str(ct), value=line, inline=False)
        await ctx.send(embed=embed)

@client.command()
async def stats(ctx):
    print(ctx.channel.id)
    df=pd.read_csv('data.csv')
    print(df)
    await ctx.send(df)


@client.command(aliases=['8ball'])
async def _8ball(ctx, *, question):
    responses = ["It is certain.",
                "It is decidedly so.",
                "Without a doubt.",
                "Yes - definitely.",
                "You may rely on it.",
                "As I see it, yes.",
                "Most likely.",
                "Outlook good.",
                "Yes.",
                "Signs point to yes.",
                "Reply hazy, try again.",
                "Ask again later.",
                "Better not tell you now.",
                "Cannot predict now.",
                "Concentrate and ask again.",
                "Don't count on it.",
                "My reply is no.",
                "My sources say no.",
                "Outlook not so good.",
                "Very doubtful."]
    await ctx.send(f"Question : {question}\nAnswer : {random.choice(responses)}")

@client.command()
@commands.has_permissions(manage_messages = True)
async def clear(clx, amount = 10):
    await clx.channel.purge(limit=amount)

def is_it_me(ctx):
    return ctx.author.id == 823258998769582130

@client.command()
@commands.check(is_it_me)
async def hi(ctx):
    await ctx.send(f"Hi i am {ctx.author}")

@client.command()
async def kick(ctx, member : discord.Member, *, reason = None):
    await member.kick(reason=reason)
    await ctx.send(f"Kicked {member.mention}")

@client.command()
async def ban(ctx, member : discord.Member, *, reason = None):
    await member.ban(reason=reason)
    await ctx.send(f"Banned {member.mention}")

@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if(user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"Unbanned {user.mention}")
            return

@client.command()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")

@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")

@client.command()
async def reload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")

for filename in os.listdir('./cogs'):
    if filename.endswith(".py"):
        client.load_extension(f"cogs.{filename[:-3]}")


client.run('ODIyMTg4NzU2ODUzMDYzNzAw.YFOo8w.F1zaakiq7BnZWXJOlLp50RdL1qE')