from discord.ext import commands
import discord

class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        main_role = "Everyone" #change to verified.
        announcement_ping = "Oppressors"
        badwords = ["nidda", "porn", "gay" ,"sex" , "motherfucker", "motherfuckers", "fucker", "fucking", "bitch", "nigga", "dick", "pussy", "fuck","nigger"]
        admin_id = 713735322399277087
        admin2 = 489092730253737986
        dm = True
        meme_file = open('memes.txt', 'r')
        memes = meme_file.read().split("\n")
        memes = memes[:-1]
        count = int(open('count.txt', 'r').read())
    #==============WARN========================
    @commands.command()
    async def warn(self, ctx, member :discord.Member, reason):
        try:
            await ctx.send(f"Warned {member.mention} for {reason}")
            print(c)
            c.execute(f"INSERT INTO info VALUES ('{ctx.author.id}', '{member.id}', 'WARN')")
            conn.commit()
            if dm:
                await send_dm(f"{ctx.author} warned {member.name} for {reason}")
        except:
            ctx.send("An error occured boi.. :(")

    #=================KICK======================

    @commands.command()
    async def kick(self, ctx, member : discord.Member, reason=None):
        await member.kick(reason = reason)
        await ctx.send(f"Kicked {member} for {reason}")
        if dm:
            await send_dm(f"{ctx.author} kicked {member.name} for {reason}")
        c.execute(f"INSERT INTO info VALUES ('{ctx.author.id}', '{member.id}', 'KICK')")
        conn.commit()

    #==============BAN==========================
    @commands.command()
    async def ban(self, ctx, member:discord.Member, reason=None):
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
    @commands.command() 
    async def unban(self, ctx,*, member):
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
    @commands.command()
    async def mute(self, ctx, member: discord.Member):
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
    @commands.command()
    async def unmute(self, ctx, member: discord.Member):
        for channel in ctx.guild.text_channels:
            perms = channel.overwrites_for(member)
            perms.send_messages = True
            await channel.set_permissions(member, overwrite=perms, reason="Muted!")
        await ctx.send(f"{member} has been muted.")
        c.execute(f"INSERT INTO info VALUES ('{ctx.author.id}', '{member.id}', 'UNMUTE')")
        conn.commit()
        if dm:
            await send_dm(f"Unmuted {member}")
        

    #==============LOCK====================
    @commands.command()
    async def lock(self, ctx, channel : discord.TextChannel=None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send('Channel locked.')

    #==============UNLOCK====================
    @commands.command()
    async def unlock(self, ctx, channel : discord.TextChannel=None):
        channel = channel or ctx.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        print(ctx.guild.default_role)
        overwrite.send_messages = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        await ctx.send('Channel unlocked.')

def setup(bot):
  bot.add_cog(ModerationCog(bot))