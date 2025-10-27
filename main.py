import os
import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command()
@commands.has_permissions(administrator=True)
async def dm(ctx, role: discord.Role, *, message):
    """DM all members with a specific role"""
    sent = 0
    failed = 0
    await ctx.send(f"📨 Sending DMs to members with role: {role.name}...")
    for member in role.members:
        if member.bot:
            continue
        try:
            await member.send(message)
            sent += 1
            await asyncio.sleep(2)
        except:
            failed += 1
    await ctx.send(f"✅ Sent to {sent} members, failed for {failed}.")

bot.run(os.getenv("TOKEN"))
