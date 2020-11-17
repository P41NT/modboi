import discord
from discord.ext import commands

client = commands.Bot(command_prefix="sudo ")
##hello..

@client.event
async def on_ready():
    print("[*] Terminator Status : SkyNet Activated.")

@client.command()
async def wyd(ctx):
    await ctx.send("Terminating...")

@client.command()
async def stfu(ctx):
    await ctx.send("No you stfu.")

@client.command()
async def stop(ctx):
    await ctx.send("there is no stopping now hehe")

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
    print(f"Muting..{member.name}")
    if "Muted" in member.guild.roles:
      for role in member.guild.roles:
          print(role.name)
          if role.name == "Muted":
              await member.add_roles(role)
              await ctx.send(f"Muted {member} for {reason} for {time}")
              return
    else:
      overwrite = discord.PermissionOverwrite(send_messages=False)
      guild = ctx.guild
      newRole = await guild.create_role(name="Muted")

      for channel in member.guild.text_channels:
          await channel.set_permissions(newRole, overwrite = overwrite)
      
      await member.add_roles(newRole)
      await ctx.send(f"Muted {member} for {reason} for {time}")
    
@client.command()
async def unmute(ctx, member: discord.Member, *, time=None, reason=None):
    for role in member.guild.roles:
        if role.name == "Muted":
            await member.remove_roles(role)
            await ctx.send(f"Unmuted {member}")

client.run("Nzc1MzMyNDQ4NjI3NzIwMjMy.X6kynA.CFT9hzBShYnmsTpU_I916D3m_2o")