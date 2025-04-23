import discord
import asyncio
import os
from discord.ext import commands
from dotenv import load_dotenv
from commands.rcon_commands import RconGeneralCommands
from zomboid_rcon import ZomboidRCON  # You should define or import this class

from monitors.admin_log_monitor import AdminLogMonitor
from monitors.item_edit_monitor import ItemEditLogMonitor
from monitors.exploit_monitor import ExploitLogMonitor
from monitors.perk_monitor import PerkLogMonitor
from commands.admin_commands import setup_admin_commands
from utils.admin_bypass_manager import AdminBypassManager

admin_manager = AdminBypassManager()
load_dotenv()

# --- CONFIG ---
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
LOG_DIR = os.getenv("LOG_DIR")
EXPLOIT_LOG_PATH = os.getenv("EXPLOIT_LOG_PATH")
LEVEL_WINDOW = int(os.getenv("LEVEL_WINDOW", 5))
SRJ_GRACE = int(os.getenv("SRJ_GRACE", 10))
RCON_HOST = os.getenv("RCON_HOST")
RCON_PORT = int(os.getenv("RCON_PORT"))
RCON_PASSWORD = os.getenv("RCON_PASSWORD")

# --- Discord Setup ---
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=commands.DefaultHelpCommand(no_category='Commands'))

# --- Initialize Monitors ---
admin_file_path = os.path.join(os.path.dirname(__file__), "admin_bypass.json")
item_edit_monitor = ItemEditLogMonitor(bot, CHANNEL_ID, LOG_DIR,admin_file_path)
admin_log_monitor = AdminLogMonitor(bot, CHANNEL_ID, LOG_DIR,admin_file_path)
perk_monitor = PerkLogMonitor(bot, CHANNEL_ID,LOG_DIR, srj_grace=SRJ_GRACE, level_window=LEVEL_WINDOW)
exploit_monitor = ExploitLogMonitor(bot, CHANNEL_ID, EXPLOIT_LOG_PATH)

# --- Load Command Cogs ---
@bot.event
async def on_ready():
    print(f"✅ Connected as {bot.user.name}")
    zrcon = ZomboidRCON(RCON_HOST, RCON_PORT, RCON_PASSWORD)
    await bot.add_cog(setup_admin_commands(bot, admin_manager))
    await bot.get_channel(CHANNEL_ID).send("🤖 **TERMINUS BOT is now watching the logs!**")
    await bot.add_cog(RconGeneralCommands(bot, zrcon))    
    # Background loops
    asyncio.create_task(item_edit_monitor.loop())
    asyncio.create_task(admin_log_monitor.loop())
    asyncio.create_task(perk_monitor.loop())
    asyncio.create_task(exploit_monitor.loop())

# --- Run Bot ---
if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)

