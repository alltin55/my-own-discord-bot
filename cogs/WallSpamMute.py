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
		print('Anti-Wall SpamMute')

	@Cog.listener()
	async def on_message(self, message):
                if len(message.content) > 900:
                        if message.author.guild_permissions.manage_messages:
                                return
                        guild = message.guild
                        mutedRole = discord.utils.get(guild.roles, name="Muted")
                        try:
                                await message.author.add_roles(mutedRole)
                                for channel in guild.channels:
                                        await channel.set_permissions(mutedRole, speak=False, send_messages=False)
                        except:
                                mutedRole = await guild.create_role(name="Muted")
                                for channel in guild.channels:
                                        await channel.set_permissions(mutedRole, speak=False, send_messages=False)
                                        await message.author.add_roles(mutedRole)
                        await message.channel.purge(
			    after=datetime.now() - timedelta(minutes=3),
			    check=lambda x: x.author.id == message.author.id,
			    oldest_first=False)
                        await asyncio.sleep(120)
                        await message.author.remove_roles(mutedRole)
                        

def setup(bot):
	bot.add_cog(Log(bot))
