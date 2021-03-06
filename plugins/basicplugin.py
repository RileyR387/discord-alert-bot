
import os

class BotPlugin:
    def __init__(self, msgCallback):
        self.name = "basicplugin"
        self.SendMessage = msgCallback

    async def ProcessMessage(self, message):
        if message.content.startswith('?testplugin'):
            await message.channel.send('Hello from a plugin!')

        self.SendMessage("Test Message Sending")

