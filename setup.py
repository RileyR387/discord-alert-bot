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
    name='discord-alert-bot',
    version='0.0.1',
    author='Riley Raschke',
    author_email='riley@rrappsdev.com',
    scripts=['discord-alert-bot.py'],
    packages=['bot','config'],
    url='https://github.com/RileyR387/discord-alert-bot',
    license='LICENSE',
    description='Discord bot for scheduled notifications.',
    long_description='Configurable alert bot for discord text chats',
    install_requires=requires,
    extras_require={
        'dev': dev_requires
    }
)

