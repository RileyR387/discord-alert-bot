# Discord Alert Bot

A discord bot with configurable alerts.

### Install
```
python3 -m venv venv
./venv/bin/pip install .
./venv/bin/discord-alert-bot.py --help
```

### Channel ID look up
To look up channel IDs for configuration, set the bot token and run `./discord-alert-bot.py --listGuilds`
```
export DISCORD_BOT_TOKEN="my bots token"
./discord-alert-bot.py --listGuilds
```
Please note that the discord server must first authorize the bot to see the available channels.

### Usage
```
./discord-alert-bot.py --help
usage: discord-alert-bot.py [-h] [-c conf.yaml] [-a msgText] [-m msgText]
                            [-i 123456...] [-l] [-t]

Configurable discord alert bot

optional arguments:
  -h, --help            show this help message and exit
  -c conf.yaml, --config conf.yaml
                        Specify single config file
  -a msgText, --messageAll msgText
                        Send a test message to all channels.
  -m msgText, --message msgText
                        Message a single channel, requires `-i`
  -i 123456..., --channelId 123456...
                        ChannelID to use with `--message`
  -l, --listGuilds      List all channels and their unique id's
  -t, --test            Send test message every 10 seconds

```

### Environment Variable Overrides

The following environment variables can bet set, overriding configuration values or lack there of:
```
export DISCORD_BOT_TOKEN="<long bot token>"
export DISCORD_DEFAULT_CHANNELID="123456789101112131415161718"
```

### Configuration
By default, configurations will be automatically loaded and merged from the following locations if the file exists. Any keys specified in the last existing configuration location will overwrite any prior specifications.
```
./default.yaml
./etc/discord-alert-bot.yaml
~/etc/discord-alert-bot.yaml
~/.discord-alert-bot.yaml
/etc/discord-alert-bot.yaml
```

Complete config example without need for environment variables
```default.yaml
---
discordBotToken: "<long bot token>"

# Used for single messages from command line
discordDefaultChannelId: 123456789101112131415161718

alerts:
  channelIds: [123456789101112131415161718] # for multiple channels, fall back to `discordDefaultChannelId` if not specified
  daily: # CST below
    "19:00":
      days: [sunday,monday,tuesday,wednesday,thursday]
      msg: "The TSE (Tokyo Stock Exchange) is now open"
    "20:15":
      days: [sunday,monday,tuesday,wednesday,thursday]
      msg:  "The SSE (Shanghai Stock Exchange) is now open"
    "20:30":
      days: [sunday,monday,tuesday,wednesday,thursday]
      msg:  "The HKE (Hong Kong Stock Exchange) is now open"
    "01:00":
      days: [monday,tuesday,wednesday,thursday,friday]
      msg:  "The TSE (Tokyo Stock Exchange) is now closed"
    "02:00":
      days: [monday,tuesday,wednesday,thursday,friday]
      msg:  "The LSE (London Stock Exchange) is now open"
    "02:00":
      days: [monday,tuesday,wednesday,thursday,friday]
      msg:  "The SSE (Shanghai Stock Exchange) is now closed"
    "03:00":
      days: [monday,tuesday,wednesday,thursday,friday]
      msg:  "The HKE (Hong Kong Stock Exchange) is now closed"
    "08:30":
      days: [monday,tuesday,wednesday,thursday,friday]
      msg:  "The cash market is now open! Have a great trading day!"
    "10:30":
      days: [monday,tuesday,wednesday,thursday,friday]
      msg:  "The LSE (London Stock Exchange) is now closed"
    "15:00":
      days: [monday,tuesday,wednesday,thursday,friday]
      msg:  "The cash market is now closed! Hope you had a great trading day!"

```

### Additional Resources
For information on creating bot tokens check out:
  - https://www.freecodecamp.org/news/create-a-discord-bot-with-python/


### Systemd Install
as root:
```
useradd --system -d /opt/discord-bots -s /sbin/nologin discord
mkdir /opt/discord-bots
cd /opt/discord-bots
mkdir etc
git clone https://github.com/RileyR387/discord-alert-bot.git
cd discord-alert-bot
python3 -m venv venv
./venv/bin/pip3 install .
cp default.yaml /opt/discord-bots/etc/discord-alert-bot.yaml
# configure the bot by populating /opt/discord-bots/etc/discord-alert-bot.yaml with channel id's and bot token by hand

cp systemd/discord-alert-bot.service /etc/systemd/system/discord-alert-bot.service
systemctl daemon-reload
systemctl enable discord-alert-bot
systemctl start discord-alert-bot
systemctl status discord-alert-bot
# done!
# view log:
journalctl -n 100 -u discord-alert-bot
```

