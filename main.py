import discord
from discord.ext import commands, tasks
from discord.ext import commands
from discord import Member

from discord.ext.commands import Cog, Greedy
import asyncio

from itertools import cycle
import os
import json
import random
import keep_alive
import typing
from datetime import datetime
import datetime
import time

from datetime import datetime, timedelta
import logging

from typing import Optional

from discord.ext.commands import BadArgument, Bot, Context, Converter, IDConverter, MemberConverter, UserConverter

from discord.utils import DISCORD_EPOCH, escape_markdown, snowflake_time

from dateutil.relativedelta import relativedelta
from discord import TextChannel

from discord.ext.commands import Cog, Context, group, has_any_role

from discord import Intents
from discord import Embed
import psutil









prefixes = ["b!", "B!"]
intents = Intents.default()
intents.members = True
activity = discord.Activity(type=discord.ActivityType.watching, name="b!setup | b!help", description="https://discord.com/api/oauth2/authorize?client_id=861968479392497665&permissions=8&scope=bot")
client = commands.Bot(command_prefix=prefixes, activity=activity, status=discord.Status.idle, help_command=None, intents=intents)












time_window_milliseconds = 5000
max_msg_per_window = 5
max_msg_per_ban = 2
max_msg_per_channel = 4
max_msg_per_role = 2
max_msg_per_chr = 3
max_msg_per_ror = 2

author_msg_times = {}

everyone = ["@everyone", "@here"]
banwords = ["Discord.gg/", "discord.gg/", "https://discord.gg/", "https://Discord.gg/"]
#client.warnings = {
        #guild_id : (member_id: [count, [(admin_id, reason)]])
#}
lag = ["<@"]










                                
WARNS = []
ANTI_SPAM = {}
JOIN_LEAVE_DETECTOR = {}





@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))







@client.command()
async def ping(ctx):
        msg = discord.Embed(title="Bot's Performance", description=f"**Latency**\n<:blank:892745849807982632> <:BabatinsRR:893827627406729248> {round(client.latency * 1000)}ms\n**Cpu**\n<:blank:892745849807982632> <:BabatinsRR:893827627406729248> {psutil.cpu_percent()}%")
        await ctx.send(embed=msg)




@client.command()
async def babatins(ctx):
    await ctx.send(embed=discord.Embed(title="Babatin's Info Command", description=f"{len(client.guilds)} servers, {len(client.users)} users | Database is connected"))


#add role




@client.command(pass_context=True)
@commands.has_permissions(administrator=True) #permissions
async def role(ctx, user : discord.Member, *, role=None):
        if not role:
                msg = discord.Embed(description=":x: no role was given please try again",
                color=discord.Colour.dark_theme())
                await ctx.send(embed=msg)
                return
        rolee = discord.utils.get(ctx.guild.roles, name=(role))
        if not rolee:
                msg = discord.Embed(description=":x: That role doesn't exist please try again",
                color=discord.Colour.dark_theme())
                await ctx.send(embed=msg)
                return
        else:
                if rolee.position > ctx.author.top_role.position:
                        return await ctx.send('**:x: | That role is above your top role!**') 
                if rolee in user.roles:
                        await ctx.author.remove_roles(rolee) #removes the role if user already has
                        msg = discord.Embed( description=f"<:babatinS:892818123374329977> Successfully removed {rolee} from {user.mention}", color=discord.Colour.dark_theme())
                        await ctx.send(embed=msg)
                else:
                        await ctx.author.add_roles(rolee)
                        msg = discord.Embed(description=f"<:babatinS:892818123374329977> Successfully added {rolee} to {user.mention}", color=discord.Colour.dark_theme())
                        await ctx.send(embed=msg)


@role.error
async def commands_to_use_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        
        await ctx.send(f'**:x: | You dont have permissions to do that {ctx.message.author.mention}**')









log_channel = []







@client.event
async def on_member_join(member):
        em = discord.Embed(title="Member joins")
        em.add_field(name="Created At", value=f"{member.mention}, {member.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S')}")
        em.set_author(name=str(member), icon_url=member.avatar_url)
        await post_modlogg(embed=em, guild=member.guild)



@client.event
async def on_member_leave(member):
        em = discord.Embed(title="Member left")
        em.add_field(name="Created At", value=f"{member.mention}, {member.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S')}")
        em.set_author(name=str(member), icon_url=member.avatar_url)
        await post_modlogg(embed=em, guild=member.guild)
        
@client.event
async def on_message(ctx):
        if ctx.author == client.user:
                return

        if any(word in ctx.content for word in banwords):
                if ctx.author.guild_permissions.manage_messages:
                        return
                else:
        #le = ctx.content
        #if any(word in len(le) for word in ) 
                        await ctx.delete()
                        msg = 'Do Not Promote Servers {0.author.mention}'.format(ctx)
                        await ctx.channel.send(msg, delete_after=3)
        await client.process_commands(ctx)
        global author_msg_counts
        author_id = ctx.author.id
        # Get current epoch time in milliseconds
        curr_time = datetime.now().timestamp() * 1000

        # Make empty list for author id, if it does not exist
        if not author_msg_times.get(author_id, False):
                author_msg_times[author_id] = []

        # Append the time of this message to the users list of message times
        author_msg_times[author_id].append(curr_time)

        # Find the beginning of our time window.
        expr_time = curr_time - time_window_milliseconds

        # Find message times which occurred before the start of our window
        expired_msgs = [
        msg_time for msg_time in author_msg_times[author_id]
        if msg_time < expr_time
        ]

        # Remove all the expired messages times from our list
        for msg_time in expired_msgs:
                author_msg_times[author_id].remove(msg_time)
        # ^ note: we probably need to use a mutex here. Multiple threads
        # might be trying to update this at the same time. Not sure though.\
        
        if len(author_msg_times[author_id]) > max_msg_per_window:
                if ctx.author.guild_permissions.manage_messages:
                        return
                
                guild = ctx.guild
                mutedRole = discord.utils.get(guild.roles, name="Muted")
                if not mutedRole:
                        mutedRole = await guild.create_role(name="Muted")
                        for channel in guild.channels:
                                await channel.set_permissions(mutedRole, speak=False, send_messages=False)
                await ctx.author.add_roles(mutedRole)
                for channel in guild.channels:
                        await channel.set_permissions(mutedRole, speak=False, send_messages=False)
                #triumvirato = discord.utils.get(guild.roles, name="Muted")
                #if triumvirato in ctx.author.roles:
        

        
