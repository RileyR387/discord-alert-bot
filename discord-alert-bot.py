#!/usr/bin/env python3

import sys
import os
import argparse
import discord

# Plugin loading libs
import importlib
import pkgutil

# Local config loader package - unpublished
from config.simple import AutoLoad, LoadConfig

# Local Bot
from bot.service import DiscordAlertBot

opts = argparse.ArgumentParser(
    description="Configurable discord alert bot"
)

opts.add_argument('-c', '--config', type=str, metavar="conf.yaml", help="Specify single config file")
opts.add_argument('-a', '--messageAll', type=str, metavar="msgText", help="Send a test message to all channels.")
opts.add_argument('-m', '--message', type=str, metavar="msgText", help="Message a single channel, requires `-i`")
opts.add_argument('-i', '--channelId', type=str, metavar="123456...", help="ChannelID to use with `--message`")
opts.add_argument('-l', '--listGuilds', action="store_true", help="List all channels and their unique id's")
opts.add_argument('-p', '--plugins', type=str, nargs="+", default='', help="Plugins to enable")
opts.add_argument('-t', '--test', action="store_true", help="Send test message every 10 seconds")
#opts.add_argument('-s', '--service', action="store_true", help="Run as service, don't terminate")

args = opts.parse_args()

conf={}

if args.config:
    conf = LoadConfig( args.config )
else:
    conf = AutoLoad(__file__)

## Verify we have a token
token = None
if "discordBotToken" in conf:
   token = conf["discordBotToken"]
token = os.getenv('DISCORD_BOT_TOKEN', default=token)
if token is None:
    print("Please set DISCORD_BOT_TOKEN in environment or discordBotToken in config")
    sys.exit(1)

## Load Plugins
def iter_namespace(ns_pkg):
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")

plugins = {}
if len(args.plugins) != 0:
    plugins = {
        name: importlib.import_module('plugins.' + name)
            for name in args.plugins
    }

## Create Client
client = discord.Client()
bot    = DiscordAlertBot(client, conf, plugins, args)

## Client Handlers
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    await bot.RunArgs()

@client.event
async def on_message(message):
    await bot.ProcessMessage(message)

async def RunBotLoop():
    await client.wait_until_ready()
    await bot.RunSchedule()

## Default to alert service if not given a specific operation
if not args.messageAll and not args.message and not args.listGuilds:
    client.loop.create_task(RunBotLoop())

client.run(token)

sys.exit(bot.Stop())

