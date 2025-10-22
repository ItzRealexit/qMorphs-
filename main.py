import discord
from discord.ext import commands
import asyncio
import os

# --------- Intents (important) ---------
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# --------- Bot setup ---------
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")

# --------- DM command ---------
@bot.command()
@commands.has_permissions(administrator=True)
async def dm(ctx, role: discord.Role, *, message):
    """DM all members of a mentioned role."""
    sent = 0
    failed = 0

    await ctx.send(f"📨 Sending DMs to members with role: **{role.name}** ...")

    for member in role.members:
        if member.bot:
            continue  # Skip bots
        try:
            await member.send(message)
            sent += 1
            await asyncio.sleep(2)  # delay to avoid rate limit
        except:
            failed += 1

    await ctx.send(f"✅ Done! Sent to `{sent}` members, failed for `{failed}`.")

# --------- Run bot ---------
bot.run(os.getenv("TOKEN"))