#Anti-ch delete
@client.event
async def on_guild_channel_delete(channel):
        guild = channel.guild
        logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_delete).flatten()
        logs = logs[0]
        author_id = guild.get_member(logs.user.id)
        
        # Get current epoch time in milliseconds
        curr_time = datetime.now().timestamp() * 1000

        # Make empty list for author id, if it does not exist
        if not author_msg_times.get(author_id, False):
                author_msg_times[author_id] = []

        # Append the time of this message to the users list of message times
        author_msg_times[author_id].append(curr_time)

        # Find the beginning of our time window.
        expr_time = curr_time - time_window_milliseconds

        # Find message times which occurred before the start of our window
        expired_msgs = [
        msg_time for msg_time in author_msg_times[author_id]
        if msg_time < expr_time
        ]

        # Remove all the expired messages times from our list
        for msg_time in expired_msgs:
                author_msg_times[author_id].remove(msg_time)
        # ^ note: we probably need to use a mutex here. Multiple threads
        # might be trying to update this at the same time. Not sure though.\
        if len(author_msg_times[author_id]) > max_msg_per_chr:
                reason = "Anti-Nuke Reason: Deleting to many channels"
                member = guild.get_member(logs.user.id)
                await member.ban(reason=reason)
#Anti-Role spam
@client.event
async def on_guild_role_create(role):
        guild = role.guild
        logs = await guild.audit_logs(limit=1,after=datetime.now() - timedelta(hours=1),  action=discord.AuditLogAction.role_create).flatten()
        logs = logs[0]
        author_id = guild.get_member(logs.user.id)
        # Get current epoch time in milliseconds
        curr_time = datetime.now().timestamp() * 1000

        # Make empty list for author id, if it does not exist
        if not author_msg_times.get(author_id, False):
                author_msg_times[author_id] = []

        # Append the time of this message to the users list of message times
        author_msg_times[author_id].append(curr_time)

        # Find the beginning of our time window.
        expr_time = curr_time - time_window_milliseconds

        # Find message times which occurred before the start of our window
        expired_msgs = [
        msg_time for msg_time in author_msg_times[author_id]
        if msg_time < expr_time
        ]

        # Remove all the expired messages times from our list
        for msg_time in expired_msgs:
                author_msg_times[author_id].remove(msg_time)
        # ^ note: we probably need to use a mutex here. Multiple threads
        # might be trying to update this at the same time. Not sure though.\
        if len(author_msg_times[author_id]) > max_msg_per_role:
                reason = "Anti-Nuke Reason: Creating to many roles"
                member = guild.get_member(logs.user.id)
                await member.ban(reason=reason)
                await role.delete() 

#Anti-Role delete
@client.event
async def on_guild_role_delete(role):
        guild = role.guild
        logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.role_delete).flatten()
        logs = logs[0]
        author_id = guild.get_member(logs.user.id)

        # Get current epoch time in milliseconds
        curr_time = datetime.now().timestamp() * 1000

        # Make empty list for author id, if it does not exist
        if not author_msg_times.get(author_id, False):
                author_msg_times[author_id] = []

        # Append the time of this message to the users list of message times
        author_msg_times[author_id].append(curr_time)

        # Find the beginning of our time window.
        expr_time = curr_time - time_window_milliseconds

        # Find message times which occurred before the start of our window
        expired_msgs = [
        msg_time for msg_time in author_msg_times[author_id]
        if msg_time < expr_time
        ]

        # Remove all the expired messages times from our list
        for msg_time in expired_msgs:
                author_msg_times[author_id].remove(msg_time)
        # ^ note: we probably need to use a mutex here. Multiple threads
        # might be trying to update this at the same time. Not sure though.\
        if len(author_msg_times[author_id]) > max_msg_per_ror:
                reason = "Anti-Nuke Reason: Deleting to many roles"
                member = guild.get_member(logs.user.id)
                await member.ban(reason=reason)  
#Anti-Emoji Spam
@client.event
async def on_emoji_update(emoji):
        guild = emoji.guild
        logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.emoji_update).flatten()
        logs = logs[0]
        author_id = guild.get_member(logs.user.id)
        # Get current epoch time in milliseconds
        curr_time = datetime.now().timestamp() * 1000

        # Make empty list for author id, if it does not exist
        if not author_msg_times.get(author_id, False):
                author_msg_times[author_id] = []

        # Append the time of this message to the users list of message times
        author_msg_times[author_id].append(curr_time)

        # Find the beginning of our time window.
        expr_time = curr_time - time_window_milliseconds

        # Find message times which occurred before the start of our window
        expired_msgs = [
        msg_time for msg_time in author_msg_times[author_id]
        if msg_time < expr_time
        ]

        # Remove all the expired messages times from our list
        for msg_time in expired_msgs:
                author_msg_times[author_id].remove(msg_time)
        # ^ note: we probably need to use a mutex here. Multiple threads
        # might be trying to update this at the same time. Not sure though.\
        if len(author_msg_times[author_id]) > max_msg_per_windowwww:
                reason = "Anti-Nuke Reason: Creating to many emojis"
                member = guild.get_member(logs.user.id)
                await member.ban(reason=reason)
