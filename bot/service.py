
import discord
import datetime
import time
import asyncio

from .alertscheduler import AlertScheduler
from .util import ListGuilds

class DiscordAlertBot:
    def __init__(self, client, config, args):
        self.client = client
        self.config = config
        self.args = args

        self.time = datetime.datetime.now
        self.test_min = self.time().minute+1
        self.test_hr = self.time().hour

        #self.client.loop.create_task(AlertMktOpens())

    async def Run(self):
        print('We have logged in as {0.user}'.format(self.client))
        if self.args.listGuilds:
            await self.ListGuilds()
            await self.client.close()
            return
        if self.args.messageAll is not None:
            await self.NotifyAllChannels(self.args.messageAll)
            await self.client.close()
            return

        if self.args.service:
            self.SpawnService()
            return

    async def ProcessMessage(self, message):
        if message.author == self.client.user:
            return

        if message.content.startswith('?hello'):
            await message.channel.send('Hello!')

    async def NotifyAllChannels(self, msg):
        await self.client.wait_until_ready()
        guilds = self.client.guilds
        for guild in guilds:
            for channel in guild.channels:
                print("Assessing Channel({}): {}".format(channel.type, channel.name))
                if channel.type == discord.ChannelType.text:
                    if self.config['discord']['alertChannels'] is not None and channel.name in self.config['discord']['alertChannels']:
                        print("Alerting {}".format( guild ))
                        await channel.send("Configured: {} {}:{}".format(msg, self.time().hour, self.time().minute))
                    else:
                        await channel.send("Unconfigured: {} {}:{}".format(msg, self.time().hour, self.time().minute))
                        print("Skipping {}".format( guild ))

    async def ListGuilds(self):
        await self.client.wait_until_ready()
        for guild in self.client.guilds:
            for channel in guild.channels:
                print(
                    "Available Channel - ID: \"{}\", Name: \"{}\", Type: \"{}\""
                    .format(channel.id, channel.name, channel.type)
                )

    def Stop(self):
        None

## Don't like this approach. Will remove example
async def AlertMktOpens():
    await client.wait_until_ready()
    msg_sent = False
    while True:
        if time().hour == 17 and (time().minute == test_min or time().minute == test_min+2):
            if not msg_sent:
                await NotifyChannels("Time is: ")
                msg_sent = True
        else:
            print("{}:{}:{}".format(time().hour, time().minute, time().second))
            msg_sent = False
        await asyncio.sleep(1)

