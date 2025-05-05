from datetime import datetime
import nextcord
from nextcord.ext import commands, tasks
from file_read_backwards import FileReadBackwards
import os
import hashlib
import monitors.modUpdater

class consoleReader(commands.Cog):
    def __init__(self, bot, logPath):
        self.bot = bot
        self.logPath = logPath
        self.lastMessageHash = None
        self.lastUpdateRealTimestamp = datetime.now().timestamp() * 1000
        self.sendLogs = True

        self.update.start()  # Start background loop

    def splitLine(self, line: str) -> tuple[int, str]:
        try:
            _, timestamp_part, message = line.strip()[1:].split(">", 2)
            timestamp_str = timestamp_part[timestamp_part.find(",", 2) + 1:].strip().replace(" ", "").replace(",", "")
            return int(timestamp_str), message
        except Exception as e:
            self.bot.log.warning(f"[consoleReader] Failed to parse log line: {line.strip()} ({e})")
            return 0, ""

    @tasks.loop(seconds=2)
    async def update(self) -> None:
        log_file = os.path.join(self.logPath, "server-console.txt")
        if not os.path.exists(log_file):
            return

        print("[consoleReader] 🔄 Loop tick")

        with FileReadBackwards(log_file, encoding="utf-8") as f:
            for line in f:
                if "LOG" not in line:
                    continue

                print(f"[consoleReader] 📝 Read line: {line.strip()}")

                timestamp, message = self.splitLine(line)
                if timestamp >= self.lastUpdateRealTimestamp:
                    messageHash = hashlib.md5(line.encode("utf-8")).hexdigest()
                    if messageHash != self.lastMessageHash:
                        embed = await self.readLog(timestamp, message)
                        self.lastMessageHash = messageHash

                        if embed and hasattr(self.bot, "channel") and self.bot.channel:
                            await self.bot.channel.send(embed=embed)
                else:
                    self.lastUpdateRealTimestamp = datetime.now().timestamp() * 1000
                    break

    async def readLog(self, timestamp: int, message: str) -> None:
        if "CheckModsNeedUpdate: Mods updated" in message:
            self.bot.log.info("[consoleReader] All mods are up-to-date.")

        elif "CheckModsNeedUpdate: Mods need update" in message:
            self.bot.log.warning("[consoleReader] One or more mod(s) need to be updated.")
            channel_id = int(os.getenv("CHANNEL_ID"))
            channel = self.bot.get_channel(channel_id)
            if channel:  # 🛠️ this line had a bad indent in your original code
                await channel.send("📦 One or more mod(s) need to be updated.")
                self.lastUpdateRealTimestamp = datetime.now().timestamp() * 1000
                mod_updater = self.bot.get_cog("modUpdater")
                if mod_updater:
                    await mod_updater.startUpdate()
        else:
            self.bot.log.debug(f"[consoleReader] Ignored: {message}")

        return None
