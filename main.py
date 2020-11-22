import discord
from discord.ext import commands
import asyncio
from discord.ext.commands import has_permissions
import sqlite3
import os.path
import random
import subprocess

#++++++++++++++++++++PARAMETERS+++++++++++++++++
token = "Nzc1MzMyNDQ4NjI3NzIwMjMy.X6kynA.XlnDNkUCy8Dhyt4Q4D6rm_Go_1o"
command_prefix = "sudo "
main_role = "Everyone" #change to verified.
announcement_ping = "Oppressors"
badwords = ["nidda", "porn", "gay" ,"sex" , "motherfucker", "motherfuckers", "fucker", "fucking", "bitch", "nigga", "dick", "pussy", "fuck","nigger"]
mute_roles = ["MUTED"] #whatever u want to be given
mute_roles_taken = ["Morons", "Oppressors", "Oppressed", "Everyone"]#Change to all the roles
admin_id = 713735322399277087
admin2 = 489092730253737986
dm = True
meme_file = open('memes.txt', 'r')
memes = meme_file.read().split("\n")
memes = memes[:-1]
#+++++++++++++++++++++++++++++++++++++++++++++++

#++++++++++++++++++++++INITIALIZE++++++++++++++++
client = commands.Bot(command_prefix=command_prefix)

@client.event
async def on_ready():
  print("[*] Terminator Status : SkyNet Activated.")


if not os.path.isfile('./info.db'):
  conn = sqlite3.connect("info.db")

  c = conn.cursor()
  c.execute("""CREATE TABLE info(
    mod text,
    user text,
    action text
  )""")
else:
  conn = sqlite3.connect("info.db")
  c = conn.cursor()

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

def getaction(action):
  action_dict = {"BAN" : 'BANNED', 'KICK' : 'KICKED', 'MUTE': 'MUTED', 'UNMUTE': 'UNMUTED'}
  return action_dict[action]


#+++++++++++++++++++++++++++++++++++++++++++++++

#++++++++++++++++++++++DATABASE++++++++++++++++++++++

@client.command()
async def info(ctx, member: discord.Member):
  print(member.id)
  c.execute(f"SELECT * FROM info WHERE user='{member.id}'")
  info_list = c.fetchall()
  print(info_list)
  info_string = ""
  for i in range(len(info_list)):
    info_string+="<@" + info_list[i][0] + ">"  + " " + "<@" + info_list[i][1] + ">"  + " " + info_list[i][2] + "\n"
  embed = discord.Embed(title=f"INFO OF {member.name}", description=info_string,  color=discord.Color.blue())
  await ctx.send(embed = embed)
  # await ctx.send(info_list)


#++++++++++++++++++++++EVENTS++++++++++++++++++++++

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
      await ctx.send("That command wasn't found! Sorry :(")
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
      await ctx.send("You missed some argument I guess.")
      

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
    await channel.send(f"{message.author.mention} That word is not allowed here, continuing will result in mute.")
    await message.delete()
    await send_dm(f"Message '{message.content}' deleted in #{message.channel.mention} from {message.author.mention}")

#++++++++++++++++++++++COMMANDS++++++++++++++++++++

#==============TEST========================
@client.command()
@has_permissions(kick_members=True)  
async def hello(ctx):
  await ctx.send("Sup!")

@client.command()
async def bye(ctx):
   await ctx.send("Bye!")


#==============DM TOGGLE===================

#==============WARN========================
@client.command()
@has_permissions(kick_members=True)
async def warn(ctx, member :discord.Member, reason):
  try:
    await ctx.send(f"Warned {member.mention} for {reason}")
    c.execute(f"INSERT INTO info VALUES ('{ctx.author.id}', '{member.id}', 'WARN')")
    conn.commit()
    if dm:
      await send_dm(f"{ctx.author} warned {member.name} for {reason}")
  except:
    ctx.send("An error occured boi.. :(")

#==============KICK========================

