import discord
import asyncio
import os
import re
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PerkLogMonitor:
    def __init__(self, bot, channel_id, log_dir, srj_grace=10, suspicious_window=5,srj_max_duration=15):
        self.bot = bot
        self.channel_id = channel_id
        self.log_dir = log_dir
        self.srj_grace = srj_grace
        self.suspicious_window = suspicious_window
        self.srj_max_duration = srj_max_duration  # Maximum time in seconds to keep SRJ status (5 minutes default)
        
        # Tracking dictionaries
        self.active_srj_readers = {}  # {steamid: {'start_time': datetime, 'end_time': datetime}}
        self.player_skills = {}       # {steamid: {skill: {'last_level': level, 'last_time': time}}}
        
        # File handling
        self.current_log = None
        self.last_position = None

        self.suspicious_buffer = {}  # {steamid: {'username': str, 'skills': [], 'timestamp': datetime}}
        self.alert_cooldown = 30  # seconds to wait before sending grouped alerts        
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
                r"\[SRJ STOP READING\].*?(?:\((?:stop|forceStop)\))?",
                re.IGNORECASE
            )
        }

    def _parse_log_time(self, time_str):
        """Convert log timestamp string to datetime object"""
        return datetime.strptime(time_str, "%y-%m-%d %H:%M:%S.%f")

    def _cleanup_expired_srj(self, current_time: datetime):
        """Clean up expired SRJ sessions"""
        expired_steamids = []
        
        for steamid, srj_data in self.active_srj_readers.items():
            # Check if max duration exceeded
            if (current_time - srj_data['start_time']).total_seconds() > self.srj_max_duration:
                expired_steamids.append(steamid)
                logger.info(f"SRJ session expired for {steamid} (max duration exceeded)")
            # Check if grace period exceeded
            elif current_time > srj_data['end_time']:
                expired_steamids.append(steamid)
                logger.info(f"SRJ session expired for {steamid} (grace period ended)")
        
        # Remove expired sessions
        for steamid in expired_steamids:
            self.active_srj_readers.pop(steamid, None)
            self.player_skills.pop(steamid, None)  # Reset skill tracking

    def _is_reading_srj(self, steamid: str, current_time: datetime) -> bool:
        """Check if player is currently reading SRJ"""
        if steamid in self.active_srj_readers:
            srj_data = self.active_srj_readers[steamid]
            # Check if within max duration
            if (current_time - srj_data['start_time']).total_seconds() <= self.srj_max_duration:
                return True
            else:
                # Clean up expired SRJ session
                self.active_srj_readers.pop(steamid)
                logger.info(f"SRJ session expired for {steamid}")
        return False

    async def _send_grouped_alert(self, steamid):
        """Send grouped suspicious activity alert to Discord"""
        try:
            if steamid not in self.suspicious_buffer:
                return

            data = self.suspicious_buffer[steamid]
            username = data['username']
            skills = data['skills']

            if not skills:
                return

            channel = self.bot.get_channel(self.channel_id)
            if channel:
                skill_text = "\n".join([
                    f"• {skill} ({old_level} → {new_level}) in {delta:.1f}s"
                    for skill, old_level, new_level, delta in skills
                ])

                embed = discord.Embed(
                    title="🚨 Suspicious Level Gains Detected",
                    description=(
                        f"**Player:** {username}\n"
                        f"**Steam ID:** {steamid}\n\n"
                        f"**Suspicious Skills Gains:**\n{skill_text}"
                    ),
                    color=0xFF5733,
                    timestamp=data['timestamp']
                )
                await channel.send(embed=embed)

            # Clear the buffer after sending
            self.suspicious_buffer.pop(steamid)

        except Exception as e:
            logger.error(f"Failed to send grouped alert: {e}")

    async def _buffer_suspicious_activity(self, steamid, username, skill, old_level, new_level, delta):
        """Buffer suspicious activity for grouped alerts"""
        current_time = datetime.now()

        if steamid not in self.suspicious_buffer:
            self.suspicious_buffer[steamid] = {
                'username': username,
                'skills': [],
                'timestamp': current_time
            }
        
        self.suspicious_buffer[steamid]['skills'].append((skill, old_level, new_level, delta))

        # Send alert if cooldown has passed
        if (current_time - self.suspicious_buffer[steamid]['timestamp']).total_seconds() >= self.alert_cooldown:
            await self._send_grouped_alert(steamid)

    async def process_line(self, line: str):
        """Process a single log line"""
        try:
            # First check for SRJ events
            if match := self.patterns['srj_start'].search(line):
                time = self._parse_log_time(match.group(1))
                steamid = match.group(2)
                username = match.group(3)
                
                self.active_srj_readers[steamid] = {
                    'start_time': time,
                    'end_time': time + timedelta(seconds=self.srj_grace)
                }
                logger.info(f"SRJ start detected for {username} ({steamid})")
                return

            if match := self.patterns['srj_stop'].search(line):
                time = self._parse_log_time(match.group(1))
                steamid = match.group(2)
                if steamid in self.active_srj_readers:
                    self.active_srj_readers.pop(steamid)
                    logger.info(f"SRJ stop detected for {steamid}")
                return

            # Then check for perk changes
            if match := self.patterns['perk'].search(line):
                time = self._parse_log_time(match.group(1))
                steamid = match.group(2)
                username = match.group(3)
                skill = match.group(5)
                new_level = int(match.group(6))
                hours_survived = int(match.group(7))

                # Important: Check SRJ status first
                if self._is_reading_srj(steamid, time):
                    logger.info(f"Ignoring level change for {username} - Currently reading SRJ")
                    return

                # Only then check for suspicious gains
                is_suspicious, delta, old_level = self._is_suspicious_gain(
                    steamid, skill, new_level, time
                )

                if is_suspicious:
                    await self._buffer_suspicious_activity(
                        steamid, username, skill, old_level, new_level, delta
                    )

        except Exception as e:
            logger.error(f"Error processing line: {e}")

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
                embed = discord.Embed(
                    title="Suspicious Level Gain Detected",
                    description=(
                        f"Player: {username}\n"
                        f"Steam ID: {steamid}\n"
                        f"Skill: {skill}\n"
                        f"Level Change: {old_level} → {new_level}\n"
                        f"Time Delta: {delta:.1f}s\n"
                        f"Hours Survived: {hours_survived}"
                    ),
                    color=0xFF5733
                )
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

    # ... (rest of the methods remain the same as in the previous version)
    async def scan_log(self):
        """Scan the log file for new entries"""
        log_path = self._get_latest_log()
        if not log_path:
            return

        try:
            # Handle log file rotation or first run
            if self.current_log != log_path:
                if self.current_log:
                    logger.info(f"Switching to new log file: {log_path}")
                    self.last_position = 0
                else:
                    # First time running - start from end of file
                    logger.info("First run - starting from end of current log")
                    with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
                        f.seek(0, 2)  # Seek to end of file
                        self.last_position = f.tell()
                self.current_log = log_path

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
        logger.info("Starting PerkLogMonitor...")
        while True:
            await self.scan_log()
            
            # Check for any remaining buffered alerts
            current_time = datetime.now()
            for steamid in list(self.suspicious_buffer.keys()):
                if (current_time - self.suspicious_buffer[steamid]['timestamp']).total_seconds() >= self.alert_cooldown:
                    await self._send_grouped_alert(steamid)
            
            await asyncio.sleep(1)

