
import os

class BotPlugin:
    def __init__(self, msgCallback):
        self.name = "basicplugin"
        self.SendMessage = msgCallback

    async def ProcessMessage(self, message):
        if message.content.startswith('?testplugin'):
            await message.channel.send('Hello from a plugin!')

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

