from datetime import datetime
import asyncio
from discord import Embed
from discord.ext.commands import Cog
from discord.ext.commands import command
from datetime import datetime, timedelta
import discord

time_window_milliseconds = 5000
max_msg_per_window = 5
author_msg_times = {}


class Log(Cog):
	def __init__(self, bot):
		self.bot = bot

	@Cog.listener()
	async def on_ready(self):
		print('anti-raidMessage')

	@Cog.listener()
	async def on_message(self, ctx):
		global author_msg_counts
		author_id = ctx.author.id
		curr_time = datetime.now().timestamp() * 1000
		if not author_msg_times.get(author_id, False):
			author_msg_times[author_id] = []
		author_msg_times[author_id].append(curr_time)
		expr_time = curr_time - time_window_milliseconds
		expired_msgs = [
		    msg_time for msg_time in author_msg_times[author_id]
		    if msg_time < expr_time
		]

		# Remove all the expired messages times from our list
		for msg_time in expired_msgs:
			author_msg_times[author_id].remove(msg_time)
		if len(author_msg_times[author_id]) > max_msg_per_window:
			if ctx.author.guild_permissions.manage_messages:
				return
			guild = ctx.guild
			mutedRole = discord.utils.get(guild.roles, name="Muted")
			msg = Embed(
			    title="Auto-Moderation",
			    description=
			    f"**{ctx.author.mention} has been muted for 5 minutes\n<:blank:892745849807982632> <:BabatinsRR:893827627406729248> Reason: Spamming**",
			    color=discord.Colour.orange())
			msg.set_footer(text=f"{str(ctx.author)} | {ctx.author.id}")
			await ctx.channel.send(embed=msg)
			await ctx.channel.purge(
			    after=datetime.now() - timedelta(minutes=3),
			    check=lambda x: x.author.id == ctx.author.id,
			    oldest_first=False)
			await asyncio.sleep(300)
			await ctx.author.remove_roles(mutedRole)
			mssg = Embed(title="Auto-Moderation",
			             description=f"{ctx.author.mention} has been unmuted",
			             color=discord.Colour.orange())
			mssg.set_footer(text=f"{str(ctx.author)} | {ctx.author.id}")
			await ctx.channel.send(embed=mssg)
			return


def setup(bot):
	bot.add_cog(Log(bot))