import os
from discord.ext import commands
from discord import Embed
from dotenv import load_dotenv

from meme import get_reddit_meme, get_cat_api_image_url

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_SERVER')
CHANNEL_MEMES = int(os.getenv('CHANNEL_MEMES'))
CHANNEL_KATZEN = int(os.getenv('CHANNEL_KATZEN'))

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )


@bot.command(name='meme', help='Get the meme!')
async def get_meme(ctx):
    if ctx.author == bot.user.name:
        return

    data = get_reddit_meme()
    embed = Embed(title=data['title'],
                  description=data['url'],
                  color=0x00ff00
                  )
    embed.set_image(url=data['url'])
    embed.set_footer(text='/' + data["subreddit"])

    channel = bot.get_channel(CHANNEL_MEMES)

    await channel.send(embed=embed)


@bot.command(name='cat', help='Random cat!')
async def get_cat(ctx):
    if ctx.author == bot.user.name:
        return

    data = get_cat_api_image_url()
    embed = Embed(description=data['url'],
                  color=0x00ff00
                  )
    embed.set_image(url=data['url'])
    embed.set_footer(text=f"{data['width']}x{data['height']}")

    channel = bot.get_channel(CHANNEL_KATZEN)

    await channel.send(embed=embed)


if __name__ == '__main__':
    bot.run(TOKEN)