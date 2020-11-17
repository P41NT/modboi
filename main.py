import discord
from discord.ext import commands

client = commands.Bot(command_prefix="sudo ")

@client.event
async def on_ready():
    print("[*] Terminator Status : SkyNet Activated.")

@client.command()
async def hello(ctx):
    await ctx.send("sup")

@client.command()
async def kick(ctx, member : discord.Member, *, reason=None):
    await member.kick(reason = reason)
    await ctx.send(f"Kicked {member} for {reason}")

@client.command()
async def ban(ctx, member:discord.Member, *, reason=None):
    await member.ban(reason = reason)
    await ctx.send(f"Banned {member} for {reason}")

@client.command()
async def mute(ctx, member: discord.Member, *, time=None, reason=None):
    for role in guild.roles():
        if role.name == "Muted":
            await member.add_role(role)
            await ctx.send(f"Muted {member} for {reason} for {time}")
            return

            overwrite = discord.PermissionOverwrite(send_messages=False)
            newRole = await guild.createRole("Muted")

            for channel in guild.text_channels:
                await channel.set_permissions(newRole, overwrite = overwrite)
            
            await member.add_role(newRole)
            await ctx.send(f"Muted {member} for {reason}")
    
@client.command()
async def unmute(ctx, member: discord.Member, *, time=None, reason=None):
    for role in guild.roles():
        if role.name == "Muted":
            await member.remove_role(role)
            await ctx.send(f"Unmuted {member}")

client.run("Nzc1MzMyNDQ4NjI3NzIwMjMy.X6kynA.ox9IstqIwpzo7Y1nSHFA8xLBOUQ")