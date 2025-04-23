import discord
import asyncio
import os
import re
from datetime import datetime, timedelta

class PerkLogMonitor:
    def __init__(self, bot, channel_id, log_dir, srj_grace=15, level_window=5):
        self.bot = bot
        self.channel_id = channel_id
        self.log_dir = log_dir
        self.srj_grace = srj_grace
        self.level_window = level_window
        self.tracking_ttl = 3600  # 1 hour TTL
        self.cleanup_interval = 300  # 5 minutes
        self.last_cleanup = datetime.utcnow()
        
        self.player_tracking = {}
        self.srj_reading = {}
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

    def cleanup_old_entries(self):
        now = datetime.utcnow()
        # Clean SRJ reading entries
        expired_srj = [k for k, v in self.srj_reading.items() 
                      if (now - v).total_seconds() > self.srj_grace]
        for steamid in expired_srj:
            del self.srj_reading[steamid]
        
        # Clean player tracking
        expired_players = []
        for steamid, skills in self.player_tracking.items():
            try:
                newest_time = max(max(data["times"]) for data in skills.values() if data["times"])
                if (now - newest_time).total_seconds() > self.tracking_ttl:
                    expired_players.append(steamid)
            except ValueError:
                expired_players.append(steamid)
        
        for steamid in expired_players:
            del self.player_tracking[steamid]

    async def send_suspicious(self, steamid, username, skill, old_level, new_level, delta, hours_survived):
        channel = self.bot.get_channel(self.channel_id)
        if channel:
            embed = discord.Embed(
                description=f"`[SUSPICIOUS]: [{steamid}] {username} {{{skill}}} ({old_level} → {new_level}) D:{delta:.1f}s HS:{hours_survived}`",
                color=0xffc107
            )
            await channel.send(embed=embed)

    async def scan_log(self):
        try:
            # Periodic cleanup
            if (datetime.utcnow() - self.last_cleanup).total_seconds() > self.cleanup_interval:
                self.cleanup_old_entries()
                self.last_cleanup = datetime.utcnow()

            logs = [f for f in os.listdir(self.log_dir) if f.endswith("_PerkLog.txt")]
            if not logs:
                return

            logs.sort(reverse=True)
            log_path = os.path.join(self.log_dir, logs[0])

            if not self.log_file or self.log_file.name != log_path:
                if self.log_file:
                    self.log_file.close()
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
                    continue

                if stop := self.pattern_srj_stop.search(line):
                    steamid = stop.group(2)
                    self.srj_reading.pop(steamid, None)
                    self.player_tracking.pop(steamid, None)
                    continue

                if match := self.pattern_perk.search(line):
                    log_time = datetime.strptime(match.group(1), "%y-%m-%d %H:%M:%S.%f")
                    steamid = match.group(2)
                    username = match.group(3)
                    skill = match.group(5)
                    level = int(match.group(6))
                    hours_survived = int(match.group(7))

                    if steamid in self.srj_reading:
                        if (log_time - self.srj_reading[steamid]).total_seconds() < self.srj_grace:
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
                        continue

                    if level > last_level:
                        delta = (log_time - last_time).total_seconds()

                        if skill.lower() == "engineering" and last_level >= 5:
                            tracking["levels"].append(level)
                            tracking["times"].append(log_time)
                            continue

                        if delta < self.level_window:
                            tracking["levels"].append(level)
                            tracking["times"].append(log_time)
                            await self.send_suspicious(steamid, username, skill, last_level, level, delta, hours_survived)
                        else:
                            tracking["levels"] = [level]
                            tracking["times"] = [log_time]

        except Exception as e:
            print(f"[PERK MONITOR ERROR] {e}")
            if self.log_file:
                self.log_file.close()
                self.log_file = None

    async def loop(self):
        while True:
            try:
                await self.scan_log()
            except Exception as e:
                print(f"[LOOP ERROR] {e}")
            await asyncio.sleep(1)
