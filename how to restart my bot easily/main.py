import discord
import os
import restart as rstart
from discord.ext.commands import Bot


bot = Bot(command_prefix='!', description='How to restart your bot easily', intents=discord.Intents.all())



@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.command()
async def restart(ctx):
    await ctx.send("Restarting...")
    os.system('python restart.py')
    await bot.close()


bot.run("")
