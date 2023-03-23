# This example requires the 'message_content' intent.

import discord
from discord.ext import commands

import module.grouping_module as mg

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

members = []

alpha = mg.Group('alpha', 'アルファ')
bravo = mg.Group('bravo', 'ブラボー')

matchNum = [0]

memberId = [1]

@bot.command(name='add')
async def addMember(ctx, arg):
    await ctx.send(mg.addMember(members, arg, memberId))

@bot.command(name='koei')
async def setLongRange(ctx, arg):
    await ctx.send(mg.setLongRange(members, arg))

@bot.command(name='team')
async def grouping(ctx):
    await ctx.send(mg.grouping(members, alpha, bravo))

@bot.command(name='win')
async def countWin(ctx, arg):
    await ctx.send(mg.countWin(members, alpha, bravo, matchNum, arg))

@bot.command(name='member')
async def printMembers(ctx):
    await ctx.send(mg.printMembers(members))

@bot.command(name='rate')
async def printRate(ctx):
    await ctx.send(mg.printRate(members))

@bot.command(name='weapon')
async def choiceWeaponForMembers(ctx):
    await ctx.send(mg.choiceWeaponForMembers(members))

@bot.command(name='random')
async def choiceWeapon(ctx):
    await ctx.send(mg.choiceWeapon())

@bot.command(name='inst')
async def printInst(ctx):
    await ctx.send(mg.printInst())

bot.run('your_token')
