
import os

'''
Plugin Abstract

Plugins configuration is best stored in environment variables for external control with possibly sane defaults

All plugins are of class name "BotPlugin"
'''

class BotPlugin:
    def __init__(self, msgCallback):
        self.name = "basicplugin"
        self.SendMessage = msgCallback

    # The alert bot service can be configured to run this based on primary services config
    def Job(self):
        None

    # Run custom threads/refreshes here, using `self.SendMessage`
    # on demand for the default or configured channel ID's
    def Run(self):
        # Bot default channel
        self.SendMessage("Basic Test Message Sending")

        # custom single channel
        self.SendMessage({
            'channelid': 660676159259934723,
            'msg': "Test single channel plugin message",
        })
        # multi custom channel
        self.SendMessage({
            'channelids': [ 660676159259934723, 807086041063227412 ],
            'msg': "Test multi channel plugin message",
        })
        # broadcast to all text channels
        ##self.SendMessage({
        ##    'BROADCAST': True ,
        ##    'msg': "Test all channel plugin message"
        ##})

    # Custom message interpriters for the plugin
    async def ProcessMessage(self, message):
        if message.content.startswith('?testplugin'):
            await message.channel.send('Hello from a plugin!')

