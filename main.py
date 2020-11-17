import discord
from discord.ext import commands
import asyncio

#++++++++++++++++++++CUSTOM METHODS++++++++++++
def convert(string):
  if string[len(string)-1] == "D":
    string = string[:-1]
    return int(string) * 1440
  elif string[len(string)-1] == "H":
    string = string[:-1]
    return int(string) * 60
  else:
    return 15
#+++++++++++++++++++++++++++++++++++++++++++++++


client = commands.Bot(command_prefix="sudo ")
token = "Nzc1MzMyNDQ4NjI3NzIwMjMy.X6kynA.CFT9hzBShYnmsTpU_I916D3m_2o"#super secret

main_role = "Everyone" #change to verified.

@client.event
async def on_ready():
  print("[*] Terminator Status : SkyNet Activated.")

@client.command()
async def hello(ctx):
  await ctx.send("Sup")

@client.command()
async def kick(ctx, member : discord.Member, reason=None):
  await member.kick(reason = reason)
  await ctx.send(f"Kicked {member} for {reason}")

@client.command()
async def ban(ctx, member:discord.Member, reason=None):
  await member.ban(reason = reason)
  await ctx.send(f"Banned {member} for {reason}")

@client.command()
async def unban(ctx,*, member):
  banned_users = await ctx.guild.bans()
  member = member.split("#")
  member_name = member[0]
  member_discriminator = member[1]
  for ban_entry in banned_users:
    user = ban_entry.user
    if (user.name, user.discriminator) == (member_name, member_discriminator):
      await ctx.guild.unban(user)
      await ctx.send(f"Unbanned {member_name}")

@client.command()
async def mute(ctx, member: discord.Member, time_, reason):
  time_ = convert(time_)
  print(f"Muting..{member.name}")
  try:
    for role in member.guild.roles:
      if role.name == main_role:
        await member.remove_roles(role)
        await ctx.send(f"Muted {member} for {reason} for {time_} minutes")

        if time_ > 0:
          await asyncio.sleep(time_ * 60)

          await member.add_roles(role)
          await ctx.send(f"Unmuted {member}")
      
  except:
    await ctx.send("An Error Occured  :(")

  return


@client.command()
async def unmute(ctx, member: discord.Member):
  for role in member.guild.roles:
    if role.name == main_role:
      await member.add_roles(role)
      await ctx.send(f"Unmuted {member}")


client.run(token) 
# TODO : ADD mute command, I'm gonna test the mute command

