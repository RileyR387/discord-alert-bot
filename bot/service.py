
import os
import sys
import discord
import datetime
import schedule
import time
import asyncio
import threading

from .util import ListGuilds

class DiscordAlertBot:
    def __init__(self, client, config, args):
        self.client = client
        self.config = config
        self.args = args

        self.stopChannel = threading.Event()
        self.schedule = schedule

        if not self.args.listGuilds:
            self.InitSchedule()

        if self.args.test:
            self.schedule.every(10).seconds.do(self.QueueMessage, channelId=self._defaultChannelId(), msg="Test Message")

    async def RunArgs(self):
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

        return

    async def RunSchedule(self):
        self.stopChannel.clear()
        await self._schedLoopAsync()

    async def _schedLoopAsync(self):
        while not self.stopChannel.is_set():
            self.schedule.run_pending()
            await asyncio.sleep(1)
        return

    def Stop(self):
        self.stopChannel.set()
        None

    def InitSchedule(self):
        alerts = self.config["alerts"]["daily"]
        channelIds = self._getChannelIds()
        for alertTime, opts in alerts.items():
            msg = opts["msg"]
            for alertDay in opts["days"]:
                for channelId in channelIds:
                    getattr(self.schedule.every(), alertDay).at(alertTime).do(self.QueueMessage, channelId=channelId, msg=msg)

    def QueueMessage(self, channelId, msg):
        asyncio.get_event_loop().create_task(
            self.MessageChannel(channelId, msg)
        )

    async def MessageChannel(self, channelId, msg):
        print("Messaging channel: {} with text: {}".format(channelId,msg))
        await self.client.wait_until_ready()
        channel = self.client.get_channel(channelId)
        if channel is not None and channel.type == discord.ChannelType.text:
            await channel.send(msg)
        else:
            # TODO: Log instead?
            print("ChannelId: {} is not a text channel or does not exists for writing.".format(channelId))

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
        await self.client.wait_until_ready()
        for guild in self.client.guilds:
            for channel in guild.channels:
                print(
                    "Available Channel - ID: \"{}\", Name: \"{}\", Type: \"{}\""
                    .format(channel.id, channel.name, channel.type)
                )

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

