#!/usr/bin/env python3

import sys
import os
import argparse
import discord

# Local config loader package - unpublished
from config.simple import AutoLoad

# Local Bot
from bot.service import DiscordAlertBot
from bot.msgprocessor import ProcessMessage

opts = argparse.ArgumentParser(
    description="Configurable discord alert bot"
)

opts.add_argument('-c', '--config', type=str, metavar="conf.yaml", help="Specify single config file")
opts.add_argument('-a', '--messageAll', type=str, metavar="msgText", help="Send a test message to all channels.")
opts.add_argument('-m', '--message', type=str, metavar="msgText", help="Message a single channel, requires `-i`")
opts.add_argument('-i', '--channelId', type=str, metavar="123456...", help="ChannelID to use with `--message`")
opts.add_argument('-l', '--listGuilds', action="store_true", help="List all channels and their unique id's")
#opts.add_argument('-s', '--service', action="store_true", help="Run as service, don't terminate")

args = opts.parse_args()

conf={}

if args.config:
    conf = LoadConfig( args.config )
else:
    conf = AutoLoad(__file__)

client = discord.Client()
bot    = DiscordAlertBot(client, conf, args)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await bot.RunArgs()

@client.event
async def on_message(message):
    await ProcessMessage(client, message)

async def RunBotLoop():
    await client.wait_until_ready()
    await bot.RunSchedule()

if not args.messageAll and not args.message and not args.listGuilds:
    client.loop.create_task(RunBotLoop())

token = ""
if "discordBotToken" in conf:
   token = conf["discordBotToken"]

client.run(os.getenv('DISCORD_BOT_TOKEN', default=token))

sys.exit(bot.Stop())

