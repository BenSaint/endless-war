#!/usr/bin/python3
#
# endless-war
# mperron (2018)
#
# a chat bot for the RFCK discord server

import discord
import asyncio
import random

client = discord.Client()

@client.event
async def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('------')

@client.event
async def on_message(message):
	# Wake up when we see a message start with pound.
	if message.content.startswith('#'):
		""" let the user know we're working on it """
		resp = await client.send_message(message.channel, '...')

		""" tokenize the message. the command should be the first word. """
		tokens = message.content.split(' ')
		cmd = tokens[0].lower()
		tokens_count = len(tokens)

		""" process command words """
		if cmd == '#kill':
			if tokens_count > 1:
				await client.edit_message(resp, 'Okay, let\'s kill {}!' . format(tokens[1]))
			else:
				await client.edit_message(resp, 'Okay tough guy, who are you killing?')

		else:
			""" couldn't process the command. bail out!! """

			""" bot rule 0: be cute """
			randint = random.randint(1,3)
			msg_mistake = "oh, sorry"
			if randint == 2:
				msg_mistake = "whoops"
			elif randint == 3:
				msg_mistake = "nevermind"

			await asyncio.sleep(1)
			await client.edit_message(resp, msg_mistake)
			await asyncio.sleep(2)
			await client.delete_message(resp)

""" find our REST API token """ 
token = ""
f_token = open("token", "r")
f_token_lines = f_token.readlines()

for line in f_token_lines:
	line = line.rstrip()
	if len(line) > 0:
		token = line

f_token.close()

# connect to discord and run indefinitely
client.run(token)