#Anti-MassBan             
@client.event                     
async def on_member_ban(guild, user):
        logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.ban).flatten()
        logs = logs[0]

        author_id = guild.get_member(logs.user.id)
        # Get current epoch time in milliseconds
        curr_time = datetime.now().timestamp() * 1000

        # Make empty list for author id, if it does not exist
        if not author_msg_times.get(author_id, False):
                author_msg_times[author_id] = []

        # Append the time of this message to the users list of message times
        author_msg_times[author_id].append(curr_time)

        # Find the beginning of our time window.
        expr_time = curr_time - time_window_milliseconds

        # Find message times which occurred before the start of our window
        expired_msgs = [
        msg_time for msg_time in author_msg_times[author_id]
        if msg_time < expr_time
        ]

        # Remove all the expired messages times from our list
        for msg_time in expired_msgs:
                author_msg_times[author_id].remove(msg_time)
        # ^ note: we probably need to use a mutex here. Multiple threads
        # might be trying to update this at the same time. Not sure though.\
        if len(author_msg_times[author_id]) > max_msg_per_ban:
                reason = "Anti-Nuke Reason: Banning to many members"
                member = guild.get_member(logs.user.id)
                await member.ban(reason=reason)

#Anti-Channel Spam
@client.event
async def on_guild_channel_create(channel):
        guild = channel.guild
        logs = await guild.audit_logs(limit=1, after=datetime.now() - timedelta(hours=5), action=discord.AuditLogAction.channel_create).flatten()
        logs = logs[0]
        
        author_id = guild.get_member(logs.user.id)
                # Get current epoch time in milliseconds
        curr_time = datetime.now().timestamp() * 1000

                # Make empty list for author id, if it does not exist
        if not author_msg_times.get(author_id, False):
                author_msg_times[author_id] = []

                # Append the time of this message to the users list of message times
        author_msg_times[author_id].append(curr_time)

                # Find the beginning of our time window.
        expr_time = curr_time - time_window_milliseconds

                # Find message times which occurred before the start of our window
        expired_msgs = [
        msg_time for msg_time in author_msg_times[author_id]
        if msg_time < expr_time
        ]

                # Remove all the expired messages times from our list
        for msg_time in expired_msgs:
                author_msg_times[author_id].remove(msg_time)
                # ^ note: we probably need to use a mutex here. Multiple threads
                # might be trying to update this at the same time. Not sure though.\
        if len(author_msg_times[author_id]) > max_msg_per_channel:
                member = guild.get_member(logs.user.id)
                reason = "Anti-Nuke Reason: Creating to many channels"
                await member.ban(reason=reason)
                await channel.delete()

                        

                        
                


@client.command(pass_context=True)
@commands.has_permissions(manage_messages=True)
async def setdelay(ctx, seconds: int=None):
    if not seconds:
            await ctx.send('Please Put A Number For The Delay')
    else:
            await ctx.channel.edit(slowmode_delay=seconds)
            bby = discord.Embed(title='Set Delay', description=f"{ctx.author.mention} Set the slowmode delay in this channel to {seconds} seconds!", color= discord.Colour.blue())
            await ctx.send(embed=bby)


@setdelay.error
async def commands_to_use_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        
        await ctx.send(f'You dont have permissions to do that {ctx.message.author.mention}')

@client.command(pass_context=True)
@commands.has_permissions(manage_messages=True)
async def rdelay(ctx):
    await ctx.channel.edit(slowmode_delay=0)
    await ctx.send(f"The delay for this channel has been set to Default")
@rdelay.error
async def commands_to_use_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        
        await ctx.send(f'You dont have permissions to do that {ctx.message.author.mention}')
        

@client.command()
async def membercount(ctx):
        msg = discord.Embed(title="Members", description=f"{ctx.guild.member_count}", color=discord.Colour.orange())
        await ctx.send(embed=msg)

@client.command(pass_context=True)
@commands.has_permissions(manage_channels=True)
async def lock(ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=False)
        embed = discord.Embed(title = f"#{ctx.guild.name} is now under lockdown!!", description = f"", color = 0x2fa737) # Green
        await ctx.send(embed = embed)
@lock.error
async def commands_to_use_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f'You dont have permissions to do that {ctx.message.author.mention}')



@client.command(pass_context=True)
@commands.has_permissions(manage_channels=True)
async def unlock(ctx):
        await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
        
        bby = discord.Embed(title=f"#{ctx.guild.name} has been unlocked", description=f"", color= discord.Colour.green())
        await ctx.send(embed=bby)
@unlock.error
async def commands_to_use_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        
        await ctx.send(f'You dont have permissions to do that {ctx.message.author.mention}')

        



snipe_message_author = {}
snipe_message_content = {}

@client.event
async def on_message_delete(message):
  if not message.author.bot:
          embed = Embed(title=f"Message deleted in #{message.channel}",
          colour=message.author.colour,
          timestamp=datetime.utcnow())
          fields = [("Content", message.content, False)]
          for name, value, inline in fields:
                  embed.add_field(name=name, value=value, inline=inline)
          embed.set_author(name=str(message.author), icon_url=message.author.avatar_url)
          await post_modlogg(embed=embed, guild = message.guild)
  snipe_message_author[message.channel.id] = message.author
  snipe_message_content[message.channel.id] = message.content
  



@client.command(pass_context=True)
async def s(ctx):
  channel = ctx.channel
  try:
    
    em = discord.Embed(name = f"Last deleted message in #{channel.name}", description = snipe_message_content[channel.id], color=discord.Colour.dark_theme())
    em.set_footer(text = f"This message was sent by {snipe_message_author[channel.id]}")
    await ctx.send(embed = em)

  except:
    await ctx.send(f"There are no recently deleted messages in #{channel.name}")
    return



