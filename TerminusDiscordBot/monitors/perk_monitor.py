import nextcord
import asyncio
import os
import re
from datetime import datetime, timedelta
import logging
from utils.admin_bypass import AdminBypassManager
from utils.embed_factory import create_embed_response

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PerkLogMonitor:
    def __init__(self, bot, channel_id, log_dir, admin_bypass, srj_grace=10, suspicious_window=5, srj_max_duration=15):
        self.bot = bot
        self.channel_id = channel_id
        self.log_dir = log_dir
        self.srj_grace = srj_grace
        self.suspicious_window = suspicious_window
        self.srj_max_duration = srj_max_duration
        
        # Memory management parameters
        self.max_cached_players = 1000  # Maximum number of players to keep in memory
        self.cleanup_interval = 300     # Cleanup every 5 minutes
        
        # Tracking dictionaries
        self.active_srj_readers = {}    # {steamid: {'start_time': datetime, 'end_time': datetime}}
        self.player_skills = {}         # {steamid: {skill: {'last_level': level, 'last_time': time}}}
        
        # File handling
        self.current_log = None
        self.last_position = None
        self._last_alert_time = datetime.now()

        self.suspicious_buffer = {}      # {steamid: {'username': str, 'skills': [], 'timestamp': datetime}}
        self.alert_cooldown = 30        # seconds to wait before sending grouped alerts
        self.admin_bypass = admin_bypass
     
        # Regex patterns - compiled once at initialization
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
        try:
            return datetime.strptime(time_str, "%y-%m-%d %H:%M:%S.%f")
        except ValueError as e:
            logger.error(f"Error parsing time string '{time_str}': {e}")
            return datetime.now()

    def _cleanup_memory(self):
        """Clean up old data from memory"""
        try:
            current_time = datetime.now()
            
            # Clean up SRJ readers
            self._cleanup_expired_srj(current_time)
            
            # Clean up old player skills
            if len(self.player_skills) > self.max_cached_players:
                # Remove oldest entries
                sorted_players = sorted(
                    self.player_skills.items(),
                    key=lambda x: max(skill['last_time'] for skill in x[1].values())
                )
                to_remove = len(self.player_skills) - self.max_cached_players
                for steamid, _ in sorted_players[:to_remove]:
                    del self.player_skills[steamid]
            
            # Clean up suspicious buffer
            expired_buffers = [
                steamid for steamid, data in self.suspicious_buffer.items()
                if (current_time - data['timestamp']).total_seconds() > self.alert_cooldown * 2
            ]
            for steamid in expired_buffers:
                del self.suspicious_buffer[steamid]
                
        except Exception as e:
            logger.error(f"Error during memory cleanup: {e}")

    def _cleanup_expired_srj(self, current_time: datetime):
        """Clean up expired SRJ sessions"""
        try:
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
                
        except Exception as e:
            logger.error(f"Error cleaning up expired SRJ sessions: {e}")

    def _is_reading_srj(self, steamid: str, current_time: datetime) -> bool:
        """Check if player is currently reading SRJ"""
        try:
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
        except Exception as e:
            logger.error(f"Error checking SRJ status: {e}")
            return False

    async def _send_grouped_alert(self, steamid):
        """Send grouped suspicious activity alert to Discord"""
        try:
            # Rate limiting
            current_time = datetime.now()
            if (current_time - self._last_alert_time).total_seconds() < 1:
                await asyncio.sleep(1)  # Prevent alert spam
            
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
                
                message = (
                    f"**Player:** {username}\n"
                    f"**Steam ID:** {steamid}\n\n"
                    f"**Suspicious Skills Gains:**\n{skill_text}"
                )              
                
                embed = create_embed_response(
                    title="🚨 Suspicious Level Gains Detected",
                    message=message,
                    color=0xFF5733,
                    code_block=False,
                    timestamp=data['timestamp']
                )
                await channel.send(embed=embed)
                self._last_alert_time = current_time

            # Clear the buffer after sending
            self.suspicious_buffer.pop(steamid)

        except Exception as e:
            logger.error(f"Failed to send grouped alert: {e}")

    async def _buffer_suspicious_activity(self, steamid, username, skill, old_level, new_level, delta):
        """Buffer suspicious activity for grouped alerts"""
        try:
            current_time = datetime.now()
            if self.admin_bypass.is_bypassed(username):
                logger.info(f"Skipping suspicious buffer for bypassed user {username}")
                return

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
                
        except Exception as e:
            logger.error(f"Error buffering suspicious activity: {e}")

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
        try:
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
            
        except Exception as e:
            logger.error(f"Error checking suspicious gain: {e}")
            return False, 0, new_level
        
    def _get_latest_log(self):
        """Get the most recent log file"""
        try:
            if not os.path.exists(self.log_dir):
                logger.error(f"Log directory not found: {self.log_dir}")
                return None

            log_files = [
                f for f in os.listdir(self.log_dir)
                if f.endswith('.txt') and 'player' in f.lower()
            ]
            
            if not log_files:
                return None

            latest_log = max(
                log_files,
                key=lambda x: os.path.getmtime(os.path.join(self.log_dir, x))
            )
            return os.path.join(self.log_dir, latest_log)
            
        except Exception as e:
            logger.error(f"Error getting latest log: {e}")
            return None

    async def scan_log(self):
        """Scan the log file for new entries"""
        try:
            # Get the latest log file
            latest_log = self._get_latest_log()
            if not latest_log:
                await asyncio.sleep(5)  # Wait before retry
                return

            # Check if log file has changed
            if latest_log != self.current_log:
                self.current_log = latest_log
                self.last_position = 0
                logger.info(f"Switched to new log file: {self.current_log}")

            # Open and read the file
            if not os.path.exists(self.current_log):
                logger.error(f"Log file not found: {self.current_log}")
                return

            with open(self.current_log, 'r', encoding='utf-8') as f:
                if self.last_position:
                    f.seek(self.last_position)
                
                while True:
                    line = f.readline()
                    if not line:
                        self.last_position = f.tell()
                        break
                    
                    await self.process_line(line.strip())
                    
        except Exception as e:
            logger.error(f"Error scanning log: {e}")
            self.last_position = None  # Reset position on error
            await asyncio.sleep(5)  # Wait before retry

    async def loop(self):
        """Main monitoring loop"""
        last_cleanup = datetime.now()
        
        while True:
            try:
                # Regular cleanup
                current_time = datetime.now()
                if (current_time - last_cleanup).total_seconds() > self.cleanup_interval:
                    self._cleanup_memory()
                    last_cleanup = current_time

                # Process logs
                await self.scan_log()
                
                # Add delay to prevent CPU overuse
                await asyncio.sleep(1)
                
            except Exception as e:
                logger.error(f"Error in monitor loop: {e}")
                await asyncio.sleep(5)  # Wait longer on error
