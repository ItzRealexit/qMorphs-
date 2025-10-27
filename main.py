import os
import asyncio
import discord
from discord import app_commands
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# ---- When bot is ready ----
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"🔁 Synced {len(synced)} slash commands.")
    except Exception as e:
        print(f"❌ Error syncing commands: {e}")

# ---- /dm command ----
@bot.tree.command(name="dm", description="Send a DM to everyone with a specific role.")
@app_commands.describe(role="Role to DM", message="Message to send")
async def dm(interaction: discord.Interaction, role: discord.Role, message: str):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("❌ Only admins can use this command.", ephemeral=True)
        return

    await interaction.response.send_message(f"📨 Sending DMs to members with role: {role.name}...")

    sent = 0
    failed = 0

    for member in role.members:
        if member.bot:
            continue
        try:
            await member.send(message)
            sent += 1
            await asyncio.sleep(2)
        except:
            failed += 1

    # 👇 Custom thank-you message added here
    await interaction.followup.send(
        f"✅ DMs sent to {sent} members, failed for {failed}.\n\n"
        f"**THANKS FOR USING CNB OFFICIAL BOT. Made by psychopathmc 🔥**"
    )

# ---- Run bot ----
bot.run(os.getenv("TOKEN"))
