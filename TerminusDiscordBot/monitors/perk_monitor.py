import nextcord
import asyncio
import os
import re
from datetime import datetime, timedelta
from utils.embed_factory import create_embed_response
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PerkLogMonitor:
    def __init__(self, bot, channel_id, log_dir, srj_grace=10, suspicious_window=5):
        self.bot = bot
        self.channel_id = channel_id
        self.log_dir = log_dir
        self.srj_grace = srj_grace
        self.suspicious_window = suspicious_window
        
        # Tracking dictionaries
        self.active_srj_readers = {}  # {steamid: end_time}
        self.player_skills = {}       # {steamid: {skill: {'last_level': level, 'last_time': time}}}
        
        # File handling
        self.current_log = None
        self.last_position = 0
        
        # Regex patterns
        self.patterns = {
            'perk': re.compile(
                r"\[(\d{2}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3})\] "
                r"\[(\d+)\]"           # Steam ID
                r"\[(.+?)\]"           # Username
                r"\[(.+?)\]"           # Action
                r"\[Level Changed\]"
                r"\[(\w+)\]"           # Skill
                r"\[(\d+)\]"           # New Level
                r"\[Hours Survived: (\d+)\]"
            ),
            'srj_start': re.compile(
                r"\[(\d{2}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3})\] "
                r"\[(\d+)\]"           # Steam ID
                r"\[(.+?)\].*?"        # Username
                r"\[SRJ START READING\]",
                re.IGNORECASE
            ),
            'srj_stop': re.compile(
                r"\[(\d{2}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3})\] "
                r"\[(\d+)\]"           # Steam ID
                r"\[(.+?)\].*?"        # Username
                r"\[SRJ STOP READING\]",
                re.IGNORECASE
            )
        }

    def _parse_log_time(self, time_str):
        """Convert log timestamp string to datetime object"""
        return datetime.strptime(time_str, "%y-%m-%d %H:%M:%S.%f")

    def _is_reading_srj(self, steamid: str, current_time: datetime) -> bool:
        """Check if player is currently reading SRJ"""
        if steamid in self.active_srj_readers:
            end_time = self.active_srj_readers[steamid]
            if current_time <= end_time:
                return True
            else:
                del self.active_srj_readers[steamid]
        return False

    def _is_suspicious_gain(self, steamid: str, skill: str, new_level: int, 
                          current_time: datetime) -> tuple[bool, float, int]:
        """
        Determine if a level gain is suspicious
        Returns: (is_suspicious, time_delta, old_level)
        """
        if steamid not in self.player_skills:
            self.player_skills[steamid] = {}
        
        if skill not in self.player_skills[steamid]:
            self.player_skills[steamid][skill] = {
                'last_level': new_level,
                'last_time': current_time
            }
            return False, 0, new_level

        skill_data = self.player_skills[steamid][skill]
        old_level = skill_data['last_level']
        time_delta = (current_time - skill_data['last_time']).total_seconds()

        # Update tracking
        skill_data.update({
            'last_level': new_level,
            'last_time': current_time
        })

        # Skip if level decreased (might be death/reset)
        if new_level <= old_level:
            return False, time_delta, old_level

        # Check if gain is suspicious
        if time_delta < self.suspicious_window:
            # Special case for Engineering skill
            if skill.lower() == "engineering" and old_level >= 5:
                return False, time_delta, old_level
            return True, time_delta, old_level

        return False, time_delta, old_level

    async def _send_alert(self, steamid, username, skill, old_level, new_level, 
                         delta, hours_survived):
        """Send suspicious activity alert to Discord"""
        try:
            channel = self.bot.get_channel(self.channel_id)
            if channel:
                formatted = (
                    f"Player: {username}\n"
                    f"Steam ID: {steamid}\n"
                    f"Skill: {skill}\n"
                    f"Level Change: {old_level} → {new_level}\n"
                    f"Time Delta: {delta:.1f}s\n"
                    f"Hours Survived: {hours_survived}"
                )
                embed = create_embed_response("Suspicious Level Gain Detected", formatted, color=0xFF5733, code_block=False)
                await channel.send(embed=embed)
        except Exception as e:
            logger.error(f"Failed to send alert: {e}")

    def _get_latest_log(self):
        """Get the most recent log file"""
        try:
            logs = [f for f in os.listdir(self.log_dir) if f.endswith("_PerkLog.txt")]
            if not logs:
                return None
            return os.path.join(self.log_dir, sorted(logs)[-1])
        except Exception as e:
            logger.error(f"Error finding log file: {e}")
            return None

    async def process_line(self, line: str):
        """Process a single log line"""
        try:
            # Check for SRJ start
            if match := self.patterns['srj_start'].search(line):
                time = self._parse_log_time(match.group(1))
                steamid = match.group(2)
                self.active_srj_readers[steamid] = time + timedelta(seconds=self.srj_grace)
                logger.debug(f"SRJ start detected for {steamid}")
                return

            # Check for SRJ stop
            if match := self.patterns['srj_stop'].search(line):
                steamid = match.group(2)
                self.active_srj_readers.pop(steamid, None)
                self.player_skills.pop(steamid, None)  # Reset skill tracking
                logger.debug(f"SRJ stop detected for {steamid}")
                return

            # Check for perk changes
            if match := self.patterns['perk'].search(line):
                time = self._parse_log_time(match.group(1))
                steamid = match.group(2)
                username = match.group(3)
                skill = match.group(5)
                new_level = int(match.group(6))
                hours_survived = int(match.group(7))

                # Skip if player is reading SRJ
                if self._is_reading_srj(steamid, time):
                    return

                # Check for suspicious gains
                is_suspicious, delta, old_level = self._is_suspicious_gain(
                    steamid, skill, new_level, time
                )

                if is_suspicious:
                    await self._send_alert(
                        steamid, username, skill, old_level, new_level, 
                        delta, hours_survived
                    )

        except Exception as e:
            logger.error(f"Error processing line: {e}")

    async def scan_log(self):
        """Scan the log file for new entries"""
        log_path = self._get_latest_log()
        if not log_path:
            return

        try:
            # Handle log file rotation
            if self.current_log != log_path:
                if self.current_log:
                    logger.info(f"Switching to new log file: {log_path}")
                self.current_log = log_path
                self.last_position = 0

            with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
                if self.last_position > 0:
                    f.seek(self.last_position)
                
                for line in f:
                    await self.process_line(line.strip())
                
                self.last_position = f.tell()

        except Exception as e:
            logger.error(f"Error scanning log: {e}")

    async def loop(self):
        """Main monitoring loop"""
        while True:
            await self.scan_log()
            await asyncio.sleep(1)
