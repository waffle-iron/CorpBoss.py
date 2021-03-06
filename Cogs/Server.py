import asyncio
import discord
import requests
import string
from   discord.ext import commands
from   Cogs import Settings
from   Cogs import Message
from   Cogs import Nullify

# This module sets/gets some server info

class Server:

	# Init with the bot reference, and a reference to the settings var and xp var
	def __init__(self, bot, settings):
		self.bot = bot
		self.settings = settings

	@commands.command(pass_context=True)
	async def setinfo(self, ctx, *, word : str = None):
		"""Sets the server info (admin only)."""

		# Check for admin status
		isAdmin = ctx.message.author.permissions_in(ctx.message.channel).administrator
		if not isAdmin:
			checkAdmin = self.settings.getServerStat(ctx.message.server, "AdminArray")
			for role in ctx.message.author.roles:
				for aRole in checkAdmin:
					# Get the role that corresponds to the id
					if aRole['ID'] == role.id:
						isAdmin = True
		# Only allow admins to change server stats
		if not isAdmin:
			await self.bot.send_message(ctx.message.channel, 'You do not have sufficient privileges to access this command.')
			return

		# We're admin
		if not word:
			self.settings.setServerStat(ctx.message.server, "Info", None)
			msg = 'Server info *removed*.'
		else:
			self.settings.setServerStat(ctx.message.server, "Info", word)
			msg = 'Server info *updated*.'

		await self.bot.send_message(ctx.message.channel, msg)

	@commands.command(pass_context=True)
	async def info(self, ctx):
		"""Displays the server info if any."""

		# Check if we're suppressing @here and @everyone mentions
		if self.settings.getServerStat(ctx.message.server, "SuppressMentions").lower() == "yes":
			suppress = True
		else:
			suppress = False

		serverInfo = self.settings.getServerStat(ctx.message.server, "Info")
		msg = 'I have no info on *{}* yet.'.format(ctx.message.server.name)
		if serverInfo:
			msg = '*{}*:\n\n{}'.format(ctx.message.server.name, serverInfo)

		# Check for suppress
		if suppress:
			msg = Nullify.clean(msg)

		await self.bot.send_message(ctx.message.channel, msg)