import nextcord
import asyncio
import os
import re
import json
from utils.embed_factory import create_embed_response
from utils.admin_bypass import AdminBypassManager  # <- import your class properly
class AdminLogMonitor:
    def __init__(self, bot, channel_id, log_dir,admin_bypass):
        self.bot = bot
        self.channel_id = channel_id
        self.log_dir = log_dir
        self.last_positions = {}
        self.last_cleanup = datetime.now()
        self.cleanup_interval = 300  # seconds (5 minutes)
        self.admin_bypass = admin_bypass       
    async def send_alert(self, line):
        channel = self.bot.get_channel(self.channel_id)
        if channel:
            embed = create_embed_response("🛡️ ADMIN ACTION DETECTED", line, color=0x7289da,code_block=True,timestamp=None)
            await channel.send(embed=embed)
    def cleanup(self):
        """Reset tracked file positions and internal state."""
        print("[DEBUG] AdminLogMonitor cleanup triggered.")
        self.last_positions.clear()
    def get_actor_name(self, line):
        # Try to match "SOMETHING CHEAT: PlayerName WHATEVER"

        patterns = [
        # CHEAT commands (TELEPORT, VEHICLE, ITEM etc)
            r"\[Buffy Logs\]\s+(?:[A-Z]+\s+)*CHEAT:\s+([a-zA-Z0-9_]+)",
        # Standard admin actions
            r"\[Buffy Logs\]\s+([a-zA-Z0-9_]+)\s",
        # Fallback for any [Buffy Logs] line
            r"\[Buffy Logs\]\s+([a-zA-Z0-9_]+)",

            r"\[[^\]]+\](?:\s+\[[^\]]+\])?\s+([a-zA-Z0-9_]+)"
        ]
        for pattern in patterns:
            match = re.search(pattern, line)
            if match:
                name = match.group(1)
                # Additional validation for CHEAT commands
                if "CHEAT:" in line and not name.isupper():
                    return name
                elif "CHEAT:" not in line:
                    return name
    
        return None
    async def scan_logs(self):
        self.admin_bypass.reload_if_needed()

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
                    print(f"[DEBUG] FULL LINE: {line.strip()}")
                    print(f"[DEBUG] EXTRACTED ACTOR: {actor}")

                    if actor:
                        actor = actor.strip()
                    if re.search(r"granted\s+\d+\s+access level", line, re.IGNORECASE):
                        await self.send_alert(line)
                        continue
                    if actor:
                        bypassed = self.admin_bypass.is_bypassed(actor)
                        if bypassed:
                            print(f"[DEBUG] Actor: '{actor}' - Bypassed: {bypassed}")
                            continue
                    await self.send_alert(line)
                        

    async def loop(self):
        while True:
            try:
                if (datetime.now() - self.last_cleanup).total_seconds() > self.cleanup_interval:
                    self.cleanup()
                    self.last_cleanup = datetime.now()
                await self.scan_logs()
            except Exception as e:
                print(f"[ADMIN LOG ERROR] {e}")
            await asyncio.sleep(3)

__all__ = ["AdminLogMonitor"]

