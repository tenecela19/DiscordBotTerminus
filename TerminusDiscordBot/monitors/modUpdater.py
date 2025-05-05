import nextcord
from nextcord.ext import commands,task
from nextcord import Interaction, SlashOption
import os
from rcon.source import Client, rcon
import re
from datetime import datetime
import asyncio
import subprocess   
from pydactyl import PterodactylClient
from zomboid_rcon import ZomboidRCON
from dotenv import load_dotenv

load_dotenv()
PANEL_URL = 'http://89.28.237.60/'
API_KEY = 'ptlc_6v3vqpnKrzfX03aUuH6Srnr3ieiLzEsQA0pbI63XshZ'
SERVER_ID = '22aae990-e69e-4482-afcc-12a860687710'
RCON_HOST = os.getenv("RCON_HOST")
RCON_PORT = int(os.getenv("RCON_PORT"))
RCON_PASSWORD = os.getenv("RCON_PASSWORD")
api = PterodactylClient(PANEL_URL, API_KEY)
zrcon = ZomboidRCON(RCON_HOST, RCON_PORT, RCON_PASSWORD)  # Replace with your actual credentials

my_servers = api.client.servers.list_servers()
# Get the unique identifier for the first server.
srv_id = my_servers[0]['attributes']['identifier']
class modUpdater(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = int(os.getenv("DISCORD_CHANNEL_ID", "123456789012345678"))
        self.srv_id = api.client.servers.list_servers()[0]['attributes']['identifier']
        if not self.checkmodsupdate.is_running():
            self.checkmodsupdate.start()

    async def startUpdate(self):
        channel = self.bot.get_channel(self.channel_id)
        if not channel:
            self.bot.log.warning("modUpdater.py : startUpdate : Channel not found.")
            return
        warnings = [
            (120, "5 minutos"),
            (120, "3 minutos"),
            (60,  "1 minuto"),
            (10,  "10 segundos"),
        ]

        for delay, text in warnings:
            msg = f"Se ha detectado una actualizacion en el Workshop. El servidor se reiniciara en {text}"
            await channel.send(msg)
            zrcon.command("servermsg",msg)
            await asyncio.sleep(delay)
        self.bot.log.info("modUpdater.py : Mod update is starting")
        api.client.servers.send_power_action(self.srv_id, "restart")

    @tasks.loop(minutes=5)
    async def checkmodsupdate(self):
        if not RCON_PASSWORD:
            self.bot.log.warning("modUpdater.py : RCON password not set.")
            self.checkmodsupdate.stop()
            return
        try:
            self.bot.log.info("modUpdater.py : Checking for mod updates...")
            zrcon.checkModsNeedUpdate()
        except Exception as e:
            self.bot.log.error(f"modUpdater.py : Error while checking mods: {e}")
            self.checkmodsupdate.stop()
            
            