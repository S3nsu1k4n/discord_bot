import os

import discord
from discord.ext import commands
from discord import Embed
from dotenv import load_dotenv

from meme import get_reddit_meme, get_cat_api_image_url
from pokemon_text import main as pokemon_text

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_SERVER')
CHANNEL_MEMES = int(os.getenv('CHANNEL_MEMES'))
CHANNEL_KATZEN = int(os.getenv('CHANNEL_KATZEN'))
CHANNEL_POKEMON = int(os.getenv('CHANNEL_POKEMON'))

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


@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandNotFound):
    await ctx.send(f'"**{ctx.message.content.split(" ")[0]}**" kenne ich nicht, miau!')


@bot.command(name='meme', help='Get the meme!')
async def get_meme(ctx):
    if ctx.author == bot.user.name:
        return

    msg = ''
    data = get_reddit_meme()
    if data['url'].find('youtube.com') != -1 or data['url'].find('?source=fallback') != -1:
        embed = Embed(title=data['title'], url=data['post_link'], color=0x9400D3)
        msg = data['url']
    else:
        embed = Embed(title=data['title'], url=data['post_link'], description=data['url'], color=0x00ff00)
        embed.set_image(url=data['url'])
    embed.set_author(name=data['author'], icon_url='https://www.redditstatic.com/desktop2x/img/favicon/apple-icon-120x120.png')
    embed.add_field(name='Gepostet', value=data['timestamp'])
    embed.add_field(name='Subreddit', value=data["subreddit"])
    channel = bot.get_channel(CHANNEL_MEMES)

    await channel.send(embed=embed)
    if msg:
        await channel.send(msg)


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


@bot.command(name='game', help='Play Pokemon Text!')
async def play_pokemon_text(ctx, *args):
    channel = bot.get_channel(CHANNEL_POKEMON)
    if len(args) > 0:
        arg = args[0]
    else:
        arg = ''

    player_name = ctx.author

    if player_name not in pokemon_text.games:
        response = pokemon_text.init(player_name=ctx.author)
        embed = Embed(title='Pokemon Text',
                      description='Professor Eichs Pokemon-Labor',
                      color=discord.Color.green(),
                      )
        embed.add_field(name=response.info.speaker, value=response.info.text, inline=False)
        starter = pokemon_text.games[player_name].get_starter()
        for i, (k, v) in enumerate(starter.items()):
            value = '\n'.join(f'{vk}: {vv}' for vk, vv in v.items())
            embed.add_field(name=f'{i+1}: {k}', value=value)
        await channel.send(embed=embed)
    else:
        response = pokemon_text.use_command(player_name=player_name, arg=arg)

        embed = Embed(title='Pokemon Text',
                      description='Professor Eichs Pokemon-Labor',
                      color=discord.Color.red(),
                      )

        if response.enemy is not None:
            embed.add_field(name=response.enemy.speaker, value=response.enemy.text, inline=False)
            embed.add_field(name=response.player.speaker, value=response.player.text)
            embed.add_field(name=response.attacks.speaker, value=response.attacks.text)

        if response.info is not None:
            embed.add_field(name=response.info.speaker, value=response.info.text, inline=False)
        if response.battle_info is not None:
            await channel.send(response.battle_info.text)
        await channel.send(embed=embed)


if __name__ == '__main__':
    bot.run(TOKEN)