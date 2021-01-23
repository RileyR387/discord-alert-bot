
import os
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

        self.schedule = schedule
        self.InitSchedule()
        self.stopChannel = threading.Event()

        self.schedule.every(10).seconds.do(self.QueueMessage, channelId=660676159259934723, msg="Test Message")

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
        #self.SpawnService()
        self.stopChannel.clear()
        await self._schedLoopAsync()
        #self.schedule.run_pending()


    def _schedLoop(self):
        while not self.stopChannel.is_set():
            self.schedule.run_pending()
            print("Scheduler Running")
            time.sleep(1)
            #await asyncio.sleep(1)

    async def _schedLoopAsync(self):
        while not self.stopChannel.is_set():
            self.schedule.run_pending()
            print("Scheduler Running")
            await asyncio.sleep(1)

    def SpawnService(self):
        t = threading.Thread(target=self._schedLoop)
        t.start()
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

    def _getChannelIds(self):
        if "channelIds" in self.config["alerts"]:
            return self.config["alerts"]["channelIds"]
        else:
            return [self._defaultChannelId()]

    def _defaultChannelId(self):
        return os.getenv("DISCORD_DEFAULT_CHANNELID", default=self.config["defaultChannelId"])


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

## Don't like this approach. Will remove example
async def AlertMktOpens():
    await client.wait_until_ready()
    msg_sent = False
    time = datetime.datetime.now
    test_min = self.time().minute+1
    test_hr = self.time().hour

    while True:
        if time().hour == 17 and (time().minute == test_min or time().minute == test_min+2):
            if not msg_sent:
                await NotifyChannels("Time is: ")
                msg_sent = True
        else:
            print("{}:{}:{}".format(time().hour, time().minute, time().second))
            msg_sent = False
        await asyncio.sleep(1)


