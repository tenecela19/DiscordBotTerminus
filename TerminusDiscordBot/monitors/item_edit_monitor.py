import discord
import asyncio
import os
import re
import json

class ItemEditLogMonitor:
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

    def get_editor_name(self, line):
        match = re.search(r"ITEM EDITED!\s+-*([\w\s]+?)(?:\s+changed|\s+opened)", line)
        return match.group(1).strip() if match else None

    async def send_alert(self, line):
        channel = self.bot.get_channel(self.channel_id)
        if channel:
            embed = discord.Embed(
                title="🛠️ ITEM EDIT DETECTED",
                description=f"```{line.strip()}```",
                color=0xff5733
            )
            await channel.send(embed=embed)

    async def scan_logs(self):
        self.load_admins()
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
                    if editor and editor not in self.admin_bypass:
                        await self.send_alert(line)

    async def loop(self):
        while True:
            try:
                await self.scan_logs()
            except Exception as e:
                print(f"[ITEM EDIT ERROR] {e}")
            await asyncio.sleep(3)

