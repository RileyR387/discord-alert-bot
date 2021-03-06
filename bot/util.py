
'''
Utility function for configuring notification destinations
'''
def ListGuilds(guilds):
    for guild in guilds:
        print(
            "Server: \"{}\" - ChannelID: \"{}\", ChannelName: \"{}\", ChannelType: \"{}\""
            .format(guild['server'], guild['channelID'], guild['channelName'], guild['channelType'])
        )

