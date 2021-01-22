
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

    async def NotifyAllChannels(self, msg):
        await self.client.wait_until_ready()
        guilds = self.client.guilds
        for guild in guilds:
            for channel in guild.channels:
                print("Assessing Channel({}): {}".format(channel.type, channel.name))
                if channel.type == discord.ChannelType.text:
                    if config['discord']['alertChannels'] is not None and channel.name in config['discord']['alertChannels']:
                        print("Alerting {}".format( guild ))
                        await channel.send("Configured: {} {}:{}".format(msg, time().hour, time().minute))
                    else:
                        await channel.send("Unconfigured: {} {}:{}".format(msg, time().hour, time().minute))
                        print("Skipping {}".format( guild ))

    async def ProcessMessage(self, message):
        if message.author == self.client.user:
            return

        if message.content.startswith('?hello'):
            await message.channel.send('Hello!')

    async def Run(self):
        print('We have logged in as {0.user}'.format(self.client))
        await ListGuilds(self.client)
        await self.client.close()

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

