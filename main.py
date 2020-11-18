import discord
from discord.ext import commands
import asyncio
from discord.ext.commands import has_permissions

#++++++++++++++++++++PARAMETERS+++++++++++++++++
token = "token...supe sercret, i wont share hehe"
command_prefix = "sudo "
main_role = "Everyone" #change to verified.
announcement_ping = "Oppressors"
badwords = ["nidda", "porn", "gay" ,"sex" , "motherfucker", "motherfuckers", "fucker", "fucking", "bitch", "nigga", "dick", "pussy", "fuck","nigger"]
admin_id = 713735322399277087
admin2 = 489092730253737986
dm = True
#+++++++++++++++++++++++++++++++++++++++++++++++

#++++++++++++++++++++++INITIALIZE++++++++++++++++
client = commands.Bot(command_prefix=command_prefix)

@client.event
async def on_ready():
  print("[*] Terminator Status : SkyNet Activated.")

#+++++++++++++++++++++++++++++++++++++++++++++++

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

async def send_dm(message):
  try:
    user = client.get_user(admin_id)
    print(user)
    await user.send(message)
  except:
    user = client.get_user(admin2)
    print(user)
    await user.send(message)

async def get_server_stats():
  pass

def dm_toggle():
  dm = not dm
  if dm :
    send_dm("DM is now ON")
  else:
    send_dm("DM is now OFF")
#+++++++++++++++++++++++++++++++++++++++++++++++

#++++++++++++++++++++++EVENTS++++++++++++++++++++++
@client.listen('on_message')
async def filter(message):
  if message.author == client.user: return
  if message.content == "sudo  how are you?":
    await message.channel.send("like a boss")
  message_list = message.content.split(' ')
  if any(badword in message_list for badword in ['nigga', 'nigger']):
    await message.author.ban(reason = "used n word")
    await message.channel.send(f"Banned {message.author} for using a bad word")
    await send_dm(f"{ctx.author} banned {message.author.name} for using n word")

  if any(badword in message_list for badword in badwords):
    channel = message.channel
    await channel.send(f"{message.author.mention} Pls avoid using vulgar words.")
    await message.delete()
    print(message.channel.mention)
    print(message.channel.id)
    await send_dm(f"Message {message.content} deleted in #{message.channel.mention} from {message.author.mention}")

#++++++++++++++++++++++COMMANDS++++++++++++++++++++

#==============TEST========================
@client.command()
@has_permissions(kick_members=True)  
async def hello(ctx):
  await ctx.send("Sup!")

@client.command()
async def bye(ctx):
   await ctx.send("Bye!")
 
@client.command()
async def hi(ctx):
   await ctx.send("Hello!")

# @client.command()
# async def (ctx):
#    await ctx.send("")

#==============DM TOGGLE===================

@client.command()
@has_permissions(kick_members=True)
def toggleDM():
  dm_toggle()

#==============KICK========================

@client.command()
@has_permissions(kick_members=True)  
async def kick(ctx, member : discord.Member, reason=None):
  try:
    await member.kick(reason = reason)
    await ctx.send(f"Kicked {member} for {reason}")
    if dm:
      await send_dm(f"{ctx.author} kicked {member.name} for {reason}")
  except:
    await ctx.send("some error occured. try again.")

#==============BAN==========================
@client.command()
@has_permissions(ban_members=True)  
async def ban(ctx, member:discord.Member, reason=None):
  try:
    await member.ban(reason = reason)
    await ctx.send(f"Banned {member} for {reason}")
    if dm:
      await send_dm(f"{ctx.author} banned {member.name} for {reason}")
  except Exception as e:
    print(e)
    await ctx.send("some error occured. try again.")
#==============UNBAN======================
@client.command()
@has_permissions(ban_members=True)  
async def unban(ctx,*, member):
  try:
    banned_users = await ctx.guild.bans()
    member = member.split("#")
    member_name = member[0]
    member_discriminator = member[1]
    for ban_entry in banned_users:
      user = ban_entry.user
      if (user.name, user.discriminator) == (member_name, member_discriminator):
        await ctx.guild.unban(user)
        await ctx.send(f"Unbanned {member_name}")
        if dm:
          await send_dm(f"{ctx.author} unbanned {member_name}")
  except:
    await ctx.send("some error occured. try again.")
#==============MUTE========================
@client.command()
@has_permissions(kick_members=True)
async def mute(ctx, member: discord.Member, time_, reason):
  time_ = convert(time_)
  print(f"Muting..{member.name}")
  try:
    for role in member.guild.roles:
      if role.name == main_role:
        await member.remove_roles(role)
        await ctx.send(f"Muted {member} for {reason} for {time_} minutes")
        if dm:
          await send_dm(f"{ctx.author.mention} muted {member} for {reason} for {time_} minutes")

        if time_ > 0:
          await asyncio.sleep(time_ * 60)

          await member.add_roles(role)
          await ctx.send(f"Unmuted {member}")
      
  except:
    await ctx.send("An Error Occured  :(")

  return

#==============UNMUTE========================
@client.command()
@has_permissions(kick_members=True)
async def unmute(ctx, member: discord.Member):
  try:
    for role in member.guild.roles:
      if role.name == main_role:
        await member.add_roles(role)
        await ctx.send(f"Unmuted {member}")
        if dm:
          await send_dm(f"Muted {member} for {reason} for {time_} minutes")
  except Exception as e:
    print(e)
    await ctx.send("some error occured. try again.")
#==============ANNOUNCE====================
@client.command()
@has_permissions(kick_members=True)  
async def announce(ctx, channel, *, message):
  try:
    channel = channel[2:-1]
    print(channel)
    announce_channel = client.get_channel(int(channel))
    for role in ctx.author.guild.roles:
      if role.name == announcement_ping:
        await announce_channel.send(f"<@&{role.id}> {message}")
  except:
    ctx.send("some error occured. try again.")
#++++++++++++++++++RUNNING++++++++++++++++++++++

client.run(token) 

##+++++++++++++++++++++++++++++++++++++++++++++++

#TODOS:
# DATABASE STUFF(STORING BANS ETC.)


#Sabby, todos: