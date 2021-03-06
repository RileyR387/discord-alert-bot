
async def ProcessMessage(message):
    if message.content.startswith('?hello'):
        await message.channel.send('Hello from development!')

