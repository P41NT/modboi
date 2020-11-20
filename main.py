import discord
from discord.ext import commands
import asyncio
from discord.ext.commands import has_permissions
import sqlite3
import os.path

#++++++++++++++++++++PARAMETERS+++++++++++++++++
token = "Nzc1MzMyNDQ4NjI3NzIwMjMy.X6kynA.I84ecXcrMvcg1YlurbVJi_VQVbw"
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
  #   info_string += f"{int(info_list[i][0])} {int(info_list[i][1])} {int(info_list[i][2])} \n"
  #   # info_string += f"{client.get_user(int(info_list[i][0])).mention} {info_list[i][2]} {client.get_user(int(info_list[i][1])).mention} \n"
  #   print(info_string)
  embed = discord.Embed(title=f"INFO OF {member.name}", description=info_string,  color=discord.Color.blue())
  await ctx.send(embed = embed)
  # await ctx.send(info_list)

@client.command()
async def info_kick(ctx):
  c.execute(f"SELECT * FROM info WHERE action='KICK'")
  info_list_kick = c.fetchall()
  info_string_kick = "fjkasdjflkd"
  for i in range(len(info_list)):
    info_string_kick+="<@" + info_list_kick[i][0] + ">"  + " " + "<@" + info_list_kick[i][1] + ">"  + " " + info_list_kick[i][2] + "\n"
  #   info_string += f"{int(info_list[i][0])} {int(info_list[i][1])} {int(info_list[i][2])} \n"
  #   # info_string += f"{client.get_user(int(info_list[i][0])).mention} {info_list[i][2]} {client.get_user(int(info_list[i][1])).mention} \n"
  #   print(info_string)
  print(info_string_kick)
  print(info_list_kick)
  embed = discord.Embed(title=f"INFO OF {member.name}", description=info_string_kick,  color=discord.Color.blue())
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
  if message.content == "sudo how are you?":
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

#==============WARN========================
# @client.command()
# @has_permissions(kick_members=True)
# async def warn(ctx, member :discord.Member, reason):
#   try:
#     await ctx.send(f"Warned {member.mention} for {reason}")
#     if dm:
#       await send_dm(f"{ctx.author} warned {member.name} for {reason}")

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
        c.execute(f"INSERT INTO info VALUES ('{ctx.author.id}', '{user.id}', 'UNBAN')")
        conn.commit()
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
        c.execute(f"INSERT INTO info VALUES ('{ctx.author.id}', '{member.id}', 'MUTE')")
        conn.commit()

        if time_ > 0:
          await asyncio.sleep(time_ * 60)

          await member.add_roles(role)
          await ctx.send(f"Unmuted {member}")
      
  except Exception as e:
    print(e)
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
        c.execute(f"INSERT INTO info VALUES ('{ctx.author.id}', '{member.id}', 'UNMUTE')")
        conn.commit()
        if dm:
          await send_dm(f"UnMuted {member}")
  except Exception as e:
    print(e)
    await ctx.send("some error occured. try again.")
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
    await message.channel.send("Some error occured. try again.")

@client.command()
@has_permissions(manage_channels=True)
async def lock(ctx, channel : discord.TextChannel=None):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    overwrite.send_messages = False
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send('Channel locked.')

@client.command()
@has_permissions(manage_channels=True)
async def unlock(ctx, channel : discord.TextChannel=None):
    channel = channel or ctx.channel
    overwrite = channel.overwrites_for(ctx.guild.default_role)
    print(ctx.guild.default_role)
    overwrite.send_messages = True
    await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
    await ctx.send('Channel unlocked.')


@client.command()
async def userinfo(ctx, target: discord.Member):
  if ctx.author.guild_permissions.administrator:
    x = ctx.guild.members
    print(x)
    roles = [role for role in target.roles]
    embed = discord.Embed(title="User information", colour=discord.Color.gold(), timestamp=datetime.utcnow())

    embed.set_author(name=target.name, icon_url=target.avatar_url)

    embed.set_thumbnail(url=target.avatar_url)

    fields = [("Name", str(target), False),
          ("ID", target.id, False),
          ("Status", str(target.status).title(), False),
          (f"Roles ({len(roles)})", " ".join([role.mention for role in roles]), False),
          ("Created at", target.created_at.strftime("%d/%m/%Y %H:%M:%S"), False),
          ("Joined at", target.joined_at.strftime("%d/%m/%Y %H:%M:%S"), False)]

    for name, value, inline in fields:
      embed.add_field(name=name, value=value, inline=inline)

    await ctx.send(embed=embed)
  else:
    await ctx.send(f'Not enough permissions')

#++++++++++++++++++RUNNING++++++++++++++++++++++

client.run(token) 

##+++++++++++++++++++++++++++++++++++++++++++++++

#TODOS:
# WARNS
# DATABASE STUFF(STORING BANS ETC.)