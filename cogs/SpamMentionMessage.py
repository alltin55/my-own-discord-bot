from datetime import datetime
import asyncio
from discord import Embed
from discord.ext.commands import Cog
from discord.ext.commands import command
from datetime import datetime, timedelta
import discord

lag = ["<@"]


class Log(Cog):
	def __init__(self, bot):
		self.bot = bot

	@Cog.listener()
	async def on_ready(self):
		print('anti-SpamMention-MuteMessage')

	@Cog.listener()
	async def on_message(self, message):
		def _check(m):
			return (m.author == message.author and len(m.mentions)
			        and (datetime.utcnow() - m.created_at).seconds < 10)

		if not message.author.bot:
			if len(list(filter(lambda m: _check(m),
			                   self.bot.cached_messages))) >= 4:
                                           if message.author.guild_permissions.manage_messages:
                                                   return
                                           msg = discord.Embed(
                                                        title="Auto-Moderation",
                                                        description=
                                                        f"{message.author.mention} has been muted for 2 minutes\n<:blank:892745849807982632> <:BabatinsRR:893827627406729248> Reason: Mention-Spam",
                                                        color=discord.Colour.orange()
                                                        )
                                           msg.set_footer(text=f"{str(message.author)} | {message.author.id}")
                                           await message.channel.send(embed=msg)
                                           await asyncio.sleep(122)
                                           msg = discord.Embed(
                                                title="Auto-Moderation",
                                                description=f"{message.author.mention} has been unmuted",
                                                color=discord.Colour.orange())
                                           await message.channel.send(embed=msg)


def setup(bot):
	bot.add_cog(Log(bot))