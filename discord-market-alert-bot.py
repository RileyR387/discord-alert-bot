#!/usr/bin/env python3

import sys
import os
import argparse
import discord

# Local config loader package - unpublished
from config.simple import AutoLoad

# Local Bot
from bot.service import DiscordAlertBot

opts = argparse.ArgumentParser(
    description="Configurable discord alert bot"
)

opts.add_argument('-c', '--config', type=str, metavar="./some-config.yaml", help='Use config file <CONFIG>')
opts.add_argument('-a', '--messageAll', type=str, metavar="TEST Message to all channels", help='Send a test message to all channels.')

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
    await bot.Run()

@client.event
async def on_message(message):
    await bot.ProcessMessage(message)

client.run(conf["discord"]["token"])

sys.exit(bot.Stop())