@client.command(pass_context=True)
@commands.has_permissions(manage_messages=True)
async def purge(ctx, limit=50, member: discord.Member=None):
    
    await ctx.message.delete()
    msg = []
    try:
        limit = int(limit)
    except:
        return await ctx.send("Please pass in an integer as limit")
    if not member:
        
        await ctx.channel.purge(limit=limit)
        return await ctx.send(f"Purged {limit} messages", delete_after=6)
    async for m in ctx.channel.history():
        
        if len(msg) == limit:
            break
        if m.author == member:
            msg.append(m)
    await ctx.channel.delete_messages(msg)
    await ctx.send(f"Purged {limit} messages of {member.mention}", delete_after=6)

@purge.error
async def commands_to_use_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):

        
        await ctx.send(f'You dont have permissions to do that {ctx.message.author.mention}')



@client.command(pass_context=True)
@commands.has_permissions(kick_members=True)   
async def kick(ctx, member : discord.Member=None, *, reason=None):
        if not member:
                await ctx.send("Please specify a member to kick")
        else:
                await member.kick(reason=reason)
                clearembed = discord.Embed(
                        description=f'*{ctx.message.author.mention} Kicked {member} reason: {reason}*',
                        color=(0xe74c3c))
                await ctx.send(embed=clearembed)
        
        
@kick.error
async def commands_to_use_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        
        await ctx.send(f'You dont have permissions to do that {ctx.message.author.mention}')
        






@client.command(pass_context = True)
@commands.has_permissions(ban_members=True)   
async def ban(ctx, member : discord.Member=None, *, reason=None):
        if not member:
                await ctx.send("Please specify a member to ban")
        else:
        
                await member.ban(reason=reason)
                clearembed = discord.Embed(
                
                description=f'{ctx.message.author.mention} Banned {member} reason: {reason}',
                color=(0xe74c3c))
                await ctx.send(embed=clearembed)
                await member.send(f"You were banned in {ctx.guild.name}.")

@ban.error
async def commands_to_use_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        
        await ctx.send(f'You dont have permissions to do that {ctx.message.author.mention}')






@client.command(description="Mutes the specified user.")
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
    embed = discord.Embed(title="muted", description=f"{member.mention} was muted ", colour=discord.Colour.light_gray())
    embed.add_field(name="reason:", value=reason, inline=False)
    await ctx.send(embed=embed)
    await member.add_roles(mutedRole, reason=reason)
    await member.send(f" you have been muted from: {guild.name} reason: {reason}")
    

@mute.error
async def commands_to_use_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
                await ctx.send(f'You dont have permissions to do that {ctx.message.author.mention}')






@client.command(pass_context=True)
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member=None):
        if not member:
                await ctx.send("Please specify a member to mute")
        else:
                mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
                
                
                await member.remove_roles(mutedRole)
                unembed=discord.Embed(description=f"Unmuted {member.mention}", color=(0xe74c3c))
                await ctx.send(embed=unembed)
                await member.send(f"You were unmuted in {ctx.guild.name}.")
@unmute.error
async def commands_to_use_error(ctx, error):

    if isinstance(error, commands.MissingPermissions):
        
        await ctx.send(f'You dont have permissions to do that {ctx.message.author.mention}')






@client.command(pass_context=True)
@commands.has_permissions(ban_members=True)
async def unban(ctx, *, member_id: int):
    
    """ command to unban user. check !help unban """
    await ctx.guild.unban(discord.Object(id=member_id))
    msg = discord.Embed(description=f"<@{member_id}> has been unbanned", color=(0xe74c3c))
    await ctx.send(embed=msg)


@unban.error
async def commands_to_use_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        
        await ctx.send(f'You dont have permissions to do that {ctx.message.author.mention}')





@client.command(pass_context=True)
async def serverinfo(ctx):
    """Displays server information."""



    embed = discord.Embed(title="{}'s info".format(ctx.guild.name), description=f"**Server name** {ctx.guild.name}:\n<:blank:892745849807982632> <:BabatinsRR:893827627406729248> **ID**: {ctx.guild.id}\n<:blank:892745849807982632> <:BabatinsRR:893827627406729248> **Region**: {ctx.guild.region}\n**Owner**: {ctx.guild.owner}\n**Verification Level**: {str(ctx.guild.verification_level)}\n**Members**: {ctx.guild.member_count}\n**Channels**:\n<:blank:892745849807982632> <:BabatinsRR:893827627406729248> Text channels {len(ctx.guild.text_channels)}\n<:blank:892745849807982632> <:BabatinsRR:893827627406729248> Voice Channels {len(ctx.guild.voice_channels)}\n**Created at**: {ctx.guild.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S')}", color=discord.Colour.dark_theme())
    await ctx.send(embed=embed)



@client.command(pass_context=True)
async def userinfo(ctx, user: discord.Member=None):
    """Displays user information."""
    if not user: # this command took forever to redo for the no user lol
        embed = discord.Embed(title="Your info.", description=f"Username {ctx.author}:\n<:blank:892745849807982632> <:BabatinsRR:893827627406729248> ID {ctx.author.id}\n<:blank:892745849807982632> <:BabatinsRR:893827627406729248> Status: {ctx.author.status}\nHighest role: {ctx.author.top_role}\nRoles: {len(ctx.author.roles)}\nJoined:  {ctx.author.joined_at.__format__('%A, %d. %B %Y @ %H:%M:%S')}\nCreated: {ctx.author.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S')}\nBot?: {ctx.author.bot}", color=discord.Colour.dark_theme())
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(description=f"Username {str(user)}:\n<:blank:892745849807982632> <:BabatinsRR:893827627406729248> ID {user.id}\n<:blank:892745849807982632> <:BabatinsRR:893827627406729248> Status: {user.status}\nHighest role: {user.top_role}\nRoles: {len(user.roles)}\nJoined:  {user.joined_at.__format__('%A, %d. %B %Y @ %H:%M:%S')}\nCreated: {user.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S')}\nBot?: {user.bot}", color=discord.Colour.dark_theme())
        embed.set_thumbnail(url=user.avatar_url)
        embed.set_author(name=str(user), icon_url=user.avatar_url)
        await ctx.send(embed=embed)


