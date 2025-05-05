import nextcord
import asyncio
import os
import re
import json
from utils.embed_factory import create_embed_response
from utils.admin_bypass import AdminBypassManager  # <- import your class properly
from datetime import datetime
class ItemEditLogMonitor:
    def __init__(self, bot, channel_id, log_dir,admin_bypass):
        self.bot = bot
        self.channel_id = channel_id
        self.log_dir = log_dir
        self.last_positions = {}
        self.admin_bypass = admin_bypass
        self.last_cleanup = datetime.now()
        self.cleanup_interval = 300  # seconds (5 minutes)
    def get_editor_name(self, line):
        match = re.search(r"ITEM EDITED!\s+-*([\w\s]+?)(?:\s+changed|\s+opened)", line)
        return match.group(1).strip() if match else None
    def cleanup(self):
        """Reset tracked file positions for memory or log rotation purposes."""
        print("[DEBUG] ItemEditLogMonitor cleanup triggered.")
        self.last_positions.clear()
    async def send_alert(self, line):
        channel = self.bot.get_channel(self.channel_id)
        if channel:
            embed = create_embed_response("🛠️ ITEM EDIT DETECTED", line, color=0xff5733)
            await channel.send(embed=embed)

    async def scan_logs(self):
        self.admin_bypass.reload_if_needed()
        for file in os.listdir(self.log_dir):
            if not file.endswith("_itemEdits.txt"):
                continue

            file_path = os.path.join(self.log_dir, file)
            if file_path not in self.last_positions:
                self.last_positions[file_path] = os.path.getsize(file_path)
                continue

            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                f.seek(self.last_positions[file_path])
                new_lines = f.readlines()
                self.last_positions[file_path] = f.tell()

                for line in new_lines:
                    if "ITEM EDITED!" not in line:
                        continue
                    editor = self.get_editor_name(line)
                    if editor and not self.admin_bypass.is_bypassed(editor):
                        await self.send_alert(line)

    async def loop(self):
        while True:
            try:
                if (datetime.now() - self.last_cleanup).total_seconds() > self.cleanup_interval:
                    self.cleanup()
                    self.last_cleanup = datetime.now()
                await self.scan_logs()
            
            except Exception as e:
                print(f"[ITEM EDIT ERROR] {e}")
            await asyncio.sleep(3)


