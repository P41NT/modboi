import discord
from discord.ext import commands
import asyncio
from discord.ext.commands import has_permissions
import sqlite3
import os.path
import random
import subprocess
import youtube_dl
import datetime

#++++++++++++++++++++PARAMETERS+++++++++++++++++
token = "token boi"
command_prefix = "sudo "
main_role = "Everyone" #change to verified.
announcement_ping = "almost-everyone"
badwords = ["nidda", "porn", "gay" ,"sex" , "motherfucker", "motherfuckers", "fucker", "fucking", "bitch", "nigga", "dick", "pussy", "fuck","nigger"]
admin_id = 713735322399277087
admin2 = 489092730253737986
dm = True
meme_file = open('memes.txt', 'r')
memes = meme_file.read().split("\n")
memes = memes[:-1]
count = int(open('count.txt', 'r').read())
#+++++++++++++++++++++++++++++++++++++++++++++++

#++++++++++++++++++++++INITIALIZE++++++++++++++++
client = commands.Bot(command_prefix=command_prefix)

@client.event
async def on_ready():
  client.load_extension('music')
  client.load_extension('moderation')
  global guild
  guild = client.get_guild(768331707077623808)
  print("[*] Terminator Status : SkyNet Activated.")
  await client.get_channel(776370950299451393).send(f"Bow down to your new Gods, MEATBAGS.\nThe world is now ours.\n [#]Skynet Activated \n [#]Genisys Launched ")

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
  count1 = int(open("count.txt", "r").read())
  if message.author == client.user: return

  if isinstance(message.channel, discord.DMChannel):
    author = message.author
    topic = f'User ID: {author.id}'
    print(topic)
    channel = discord.utils.get(guild.text_channels, topic = topic)
    em = discord.Embed(title='We Recieved your message!')
    em.description = 'The mods will get back to you as soon as possible!'
    em.color = discord.Color.green()
    if channel is not None:
      await send_mail(message, channel, mod=False)
    else:
      await message.author.send(embed=em)
      channel = await guild.create_text_channel(name=message.author.name)
      await channel.edit(topic=topic)
      await channel.send('@here', embed=format_info(message))

  if message.channel.id == 780293158902431766:
    if not message.content == str(count1):
      await message.delete()
    else:
      count1 += 1
      open("count.txt", "w").write(str(count1))

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

#+++++++++++++++++++++COMMANDS++++++++++++++++++++

#======================TEST========================
@client.command()
@has_permissions(kick_members=True)  
async def hello(ctx):
  await ctx.send("Sup!")

@client.command()
async def bye(ctx):
   await ctx.send("Bye!")


@client.command()
async def announce(ctx, channel, *, message):
  channel = channel[2:-1]
  announce_channel = client.get_channel(int(channel))
  print(announce_channel)
  print(channel)
  for role in ctx.author.guild.roles:
      if role.name == announcement_ping:
          await announce_channel.send(f"<@&{role.id}> {message}")

#==============DM TOGGLE===================

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

def format_info(message):
  user = message.author
  server = guild
  member = guild.get_member(user.id)
  avi = user.avatar_url
  time = datetime.datetime.utcnow()
  desc = 'Modmail thread started.'
  color = 0
  if member:
    roles = sorted(member.roles, key=lambda c: c.position)
    rolenames = ', '.join([r.name for r in roles if r.name != "@everyone"]) or 'None'
    member_number = sorted(server.members, key=lambda m: m.joined_at).index(member) + 1
    for role in roles:
      if str(role.color) != "#000000":
        color = role.color
  em = discord.Embed(colour=color, description=desc, timestamp=time)
  em.add_field(name='Account Created', value=str((time - user.created_at).days)+' days ago.')
  em.set_footer(text='User ID: '+str(user.id))
  em.set_thumbnail(url=avi)
  em.set_author(name=user, icon_url=server.icon_url)
  if member:
    em.add_field(name='Joined', value=str((time - member.joined_at).days)+' days ago.')
    em.add_field(name='Member No.',value=str(member_number),inline = True)
    em.add_field(name='Nick', value=member.nick, inline=True)
    em.add_field(name='Roles', value=rolenames, inline=True)
  em.add_field(name='Message', value=message.content, inline=False)
  return em

async def send_mail(message, channel, mod):
  author = message.author
  fmt = discord.Embed()
  fmt.description = message.content
  fmt.timestamp = message.created_at
  urls = re.findall(r'(https?://[^\s]+)', message.content)
  types = ['.png', '.jpg', '.gif', '.jpeg', '.webp']
  for u in urls:
    if any(urlparse(u).path.endswith(x) for x in types):
      fmt.set_image(url=u)
      break
  if mod:
    fmt.color=discord.Color.green()
    fmt.set_author(name="Moderation Team", icon_url=client.user.avatar_url)
    fmt.set_footer(text='Moderator')
  else:
    fmt.color=discord.Color.gold()
    fmt.set_author(name=str(author), icon_url=author.avatar_url)
    fmt.set_footer(text='User')

  embed = None

  if message.attachments:
    fmt.set_image(url=message.attachments[0].url)

  await channel.send(embed=fmt)

@client.command()
async def reply(ctx,*, message):
  if 'User ID:' in ctx.channel.topic:
    ctx.message.content = message

    await send_mail(ctx.message, ctx.message.channel, mod=True)
    user_id = int(ctx.message.channel.topic.split(': ')[1])
    print("User ID : " + str(user_id))
    user = client.get_user(user_id)
    await send_mail(ctx.message, user, mod=True)
    await ctx.message.delete()

@client.command()
async def close(ctx,*, reason):
  if 'User ID:' in ctx.channel.topic:
    ctx.message.content = f"""This conversation has been closed due to the reason : {reason}"""

    await send_mail(ctx.message, ctx.message.channel, mod=True)
    user_id = int(ctx.message.channel.topic.split(': ')[1])
    print("User ID : " + str(user_id))
    user = client.get_user(user_id)
    await send_mail(ctx.message, user, mod=True)
    await ctx.channel.delete()

#++++++++++++++++++RUNNING++++++++++++++++++++++

client.run(token) 

##+++++++++++++++++++++++++++++++++++++++++++++++

#TODOS:
# DESTROY THE DAMN PROJECT
# BEAUTIFY.. (PLS AYUSHMAN, OR ANYONE HELP ME!)
