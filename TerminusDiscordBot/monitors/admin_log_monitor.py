import nextcord
import asyncio
import os
import re
import json
from utils.embed_factory import create_embed_response

class AdminLogMonitor:
    def __init__(self, bot, channel_id, log_dir, admin_file_path):
        self.bot = bot
        self.channel_id = channel_id
        self.log_dir = log_dir
        self.admin_file_path = admin_file_path
        self.last_positions = {}
        self.admin_bypass = set()
        self.load_admins()

    def load_admins(self):
        try:
            with open(self.admin_file_path, 'r') as f:
                self.admin_bypass = set(json.load(f))
        except (FileNotFoundError, json.JSONDecodeError):
            self.admin_bypass = set()

    def save_admins(self):
        with open(self.admin_file_path, 'w') as f:
            json.dump(list(self.admin_bypass), f)

    async def send_alert(self, line):
        channel = self.bot.get_channel(self.channel_id)
        if channel:
            embed = create_embed_response("🛡️ ADMIN ACTION DETECTED", line, color=0x7289da,code_block=True)
            await channel.send(embed=embed)

    def get_actor_name(self, line):
        match = re.match(r"\[[^\]]+\](?:\s+\[[^\]]+\])?\s+(\w+)", line)
        return match.group(1) if match else None

    async def scan_logs(self):
        self.load_admins()
        for file in os.listdir(self.log_dir):
            if not file.endswith("_admin.txt"):
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
                    actor = self.get_actor_name(line)
                    if re.search(r"granted\s+\d+\s+access level", line, re.IGNORECASE):
                        await self.send_alert(line)
                        continue
                    actor = next((admin for admin in self.admin_bypass if re.search(rf"\b{re.escape(admin)}\b", line)), None)
                    if actor:
                        continue
                    await self.send_alert(line)
                        

    async def loop(self):
        while True:
            try:
                await self.scan_logs()
            except Exception as e:
                print(f"[ADMIN LOG ERROR] {e}")
            await asyncio.sleep(3)

__all__ = ["AdminLogMonitor"]
