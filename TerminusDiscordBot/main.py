import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import os
import asyncio
from dotenv import load_dotenv
from zomboid_rcon import ZomboidRCON  # You should define or import this class
from monitors.admin_log_monitor import AdminLogMonitor
from monitors.item_edit_monitor import ItemEditLogMonitor
from monitors.exploit_monitor import ExploitLogMonitor
from monitors.perk_monitor import PerkLogMonitor
from utils.admin_bypass import AdminBypassManager
from pydactyl import PterodactylClient
from monitors.modUpdater import ModUpdateMonitor
from monitors.consoleReader import consoleReader  
from pathlib import Path


admin_manager = AdminBypassManager()
load_dotenv()

# Import Bot Token
intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# --- CONFIG ---
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
LOG_DIR = os.getenv("LOG_DIR")
ZOMBOID_PATH = os.getenv("ZOMBOID_PATH")
EXPLOIT_LOG_PATH = os.getenv("EXPLOIT_LOG_PATH")
LEVEL_WINDOW = int(os.getenv("LEVEL_WINDOW", 5))
SRJ_GRACE = int(os.getenv("SRJ_GRACE", 10))
SRJ_MAX_DRATION =int(os.getenv("SRJ_MAX_DRATION", 15))
# --- Initialize Monitors ---
admin_file_path = os.path.join(os.path.dirname(__file__), "admin_bypass.json")

item_edit_monitor = ItemEditLogMonitor(bot, CHANNEL_ID, LOG_DIR,admin_manager)
admin_log_monitor = AdminLogMonitor(bot, CHANNEL_ID, LOG_DIR,admin_manager)
perk_monitor = PerkLogMonitor(bot, CHANNEL_ID,LOG_DIR,admin_manager, srj_grace=SRJ_GRACE, suspicious_window=LEVEL_WINDOW,srj_max_duration=SRJ_MAX_DRATION)
exploit_monitor = ExploitLogMonitor(bot, CHANNEL_ID, EXPLOIT_LOG_PATH)

def detect_log_path():
    # Try environment variable first
    env_path = os.getenv("ZOMBOID_PATH")
    if env_path and Path(env_path).joinpath("console-server.txt").exists():
        return str(Path(env_path))

    # Search user home directory for console-server.txt
    home = Path.home()
    for path in home.rglob("console-server.txt"):
        return str(path.parent)

    return None  # Not found

logPath = detect_log_path()

@bot.event
async def on_ready():
    print("The bot is now ready for use!")
    print("-----------------------------")
    await bot.get_channel(CHANNEL_ID).send("🤖 **TERMINUS BOT is now watching the logs!**")
    # Background loops
    asyncio.create_task(item_edit_monitor.loop())
    asyncio.create_task(admin_log_monitor.loop())
    asyncio.create_task(perk_monitor.loop())
    asyncio.create_task(exploit_monitor.loop())
    log_file = os.path.join(logPath, "console-server.txt")
    if not os.path.exists(log_file):
        return
    await bot.add_cog(consoleReader(bot,log_file))

#cogs commands
initial_extensions = []
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        initial_extensions.append("cogs." + filename[:-3])

if __name__ == "__main__":
    for extension in initial_extensions:
        bot.load_extension(extension)
    
bot.run(DISCORD_TOKEN)
