from setuptools import setup, find_packages

requires = [
    'argparse',
    'PyYAML',
    'schedule',
    'discord.py'
]

dev_requires = [
    'pipreqs'
]

setup(
    name='discord-market-alert-bot',
    version='0.0.1',
    author='Riley Raschke',
    author_email='riley@rrappsdev.com',
    scripts=['discord-market-alert-bot.py', 'discord-market-alert-sendone.py' ],
    url='ssh://scm.rrappsdev.com/var/git/discord-market-alert-bot',
    license='LICENSE',
    description='Discord bot for global market notifications.',
    long_description='Configurable alert bot for discord text chats',
    install_requires=requires,
    extras_require={
        'dev': dev_requires
    }
)