@client.command(pass_context=True)
async def av(ctx, user: discord.Member=None):
    """Displays users avatar."""
    if not user:
        embed = discord.Embed(color=0x176cd5)
        embed = discord.Embed(title="View full image.", url=ctx.author.avatar_url, color=0x176cd5)
        embed.set_image(url=ctx.author.avatar_url)
        embed.set_author(name=ctx.author, icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(color=0x176cd5)
        embed = discord.Embed(title="View full image.", url=user.avatar_url, color=0x176cd5)
        embed.set_image(url=user.avatar_url)
        embed.set_author(name=str(user), icon_url=user.avatar_url)
        await ctx.send(embed=embed)




@client.command()
async def help55656565656(ctx):
        embed = discord.Embed(color=discord.Colour.orange()
)
        embed.add_field(name="Help", value="> This bot has a build in anti-raid, anti-nuke and no server advertisement", inline=True)
        embed.add_field(name='Snipe', value="> Snipes the last message deleted\n>s", inline=True)
        embed.add_field(name="User info", value="> Shows a users info\n>userinfo <memeber>", inline=True)
        embed.add_field(name="Server info", value="> Shows the servers info\n>serverinfo", inline=True)
        embed.add_field(name="Avatar", value="> Shows a users avatar \n>av <member>", inline=True)
        embed.add_field(name="Purge", value="> Deletes an amount off specified messages \n >purge <limit> \n Or \n >purge <limit> <member>", inline=False)
        embed.add_field(name="Mute", value="> Mute a member\n>mute <member> <reason>", inline=True)
        embed.add_field(name="Unmute", value="> Unmute a member\n>unmute <member>", inline=True)
        embed.add_field(name="Kick", value="> Kick a member\n>kick <member> <reason>", inline=True)
        embed.add_field(name="Ban", value="> Ban a member\n>ban <member> <reason>", inline=True)
        embed.add_field(name="Unban", value="> Unban a member\n>unban <user-id>", inline=True)
        embed.add_field(name="Slow Mode", value="> Set a slowmode for the chat\n>setdelay <seconds>", inline=True)
        embed.add_field(name="Remove Delay", value="> Remove the delay\n>remove_delay", inline=True)
        embed.add_field(name="Lockdown", value="> Locks the channel down\n>lock", inline=True)
        embed.add_field(name="Unlock", value="> Unlocks the channel\n>unlock", inline=True)
        embed.set_footer(text="If you want to learn more about the anti-raid and the anti-nuke then type >infoAA")
        await ctx.send(embed=embed)
@client.command()
async def help(ctx):
        embed = discord.Embed(title="Help", color=discord.Colour.dark_theme())
        embed.add_field(name='Snipe', value="<:blank:892745849807982632> <:BabatinsRR:893827627406729248> b!s", inline=False)
        embed.add_field(name="User info", value="<:blank:892745849807982632> <:BabatinsRR:893827627406729248> b!userinfo @user", inline=False)
        embed.add_field(name="Server info", value="<:blank:892745849807982632> <:BabatinsRR:893827627406729248> b!serverinfo", inline=False)
        embed.add_field(name="User Avatar", value="<:blank:892745849807982632> <:BabatinsRR:893827627406729248> b!av @user", inline=False)
        embed.add_field(name="Purge Messages", value="<:blank:892745849807982632> <:BabatinsRR:893827627406729248> b!purge 10 @user", inline=False)
        embed.add_field(name="Mute Member", value="<:blank:892745849807982632> <:BabatinsRR:893827627406729248> b!mute @user reason", inline=False)
        embed.add_field(name="Unmute Member", value="<:blank:892745849807982632> <:BabatinsRR:893827627406729248> b!unmute @user", inline=False)
        embed.add_field(name="Kick Member", value="<:blank:892745849807982632> <:BabatinsRR:893827627406729248> b!kick @user reason", inline=False)
        embed.add_field(name="Ban Member", value="<:blank:892745849807982632> <:BabatinsRR:893827627406729248> b!ban @user reason", inline=False)
        embed.add_field(name="Unban Member", value="<:blank:892745849807982632> <:BabatinsRR:893827627406729248> b!unban -UserID-", inline=False)
        embed.add_field(name="Slow Mode", value="<:blank:892745849807982632> <:BabatinsRR:893827627406729248> b!setdelay 5", inline=False)
        embed.add_field(name="Remove Delay", value="<:blank:892745849807982632> <:BabatinsRR:893827627406729248> b!rdelay", inline=False)
        embed.add_field(name="Lock Channel", value="<:blank:892745849807982632> <:BabatinsRR:893827627406729248> b!lock", inline=False)
        embed.add_field(name="Unlock Channel", value="<:blank:892745849807982632> <:BabatinsRR:893827627406729248> b!unlock", inline=False)
        embed.add_field(name="Add/Remove Role", value="<:blank:892745849807982632> <:BabatinsRR:893827627406729248> b!role @user role name", inline=False)
        embed.add_field(name="Membercount", value="<:blank:892745849807982632> <:BabatinsRR:893827627406729248> b!membercount", inline=False)
        embed.add_field(name="Setup Bot", value="<:blank:892745849807982632> <:BabatinsRR:893827627406729248> b!setup", inline=False)
        embed.set_footer(text="If you want to learn more about the anti-raid and the anti-nuke then type b!info")
        await ctx.send(embed=embed)



@client.command()
async def info(ctx):
        msg = discord.Embed(color= discord.Colour.orange())
        msg.add_field(name=" Anti-Raid", value="<:blank:892745849807982632> <:BabatinsRR:893827627406729248> Anti-Spam\n<:blank:892745849807982632> <:BabatinsRR:893827627406729248> Anti-Mention Spam\n<:blank:892745849807982632> <:BabatinsRR:893827627406729248> Anti-Mass Mention\n<:blank:892745849807982632> <:BabatinsRR:893827627406729248> Anti-Wall Spam", inline=False)
        msg.add_field(name=" Anti-Nuke", value="<:blank:892745849807982632> <:BabatinsRR:893827627406729248> Anti-Channel Remove\n<:blank:892745849807982632> <:BabatinsRR:893827627406729248> Anti-Role Remove\n<:blank:892745849807982632> <:BabatinsRR:893827627406729248> Anti-Channel Spam\n<:blank:892745849807982632> <:BabatinsRR:893827627406729248> Anti-Role Spam\n<:blank:892745849807982632> <:BabatinsRR:893827627406729248> Anti-MassBan\n<:blank:892745849807982632> <:BabatinsRR:893827627406729248> Anti-Emoji Spam", inline=False)
        await ctx.send(embed=msg)

import asyncio
import discord
import configs

@client.event
async def on_member_ban(gld, usr):
    await asyncio.sleep(0.5) # wait for audit log
    found_entry = None
    async for entry in gld.audit_logs(limit = 50, action = discord.AuditLogAction.ban, after = datetime.utcnow() - timedelta(seconds = 15), oldest_first = False):
        if entry.created_at < datetime.utcnow() - timedelta(seconds = 10):
            continue
        if entry.target.id == usr.id:
            found_entry = entry
            break
    if not found_entry:
        return
    await post_modlog(guild = gld, type = "BAN", user = found_entry.user, target = usr, reason = found_entry.reason)
@client.event
async def on_member_unban(gld, usr):
    await asyncio.sleep(0.5) # wait for audit log
    found_entry = None
    async for entry in gld.audit_logs(limit = 50, action = discord.AuditLogAction.unban, after = datetime.utcnow() - timedelta(seconds = 15), oldest_first = False):
        if entry.created_at < datetime.utcnow() - timedelta(seconds = 10):
            continue
        if entry.target.id == usr.id:
            found_entry = entry
            break
    if not found_entry:
        return
    await post_modlog(guild = gld, type = "UNBAN", user = found_entry.user, target = usr, reason = found_entry.reason)
@client.event
async def on_member_remove(usr):
    await asyncio.sleep(0.5) # wait for audit log
    found_entry = None
    async for entry in usr.guild.audit_logs(limit = 50, action = discord.AuditLogAction.kick, after = datetime.utcnow() - timedelta(seconds = 10), oldest_first = False): # 10 to prevent join-kick-join-leave false-positives
        if entry.created_at < datetime.utcnow() - timedelta(seconds = 10):
            continue
        if entry.target.id == usr.id:
            found_entry = entry
            break
    if not found_entry:
        return
    await post_modlog(guild = usr.guild, type = "KICK", user = found_entry.user, target = usr, reason = found_entry.reason)
@client.event
async def on_member_update(before, after):
    if before.roles == after.roles:
        return
    muted_role = discord.utils.get(after.guild.roles, name = configs.MUTED_ROLE_NAME)
    if not muted_role:
        return
    if muted_role in after.roles and not muted_role in before.roles:
        if after.joined_at > (datetime.utcnow() - timedelta(seconds = 10)): # join persist mute
            return
        await asyncio.sleep(0.5) # wait for audit log
        found_entry = None
        async for entry in after.guild.audit_logs(limit = 50, action = discord.AuditLogAction.member_role_update, after = datetime.utcnow() - timedelta(seconds = 15), oldest_first = False):
            if entry.created_at < datetime.utcnow() - timedelta(seconds = 10):
                continue
            if entry.target.id == after.id and not muted_role in entry.before.roles and muted_role in entry.after.roles:
                found_entry = entry
                break
        if not found_entry:
            return
        await post_modlog(guild = after.guild, type = "MUTE", user = found_entry.user, target = after, reason = found_entry.reason)
    elif muted_role not in after.roles and muted_role in before.roles:
        if after.joined_at > (datetime.utcnow() - timedelta(seconds = 10)): # join persist unmute
            return
        await asyncio.sleep(0.5) # wait for audit log
        found_entry = None
        async for entry in after.guild.audit_logs(limit = 50, action = discord.AuditLogAction.member_role_update, after = datetime.utcnow() - timedelta(seconds = 15), oldest_first = False):
            if entry.created_at < datetime.utcnow() - timedelta(seconds = 10):
                continue
            if entry.target.id == after.id and muted_role in entry.before.roles and not muted_role in entry.after.roles:
                found_entry = entry
                break
        if not found_entry:
            return
        await post_modlog(guild = after.guild, type = "UNMUTE", user = found_entry.user, target = after, reason = found_entry.reason)
@client.event
async def on_member_update(before, after):
        if before.display_name != after.display_name:
                embed = Embed(title="Nickname change",
                colour=after.colour,
                timestamp=datetime.utcnow())
                fields = [("Before", before.display_name, False),
                          ("After", after.display_name, False)]
                for name, value, inline in fields:
                        embed.add_field(name=name, value=value, inline=inline)
                embed.set_author(name=str(after), icon_url=after.avatar_url)
                await post_modlogg(embed=embed, guild = after.guild)
        elif before.roles != after.roles:
                embed = Embed(title="Role Update",
                colour=after.colour,
                timestamp=datetime.utcnow())
                fields = [
                        ("Role: ", " ".join([r.mention for r in after.roles]), False)]
                for name, value, inline in fields:
                        embed.add_field(name=name, value=value, inline=inline)
                embed.set_author(name=str(after), icon_url=after.avatar_url)
                await post_modlogg(embed=embed, guild = after.guild)
        
@client.event
async def on_message_edit(before, after):
        if not after.author.bot:
                if before.content != after.content:
                        embed = Embed(title="Message edit",
                        colour=after.author.colour,
                        timestamp=datetime.utcnow())
                        fields = [("Before", before.content, False),
                                  ("After", after.content, False)]
                        for name, value, inline in fields:
                                embed.add_field(name=name, value=value, inline=inline)
                        embed.set_author(name=str(after.author), icon_url=after.author.avatar_url)
                        await post_modlogg(embed=embed, guild = after.guild)
@client.event
async def on_user_update(before, after):
        if before.discriminator != after.discriminator:
                embed = Embed(title="Discriminator change",
                colour=after.colour,timestamp=datetime.utcnow())
                fields = [("Before", before.discriminator, False),
                ("After", after.discriminator, False)]
                for name, value, inline in fields:
                        embed.add_field(name=name, value=value, inline=inline)
                embed.set_author(name=str(after), icon_url=after.avatar_url)
                await post_modlogg(embed=embed, guild = after.guild)
        
async def post_modlog(guild, type, user, target, reason):
    mod_log_channel = discord.utils.get(guild.text_channels, name = configs.MOD_LOG_CHANNEL_NAME)
    if not mod_log_channel:
        return
    caseid = "1"
    async for s in mod_log_channel.history(limit = 100):
        if s.author.id != client.user.id:
            continue
        if not s.embeds:
            continue
    e = discord.Embed(color = configs.MODLOG_COLORS[type], timestamp = datetime.utcnow())
    e.set_author(name = f"{type.capitalize()}")
    e.add_field(name = "Target", value = f"<@{str(target.id)}> ({str(target)})", inline = True)
    e.add_field(name = "Moderator", value = f"<@{str(user.id)}> ({str(user)})", inline = True)
    e.add_field(name = "Reason", value = reason if reason else f"{reason}", inline = False)
    await mod_log_channel.send(embed = e)
async def post_modlogg(embed, guild):
    em = embed
    mod_log_channel = discord.utils.get(guild.text_channels, name = configs.MOD_LOG_CHANNEL_NAME)
    if not mod_log_channel:
        return
    await mod_log_channel.send(embed=em)

async def post_modloggg(embed, guild):
    em = embed
    mod_log_channel = discord.utils.get(guild.text_channels, name = configs.MOD_LOG_CHANNEL_NAME)
    if not mod_log_channel:
        return
    await mod_log_channel.send(embed=em)
async def postshit(ctx, embed):
    em = embed
    mod_log_channel = discord.utils.get(ctx.guild.text_channels, name = configs.MOD_LOG_CHANNEL_NAME)
    if not mod_log_channel:
        return
    await mod_log_channel.send(embed=em)
async def edit_reason(msg):
    await msg.delete()
    pmsg = msg.content.replace(".reason ", "")
    if not " " in pmsg:
        return
    caseid = pmsg.split(" ")[0]
    if not caseid.isdigit():
        return
    new_reason = " ".join(pmsg.split(" ")[1:])
    fnd_msg = None
    async for s in msg.channel.history(limit = 500):
        if s.author.id != client.user.id:
            continue
        if not s.embeds:
            continue
        if s.embeds[0].author.name.endswith(f" | Case {caseid}"):
            fnd_msg = s
            break
    if not fnd_msg:
        return
    fnd_em = fnd_msg.embeds[0]
    fnd_em.set_field_at(2, name = "Reason", value = new_reason, inline = False)
    await fnd_msg.edit(embed = fnd_em)
@client.command(pass_context=True)
async def setup(ctx):
        if ctx.author.guild_permissions.administrator:
                msg1 = discord.Embed(title="Setting Up", description="<:babatinS:892818123374329977> Starting setup", color= discord.Colour.orange())
                message = await ctx.channel.send(embed=msg1)
                await asyncio.sleep(1)
                msg2 = discord.Embed(title="Setting Up", description="<:babatinS:892818123374329977> Starting setup\n<:babatinS:892818123374329977> Checking if there is a muted role", color= discord.Colour.orange())
                await message.edit(embed=msg2)
                guild = ctx.guild
                mutedRole = discord.utils.get(guild.roles, name="Muted")
                if not mutedRole:
                        await asyncio.sleep(1)
                        msg2 = discord.Embed(title="Setting Up", description="<:babatinS:892818123374329977> Starting setup\n<:babatinS:892818123374329977> Checking if there is a muted role\n<:blank:892745849807982632> <:BabatinsRR:893827627406729248> No muted role was found\n<:babatinS:892818123374329977> Creating muted role", color= discord.Colour.orange())
                        await message.edit(embed=msg2)
                        mutedRole = await guild.create_role(name="Muted")
                        for channel in guild.channels:
                                await channel.set_permissions(mutedRole, speak=False, send_messages=False)
                        await asyncio.sleep(1)
                        msg2 = discord.Embed(title="Setting Up", description="<:babatinS:892818123374329977> Starting setup\n<:babatinS:892818123374329977> Checking if there is a muted role\n<:blank:892745849807982632> <:BabatinsRR:893827627406729248> No muted role was found\n<:babatinS:892818123374329977> Creating muted role\n<:babatinS:892818123374329977> Checking if there is a logging channel", color= discord.Colour.orange())
                        await message.edit(embed=msg2)
                        for channel in ctx.guild.channels:
                                if channel.name == "babatin-logs":
                                        await asyncio.sleep(1)
                                        msg2 = discord.Embed(title="Setting Up", description="<:babatinS:892818123374329977> Starting setup\n<:babatinS:892818123374329977> Checking if there is a muted role\n<:blank:892745849807982632> <:BabatinsRR:893827627406729248> No muted role was found\n<:babatinS:892818123374329977> Creating muted role\n<:babatinS:892818123374329977> Checking if there is a logging channel\n<:babatinS:892818123374329977> A logging channel has been found", color= discord.Colour.orange())
                                        await message.edit(embed=msg2)
                                else:
                                        await asyncio.sleep(1)
                                        msg2 = discord.Embed(title="Setting Up", description="<:babatinS:892818123374329977> Starting setup\n<:babatinS:892818123374329977> Checking if there is a muted role\n<:blank:892745849807982632> <:BabatinsRR:893827627406729248> No muted role was found\n<:babatinS:892818123374329977> Creating muted role\n<:babatinS:892818123374329977> Checking if there is a logging channel\n<:blank:892745849807982632> <:BabatinsRR:893827627406729248> No logging channel has been found creating one", color= discord.Colour.orange())
                                        await message.edit(embed=msg2)
                                        guild = ctx.guild
                                        member = ctx.author
                                        overwrites = {
                                                 guild.default_role: discord.PermissionOverwrite(read_messages=False),
                                                 member: discord.PermissionOverwrite(read_messages=True)
                                                 }
                                        channel = await guild.create_text_channel('babatin-logs', overwrites=overwrites)
                                        await asyncio.sleep(1)
                                        msg2 = discord.Embed(title="Setting Up", description="<:babatinS:892818123374329977> Starting setup\n<:babatinS:892818123374329977> Checking if there is a muted role\n<:blank:892745849807982632> <:BabatinsRR:893827627406729248> No muted role was found\n<:babatinS:892818123374329977> Creating muted role\n<:babatinS:892818123374329977> Checking if there is a logging channel\n<:blank:892745849807982632> <:BabatinsRR:893827627406729248> No logging channel has been found creating one\n<:babatinS:892818123374329977> BaBaTin bot has been setup", color= discord.Colour.orange())
                                        await message.edit(embed=msg2)
                                        await asyncio.sleep(2)
                                        msg = discord.Embed(title="Note", description="Dont change the name off the logging channel or else you wont be reciving logs")
                                        await ctx.send(embed=msg)
                                        return
                else:
                        await asyncio.sleep(1)
                        msg2 = discord.Embed(title="Setting Up", description="<:babatinS:892818123374329977> Starting setup\n<:babatinS:892818123374329977> Checking if there is a muted role\n<:babatinS:892818123374329977> A muted role has been found", color= discord.Colour.orange())
                        await message.edit(embed=msg2)
                        await asyncio.sleep(1)
                        msg2 = discord.Embed(title="Setting Up", description="<:babatinS:892818123374329977> Starting setup\n<:babatinS:892818123374329977> Checking if there is a muted role\n<:babatinS:892818123374329977> A muted role has been found\n<:babatinS:892818123374329977> Checking if there is a logging channel", color= discord.Colour.orange())
                        await message.edit(embed=msg2)
                        channel = discord.utils.get(ctx.guild.text_channels, name="babatin-logs")
                        if not channel:
                                await asyncio.sleep(1)
                                msg2 = discord.Embed(title="Setting Up", description="<:babatinS:892818123374329977> Starting setup\n<:babatinS:892818123374329977> Checking if there is a muted role\n<:babatinS:892818123374329977> A muted role has been found\n<:babatinS:892818123374329977> Checking if there is a logging channel\n<:blank:892745849807982632> <:BabatinsRR:893827627406729248> No logging channel has been found creating one", color= discord.Colour.orange())
                                await message.edit(embed=msg2)
                                guild = ctx.guild
                                member = ctx.author
                                overwrites = {
                                        guild.default_role: discord.PermissionOverwrite(read_messages=False),
                                        member: discord.PermissionOverwrite(read_messages=True)
                                }
                                channel = await guild.create_text_channel('babatin-logs', overwrites=overwrites)
                                await asyncio.sleep(1)
                                msg2 = discord.Embed(title="Setting Up", description="<:babatinS:892818123374329977> Starting setup\n<:babatinS:892818123374329977> Checking if there is a muted role\n<:babatinS:892818123374329977> A muted role has been found\n<:babatinS:892818123374329977> Checking if there is a logging channel\n<:blank:892745849807982632> <:BabatinsRR:893827627406729248> No logging channel has been found creating one\n<:babatinS:892818123374329977> BaBaTin bot has been setup", color= discord.Colour.orange())
                                await message.edit(embed=msg2)
                                await asyncio.sleep(2)
                                msg = discord.Embed(title="Note", description="Dont change the name off the logging channel or else you wont be reciving logs")
                                await ctx.send(embed=msg)
                                return
                        else:
                                await asyncio.sleep(1)
                                msg2 = discord.Embed(title="Setting Up", description="<:babatinS:892818123374329977> Starting setup\n<:babatinS:892818123374329977> Checking if there is a muted role\n<:babatinS:892818123374329977> A muted role has been found\n<:babatinS:892818123374329977> Checking if there is a logging channel\n<:babatinS:892818123374329977> A logging channel has been found\n<:babatinS:892818123374329977> BaBaTIN bot has been set", color= discord.Colour.orange())
                                await message.edit(embed=msg2)
                                await asyncio.sleep(2)
                                msg = discord.Embed(title="Note", description="Dont change the name off the logging channel or else you wont be reciving logs")
                                await ctx.send(embed=msg)
                                return
        else:
                await ctx.channel.send(f"**:x: | {ctx.author.mention} Sorry you dont have permission to use this command**")
                return
        
   
client.load_extension('cogs.litsening')
client.load_extension('cogs.MassMentionMessage')
client.load_extension('cogs.MassMentionMute')
client.load_extension('cogs.WallSpamMessage')
client.load_extension('cogs.WallSpamMute')
client.load_extension('cogs.SpamMentionMute')
client.load_extension('cogs.SpamMentionMessage')
keep_alive.keep_alive()              
client.run(os.getenv('TOKEN'))