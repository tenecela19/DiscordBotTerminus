import os
import hashlib
from datetime import datetime
from nextcord.ext import commands, tasks
from file_read_backwards import FileReadBackwards

class ConsoleReader(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = int(os.getenv("CHANNEL_ID"))
        self.pz_path = os.getenv("PZ_PATH")
        self.console_path = os.path.join(self.pz_path, "server-console.txt")
        self.last_hash = None
        self.monitor_logs.start()

    @tasks.loop(seconds=2)
    async def monitor_logs(self):
        if not os.path.exists(self.console_path):
            print("⚠️ server-console.txt not found.")
            return

        with FileReadBackwards(self.console_path, encoding="utf-8") as f:
            for line in f:
                if "CheckModsNeedUpdate: Mods need update" in line:
                    line_hash = hashlib.md5(line.encode()).hexdigest()
                    if line_hash != self.last_hash:
                        await self.alert_discord()
                        self.last_hash = line_hash
                    break  # Stop after finding first match

    async def alert_discord(self):
        channel = self.bot.get_channel(self.channel_id)
        if channel:
            await channel.send("📦 One or more mod(s) need to be updated.")
