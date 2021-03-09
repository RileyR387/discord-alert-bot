
import os
import sys
import discord
import datetime
import schedule
import time
import asyncio
import threading

# Plugin loading libs
import importlib

from .util import ListGuilds
from .msgprocessor import ProcessMessage

class DiscordAlertBot:
    def __init__(self, client, config, plugins, args):
        self.client = client
        self.config = config
        self.pluginNames = plugins
        self.plugins = []
        self.args = args
        self.guilds = []

        self.stopChannel = threading.Event()
        self.schedule = schedule

        if not self.args.listGuilds:
            self.InitPlugins()
            self.InitSchedule()

        if self.args.test:
            self._testDailyJob()

    async def RunArgs(self):

        await self.cacheGuilds()

        if self.args.listGuilds:
            await self.ListGuilds()
            await self.client.close()
            return

        if self.args.messageAll is not None:
            await self.Broadcast(self.args.messageAll)
            await self.client.close()
            return

        if self.args.message is not None:
            channelId = self._defaultChannelId()
            if self.args.channelId is not None:
                channelId = self.args.channelId
            if channelId is not None:
                await self.MessageChannel(int(channelId), self.args.message)
            else:
                print("Please provide a channelId for message option.")
            await self.client.close()
            return

        await self.RunPlugins()
        return

    def InitPlugins(self):
        for plugin in self.pluginNames:
            self._loadPlugin( plugin )

    def _getPlugin(self, plugName):
        for plugin in self.plugins:
            if plugin["name"] == plugName:
                return plugin
        return None

    def _loadPlugin(self, pluginName):
        plug = self._getPlugin(pluginName)
        if plug is not None:
            return plug

        pluginLib = None
        try:
            if '.' not in pluginName:
                pluginLib = importlib.import_module('plugins.' + pluginName)
            else:
                # Maybe this will support external plugins?
                pluginLib = importlib.import_module(pluginName)
        except ModuleNotFoundError as x:
            print("Failed to load plugin({}): {}".format(pluginName, x))
            return None

        plug = {
            'name': pluginName,
            'runtime': pluginLib.BotPlugin(self._pluginMsgCallback),
        }
        print( "Loaded plugin: %s" % pluginName )
        self.plugins.append( plug )
        return plug


    async def RunPlugins(self):
        for plugin in self.plugins:
            asyncio.get_event_loop().create_task(
                plugin['runtime'].Run()
            )
            print("Running plugin: " + plugin['name'])

    async def RunSchedule(self):
        self.stopChannel.clear()
        await self._schedLoopAsync()

    async def _schedLoopAsync(self):
        while not self.stopChannel.is_set():
            self.schedule.run_pending()
            await asyncio.sleep(0.9)
        return

    def Stop(self):
        self.stopChannel.set()
        for plugin in self.plugins:
            plugin['runtime'].Stop()

    def InitSchedule(self):
        alerts = self.config["alerts"]["daily"]
        channelIds = self._getChannelIds()
        for alert in alerts:
            for alertDay in alert["days"]:
                for channelId in channelIds:
                    if "msg" in alert.keys():
                        job = ThreadedAlertJob( self.QueueMessage, channelId, alert["msg"] )
                        getattr(self.schedule.every(), alertDay).at(alert["time"]).do(job.Run)
                    if "plugin" in alert.keys():
                        plugin = self._loadPlugin(alert["plugin"])
                        if plugin is not None:
                            getattr(self.schedule.every(), alertDay).at(alert["time"]).do(plugin['runtime'].Job)

    def _pluginMsgCallback(self, msgOps):
        if isinstance(msgOps, str):
            self.QueueMessage( self._defaultChannelId(), msgOps )
        elif isinstance(msgOps, dict):
            msgKeys = msgOps.keys()
            if 'msg' not in msgKeys:
                self.QueueMessage( self._defaultChannelId(), msgOps )
                return

            if 'BROADCAST' in msgKeys and msgOps['BROADCAST']:
                self._pluginBroadcast(msgOps['msg'])

            if 'channelid' in msgKeys:
                self.QueueMessage( msgOps['channelid'], msgOps['msg'] )

            if 'channelids' in msgKeys:
                for chanID in msgOps['channelids']:
                    self.QueueMessage( chanID, msgOps['msg'] )

    def _pluginBroadcast(self, msg):
        for g in self.guilds:
            if g['channelType'] == discord.ChannelType.text:
                self.QueueMessage( g['channelID'], msg )


    def QueueMessage(self, channelId, msg):
        asyncio.get_event_loop().create_task(
            self.MessageChannel(channelId, msg)
        )

    async def MessageChannel(self, channelId, msg):
        await self.client.wait_until_ready()
        channel = self.client.get_channel(channelId)
        if channel is None or channel.type != discord.ChannelType.text:
            print("ChannelId: {} is not a text channel or does not exists for writing.".format(channelId))

        if isinstance(msg, str):
            print("Messaging channel: {} with text: {}".format(channelId,msg))
            await channel.send(msg)
        elif isinstance(msg, dict):
            if msg['type'] == "rich":
                richMsg = discord.Embed(**msg)
                await channel.send(embed=richMsg)
            else:
                print("Unknow non-text message type: {}".format( msg['type'] ))

    async def cacheGuilds(self):
        await self.client.wait_until_ready()
        for guild in self.client.guilds:
            for channel in guild.channels:
                self.guilds.append({
                    "server": guild.name,
                    "channelName": channel.name,
                    "channelID": channel.id,
                    "channelType": channel.type
                })

    async def Broadcast(self, msg):
        await self.client.wait_until_ready()
        guilds = self.client.guilds
        for guild in guilds:
            for channel in guild.channels:
                print("Assessing Channel({}): {}".format(channel.type, channel.name))
                if channel.type == discord.ChannelType.text:
                    print(
                        "Alerting Channel - ID: \"{}\", Name: \"{}\", Type: \"{}\""
                        .format(channel.id, channel.name, channel.type)
                    )
                    await channel.send(msg)

    async def ListGuilds(self):
        ListGuilds(self.guilds)

    async def ProcessMessage(self, message):
        if message.author == self.client.user:
            return

        await ProcessMessage(message)

        for plugin in self.plugins:
            await plugin['runtime'].ProcessMessage(message)

    def _getChannelIds(self):
        if "channelIds" in self.config["alerts"]:
            return self.config["alerts"]["channelIds"]
        else:
            return [self._defaultChannelId()]

    def _defaultChannelId(self):
        default = None
        # if alert channels are configured, attempt to use the first one in case a default isn't set
        if "channelIds" in self.config["alerts"]:
            default = self.config["alerts"]["channelIds"][0]

        if "defaultChannelId" in self.config:
            default = self.config["defaultChannelId"]
        res = os.getenv("DISCORD_DEFAULT_CHANNELID", default=default)
        if res is None:
            print("Please set DISCORD_DEFAULT_CHANNELID in environment or defaultChannelId in config")
            sys.exit(1)
        return res

    def _testDailyJob(self):
        time = datetime.datetime.now
        dow = time().strftime("%A").lower()
        t_hr = time().hour
        t_min = time().minute
        t_min += 1
        if t_min >= 60: t_min = 0; t_hr += 1;
        if t_hr >= 24: t_hr = 0;
        t = ("%02d" % t_hr) + ":" + ("%02d" % t_min)
        print("Using test time of: " + dow + " " + t)
        job1 = ThreadedAlertJob( self.QueueMessage, self._defaultChannelId(), "Test Message 1" )
        job2 = ThreadedAlertJob( self.QueueMessage, self._defaultChannelId(), "Test Message 2" )
        getattr(self.schedule.every(), dow).at(t).do(job1.Run)
        getattr(self.schedule.every(), dow).at(t).do(job2.Run)

class ThreadedAlertJob:
    def __init__(self, messageFunc, channelId, message):
        self.messageFunc = messageFunc
        self.message = message
        self.channelId = channelId

    def Run(self):
        alertThread = threading.Thread(target=self._run())
        alertThread.start()

    def _run(self):
        self.messageFunc( self.channelId, self.message )

