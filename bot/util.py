
'''
Utility function for configuring notification destinations
'''
async def ListGuilds(client):
    await client.wait_until_ready()
    for guild in client.guilds:
        for channel in guild.channels:
            print(
                "Server: \"{}\" - ChannelID: \"{}\", ChannelName: \"{}\", ChannelType: \"{}\""
                .format(guild.name, channel.id, channel.name, channel.type)
            )

