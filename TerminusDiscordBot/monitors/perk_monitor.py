import discord
import asyncio
import os
import re
from datetime import datetime

class PerkLogMonitor:
    def __init__(self, bot, channel_id, log_dir, srj_grace=10, level_window=5):
        self.bot = bot
        self.channel_id = channel_id
        self.log_dir = log_dir
        self.srj_grace = srj_grace
        self.level_window = level_window
        self.processed_lines = set()
        self.player_tracking = {}  # steamid → skill → {levels, times, username}
        self.srj_reading = {}      # steamid → datetime
        self.log_file = None
        self.last_position = 0

        self.pattern_perk = re.compile(
            r"\[(\d{2}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3})\] \[(\d+)\]\[(.+?)\]\[(.+?)\]\[Level Changed\]\[(\w+)\]\[(\d+)\]\[Hours Survived: (\d+)\]"
        )
        self.pattern_srj_start = re.compile(
            r"\[(\d{2}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+)\] \[(\d+)\]\[(.+?)\].*?\[SRJ START READING\]",
            re.IGNORECASE
        )
        self.pattern_srj_stop = re.compile(
            r"\[(\d{2}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+)\] \[(\d+)\]\[(.+?)\].*?\[SRJ STOP READING\]",
            re.IGNORECASE
        )

    async def send_suspicious(self, steamid, username, skill, old_level, new_level, delta, hours_survived):
        channel = self.bot.get_channel(self.channel_id)
        embed = discord.Embed(
            description=f"`[SUSPICIOUS]: [{steamid}] {username} {{{skill}}} ({old_level} → {new_level}) D:{delta:.1f}s HS:{hours_survived}`",
            color=0xffc107
        )
        await channel.send(embed=embed)

    def is_reading_srj(self, steamid: str, time: datetime):
        if steamid in self.srj_reading:
            delta = (time - self.srj_reading[steamid]).total_seconds()
            if delta < self.srj_grace:
                return True
            else:
                del self.srj_reading[steamid]
        return False

    async def scan_log(self):
        try:
            logs = [f for f in os.listdir(self.log_dir) if f.endswith("_PerkLog.txt")]
            if not logs:
                return

            logs.sort(reverse=True)
            log_path = os.path.join(self.log_dir, logs[0])

            if not self.log_file or self.log_file.name != log_path:
                self.log_file = open(log_path, 'r', encoding='utf-8', errors='ignore')
                self.log_file.seek(0, os.SEEK_END)
                self.last_position = self.log_file.tell()

            self.log_file.seek(self.last_position)
            new_lines = self.log_file.readlines()
            self.last_position = self.log_file.tell()

            for line in new_lines:
                line = line.strip()

                if srj := self.pattern_srj_start.search(line):
                    srj_time = datetime.strptime(srj.group(1), "%y-%m-%d %H:%M:%S.%f")
                    steamid = srj.group(2)
                    self.srj_reading[steamid] = srj_time
                    print(f"[DEBUG] SRJ START: {steamid} at {srj_time}")
                    continue

                if stop := self.pattern_srj_stop.search(line):
                    steamid = stop.group(2)
                    self.srj_reading.pop(steamid, None)
                    if steamid in self.player_tracking:
                        print(f"[DEBUG] Clearing tracking for {steamid} after SRJ stop")
                        self.player_tracking.pop(steamid)
                    print(f"[DEBUG] SRJ STOP: {steamid}")
                    continue

                match = self.pattern_perk.search(line)
                if not match:
                    continue

                log_time = datetime.strptime(match.group(1), "%y-%m-%d %H:%M:%S.%f")
                steamid = match.group(2)
                username = match.group(3)
                skill = match.group(5)
                level = int(match.group(6))
                hours_survived = int(match.group(7))

                if self.is_reading_srj(steamid, log_time):
                    continue

                if steamid not in self.player_tracking:
                    self.player_tracking[steamid] = {}

                if skill not in self.player_tracking[steamid]:
                    self.player_tracking[steamid][skill] = {
                        "levels": [level],
                        "times": [log_time],
                        "username": username
                    }
                    continue

                tracking = self.player_tracking[steamid][skill]
                last_level = tracking["levels"][-1]
                last_time = tracking["times"][-1]

                if level < last_level:
                    tracking["levels"] = [level]
                    tracking["times"] = [log_time]
                    return

                if level > last_level:
                    delta = (log_time - last_time).total_seconds()

                    if skill.lower() == "engineering" and last_level >= 5:
                        print(f"[DEBUG] Skipping 0.0s Engineering perk gain for {steamid} ({last_level} → {level})")
                        tracking["levels"].append(level)
                        tracking["times"].append(log_time)
                        return

                    if delta < self.level_window:
                        print(f"[DEBUG] Suspicious: {steamid} {skill} {last_level} → {level} D:{delta:.2f}s")
                        tracking["levels"].append(level)
                        tracking["times"].append(log_time)
                        await self.send_suspicious(steamid, username, skill, last_level, level, delta, hours_survived)
                    else:
                        tracking["levels"] = [level]
                        tracking["times"] = [log_time]

        except Exception as e:
            print(f"[PERK MONITOR ERROR] {e}")

    async def loop(self):
        while True:
            await self.scan_log()
            await asyncio.sleep(1)
