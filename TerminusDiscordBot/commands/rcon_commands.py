import discord
from discord import app_commands
from discord.ext import commands
from utils.embed_factory import create_embed_response

class RconGeneralCommands(commands.Cog):
    def __init__(self, bot: commands.Bot, zrcon):
        self.bot = bot
        self.zrcon = zrcon

    async def _send_embed(self, interaction: discord.Interaction, message):
        embed = create_embed_response("Admin Command", message)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="players", description="List connected players")
    async def players(self, interaction: discord.Interaction):
        await self._send_embed(interaction, self.zrcon.players().response)

    @app_commands.command(name="add_all_to_whitelist", description="Add all users to whitelist")
    async def add_all_to_whitelist(self, interaction: discord.Interaction):
        await self._send_embed(interaction, self.zrcon.addalltowhitelist().response)

    @app_commands.command(name="add_user", description="Add a user with password")
    @app_commands.describe(username="Username", password="Password")
    async def add_user(self, interaction: discord.Interaction, username: str, password: str):
        await self._send_embed(interaction, self.zrcon.adduser(username, password).response)

    @app_commands.command(name="add_user_to_whitelist", description="Whitelist a user")
    @app_commands.describe(username="Username")
    async def add_user_to_whitelist(self, interaction: discord.Interaction, username: str):
        await self._send_embed(interaction, self.zrcon.addusertowhitelist(username).response)

    @app_commands.command(name="remove_user_from_whitelist", description="Remove user from whitelist")
    @app_commands.describe(username="Username")
    async def remove_user_from_whitelist(self, interaction: discord.Interaction, username: str):
        await self._send_embed(interaction, self.zrcon.removeuserfromwhitelist(username).response)

    @app_commands.command(name="ban_id", description="Ban a user by Steam ID")
    async def ban_id(self, interaction: discord.Interaction, steam_id: str):
        await self._send_embed(interaction, self.zrcon.banid(steam_id).response)

    @app_commands.command(name="unban_id", description="Unban a user by Steam ID")
    async def unban_id(self, interaction: discord.Interaction, steam_id: str):
        await self._send_embed(interaction, self.zrcon.unbanid(steam_id).response)

    @app_commands.command(name="ban_user", description="Ban a user")
    async def ban_user(self, interaction: discord.Interaction, username: str):
        await self._send_embed(interaction, self.zrcon.banuser(username).response)

    @app_commands.command(name="unban_user", description="Unban a user")
    async def unban_user(self, interaction: discord.Interaction, username: str):
        await self._send_embed(interaction, self.zrcon.unbanuser(username).response)

    @app_commands.command(name="grant_admin", description="Grant admin to user")
    async def grant_admin(self, interaction: discord.Interaction, username: str):
        await self._send_embed(interaction, self.zrcon.grantadmin(username).response)

    @app_commands.command(name="remove_admin", description="Remove admin from user")
    async def remove_admin(self, interaction: discord.Interaction, username: str):
        await self._send_embed(interaction, self.zrcon.removeadmin(username).response)

    @app_commands.command(name="kick_user", description="Kick a user")
    async def kick_user(self, interaction: discord.Interaction, username: str):
        await self._send_embed(interaction, self.zrcon.kickuser(username).response)

    @app_commands.command(name="server_msg", description="Send a message to the server")
    @app_commands.describe(message="Message to broadcast")
    async def server_msg(self, interaction: discord.Interaction, message: str):
        await self._send_embed(interaction, self.zrcon.servermsg(message).response)

    @app_commands.command(name="set_access_level", description="Set user access level")
    @app_commands.describe(username="Username", access_level="Access level: admin, moderator, overseer, gm, observer")
    async def set_access_level(self, interaction: discord.Interaction, username: str, access_level: str):
        await self._send_embed(interaction, self.zrcon.setaccesslevel(username, access_level).response)

    @app_commands.command(name="voice_ban", description="Enable or disable voice ban for a user")
    @app_commands.describe(username="Username", enable="Enable or disable the ban")
    async def voice_ban(self, interaction: discord.Interaction, username: str, enable: bool):
        flag = "-true" if enable else "-false"
        await self._send_embed(interaction, self.zrcon.voiceban(username, flag).response)

    @app_commands.command(name="thunder", description="Summon thunder on user")
    async def thunder(self, interaction: discord.Interaction, username: str):
        await self._send_embed(interaction, self.zrcon.command("thunder", username).response)

    @app_commands.command(name="add_item", description="Give item to user")
    async def add_item(self, interaction: discord.Interaction, username: str, item: str):
        await self._send_embed(interaction, self.zrcon.additem(username, item).response)

    @app_commands.command(name="add_vehicle", description="Give vehicle to user")
    async def add_vehicle(self, interaction: discord.Interaction, username: str):
        await self._send_embed(interaction, self.zrcon.addvehicle(username).response)

    @app_commands.command(name="add_xp", description="Give XP to user")
    async def add_xp(self, interaction: discord.Interaction, username: str, perk: str, xp: int):
        await self._send_embed(interaction, self.zrcon.addxp(username, perk, xp).response)

    @app_commands.command(name="alarm", description="Trigger alarm")
    async def alarm(self, interaction: discord.Interaction):
        await self._send_embed(interaction, self.zrcon.alarm().response)

    @app_commands.command(name="chopper", description="Summon helicopter")
    async def chopper(self, interaction: discord.Interaction):
        await self._send_embed(interaction, self.zrcon.chopper().response)

    @app_commands.command(name="create_horde", description="Create zombie horde")
    async def create_horde(self, interaction: discord.Interaction, count: str):
        await self._send_embed(interaction, self.zrcon.createhorde(count).response)

    @app_commands.command(name="god_mode", description="Enable god mode for user")
    async def god_mode(self, interaction: discord.Interaction, username: str):
        await self._send_embed(interaction, self.zrcon.godmode(username).response)

    @app_commands.command(name="invisible", description="Make user invisible to zombies")
    async def invisible(self, interaction: discord.Interaction, username: str):
        await self._send_embed(interaction, self.zrcon.invisible(username).response)

    @app_commands.command(name="noclip", description="Enable noclip for user")
    async def noclip(self, interaction: discord.Interaction, username: str):
        await self._send_embed(interaction, self.zrcon.noclip(username).response)

    @app_commands.command(name="reload_options", description="Reload server options")
    async def reload_options(self, interaction: discord.Interaction):
        await self._send_embed(interaction, self.zrcon.reloadoptions().response)

    @app_commands.command(name="change_option", description="Change a server option")
    async def change_option(self, interaction: discord.Interaction, option: str, new_option: str):
        await self._send_embed(interaction, self.zrcon.changeoption(option, new_option).response)

    @app_commands.command(name="change_password", description="Change your password")
    async def change_password(self, interaction: discord.Interaction, password: str, new_password: str):
        await self._send_embed(interaction, self.zrcon.changepwd(password, new_password).response)

    @app_commands.command(name="gunshot", description="Trigger gunshot event")
    async def gunshot(self, interaction: discord.Interaction):
        await self._send_embed(interaction, self.zrcon.gunshot().response)

    @app_commands.command(name="quit", description="Save and quit server")
    async def quit(self, interaction: discord.Interaction):
        await self._send_embed(interaction, self.zrcon.quit().response)

    @app_commands.command(name="release_safehouse", description="Release your safehouse")
    async def release_safehouse(self, interaction: discord.Interaction):
        await self._send_embed(interaction, self.zrcon.releasesafehouse().response)

    @app_commands.command(name="reload_lua", description="Reload a Lua script")
    async def reload_lua(self, interaction: discord.Interaction, filename: str):
        await self._send_embed(interaction, self.zrcon.reloadlua(filename).response)

    @app_commands.command(name="save", description="Save world")
    async def save(self, interaction: discord.Interaction):
        await self._send_embed(interaction, self.zrcon.save().response)

    @app_commands.command(name="send_pulse", description="Toggle performance pulse")
    async def send_pulse(self, interaction: discord.Interaction):
        await self._send_embed(interaction, self.zrcon.sendpulse().response)

    @app_commands.command(name="show_options", description="Show server options")
    async def show_options(self, interaction: discord.Interaction):
        await self._send_embed(interaction, self.zrcon.showoptions().response)

    @app_commands.command(name="start_rain", description="Start rain")
    async def start_rain(self, interaction: discord.Interaction):
        await self._send_embed(interaction, self.zrcon.startrain().response)

    @app_commands.command(name="stop_rain", description="Stop rain")
    async def stop_rain(self, interaction: discord.Interaction):
        await self._send_embed(interaction, self.zrcon.stoprain().response)

    @app_commands.command(name="teleport", description="Teleport one user to another")
    async def teleport(self, interaction: discord.Interaction, from_user: str, to_user: str):
        await self._send_embed(interaction, self.zrcon.teleport(from_user, to_user).response)

    @app_commands.command(name="teleport_to", description="Teleport user to coordinates")
    async def teleport_to(self, interaction: discord.Interaction, x: str, y: str, z: str):
        await self._send_embed(interaction, self.zrcon.teleportto(x, y, z).response)

    @app_commands.command(name="check_update", description="Check mod updates")
    async def check_update(self, interaction: discord.Interaction):
        await self._send_embed(interaction, self.zrcon.checkModsNeedUpdate().response)
