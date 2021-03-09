
import os
import time
import asyncio

'''
Plugin Abstract

Plugins configuration is best stored in environment variables for external control with possibly sane defaults

All plugins are of class name "BotPlugin"
'''

class BotPlugin:
    def __init__(self, msgCallback):
        self.name = "basicplugin"
        self.SendMessage = msgCallback
        self.initEnv()
        self.running = True

    def initEnv(self):
        self.defaultChannel = int(os.getenv('BASICPLUGIN_DEFAULT_CHANNEL_ID', default='660676159259934723'))
        self.channels = []
        for channel in os.getenv('BASICPLUGIN_CHANNEL_IDS', default='660676159259934723, 807086041063227412').split(','):
            self.channels.append(int(channel.strip()))

    # Parent is stopping, maintenance op for clean exit
    def Stop(self):
        self.running = False

    # The alert bot service can be configured to run this based on primary services config
    def Job(self):
        self.SendMessage("Scheduled job from a plugin!")

    # Run asyncio tasks here within the discord event loop,
    # using `self.SendMessage` on demand for the default
    # or configured channel ID's
    async def Run(self):
        # Bot default channel
        self.SendMessage("Basic Test Message Sending")

        # custom single channel
        self.SendMessage({
            'channelid': self.defaultChannel,
            'msg': "Test single channel plugin message",
        })
        # multi custom channel
        self.SendMessage({
            'channelids': self.channels,
            'msg': "Test multi channel plugin message",
        })
        # broadcast to all text channels
        '''
        self.SendMessage({
            'BROADCAST': True ,
            'msg': "Test all channel plugin message"
        })
        '''
        # run forever!
        '''
        while self.running:
            self.SendMessage("Time is: " + str(time.time()))
            asyncio.sleep(10)
        '''

    # Custom message interpriters for the plugin
    async def ProcessMessage(self, message):
        if message.content.startswith('?testplugin'):
            await message.channel.send('Hello from a plugin!')