@client.command()
@has_permissions(kick_members=True)
async def kick(ctx, member : discord.Member, reason=None):
  try:
    await member.kick(reason = reason)
    await ctx.send(f"Kicked {member} for {reason}")
    if dm:
      await send_dm(f"{ctx.author} kicked {member.name} for {reason}")
    c.execute(f"INSERT INTO info VALUES ('{ctx.author.id}', '{member.id}', 'KICK')")
    conn.commit()
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
    c.execute(f"INSERT INTO info VALUES ('{ctx.author.id}', '{member.id}', 'BAN')")
    conn.commit()
  except Exception as e:
    print(e)
    await ctx.send("Some error occured. Try again.")
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
          await send_dm(f"{ctx.author} Unbanned {member_name}")
        c.execute(f"INSERT INTO info VALUES ('{ctx.author.id}', '{user.id}', 'UNBAN')")
        conn.commit()
  except:
    await ctx.send("Some error occured. Try again.")
  
#==============MUTE========================
@client.command()
async def mute(ctx, member: discord.Member):
    for channel in ctx.guild.text_channels:
        perms = channel.overwrites_for(member)
        perms.send_messages = False
        await channel.set_permissions(member, overwrite=perms, reason="Muted!")
    await ctx.send(f"{member} has been muted.")
    c.execute(f"INSERT INTO info VALUES ('{ctx.author.id}', '{member.id}', 'MUTE')")
    conn.commit()
    if dm:
      await send_dm(f"Muted {member}")

#==============UNMUTE========================
@client.command()
async def unmute(ctx, member: discord.Member):
    for channel in ctx.guild.text_channels:
        perms = channel.overwrites_for(member)
        perms.send_messages = True
        await channel.set_permissions(member, overwrite=perms, reason="Muted!")
    await ctx.send(f"{member} has been muted.")
    c.execute(f"INSERT INTO info VALUES ('{ctx.author.id}', '{member.id}', 'UNMUTE')")
    conn.commit()
    if dm:
      await send_dm(f"Unmuted {member}")
    
#==============ANNOUNCE====================
@client.command()
@has_permissions(kick_members=True)  
async def announce(ctx, channel, *, message):
  try:
    channel = channel[2:-1]
    announce_channel = client.get_channel(int(channel))
    for role in ctx.author.guild.roles:
      if role.name == announcement_ping:
        await announce_channel.send(f"<@&{role.id}> {message}")
  except:
    await message.channel.send("Some error occured. Try again.")

#==============LOCK====================
@client.command()
@has_permissions(manage_channels=True)
async def lock(ctx, channel : discord.TextChannel=None):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send('Channel locked.')

#==============UNLOCK====================
@client.command()
@has_permissions(manage_channels=True)
async def unlock(ctx, channel : discord.TextChannel=None):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    print(ctx.guild.default_role)
    overwrite.send_messages = True
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send('Channel unlocked.')
 
#==============USERINFO====================
@client.command()
async def userinfo(ctx, *, user: discord.Member = None): 
    if user is None:
        user = ctx.author
    print(user)    
    date_format = "%a, %d %b %Y %I:%M %p"
    print(date_format)
    embed = discord.Embed(color=0xdfa3ff, description=user.mention)
    embed.set_author(name=str(user), icon_url=user.avatar_url)
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name="Joined", value=user.joined_at.strftime(date_format))
    print(embed)
    members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
    print(members)
    embed.add_field(name="Join position", value=str(members.index(user)+1))
    embed.add_field(name="Registered", value=user.created_at.strftime(date_format))
    if len(user.roles) > 1:
        role_string = ' '.join([r.mention for r in user.roles][1:])
        embed.add_field(name="Roles [{}]".format(len(user.roles)-1), value=role_string, inline=False)
    perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
    embed.add_field(name="Guild permissions", value=perm_string, inline=False)
    embed.set_footer(text='ID: ' + str(user.id))
    return await ctx.send(embed=embed)

#==============MEME====================
@client.command()
async def meme(ctx):
  meme_no = random.randint(0, 400)
  await ctx.send(memes[meme_no])

#==============GEN_MEME====================
@client.command()
async def gen_meme(ctx):
  await ctx.send("Generating Memes")
  subprocess.Popen(["python", "memes.py"])
#++++++++++++++++++RUNNING++++++++++++++++++++++

client.run(token) 

##+++++++++++++++++++++++++++++++++++++++++++++++

#TODOS:
# DATABASE STUFF(STORING BANS ETC.)
