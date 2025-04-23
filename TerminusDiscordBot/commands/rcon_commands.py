import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option

from utils.embed_factory import create_embed_response

class RconGeneralCommands(commands.Cog):
    def __init__(self, bot: commands.Bot, zrcon):
        self.bot = bot
        self.zrcon = zrcon

    async def _send_embed(self, payload, message):
        embed = create_embed_response("Admin Command", message)
        if isinstance(payload, discord.Interaction):
            await payload.response.send_message(embed=embed)
        elif hasattr(payload, "send"):
            await payload.send(embed=embed)

    @commands.command()
    async def players(self, ctx):
        await self._send_embed(ctx, self.zrcon.players().response)

    @commands.command()
    async def add_all_to_whitelist(self, ctx):
        await self._send_embed(ctx, self.zrcon.addalltowhitelist().response)

    @commands.command()
    async def add_user(self, ctx, username: str, password: str):
        await self._send_embed(ctx, self.zrcon.adduser(username, password).response)

    @commands.command()
    async def add_user_to_whitelist(self, ctx, username: str):
        await self._send_embed(ctx, self.zrcon.addusertowhitelist(username).response)

    @commands.command()
    async def remove_user_from_whitelist(self, ctx, username: str):
        await self._send_embed(ctx, self.zrcon.removeuserfromwhitelist(username).response)

    @commands.command()
    async def ban_id(self, ctx, steam_id: str):
        await self._send_embed(ctx, self.zrcon.banid(steam_id).response)

    @commands.command()
    async def unban_id(self, ctx, steam_id: str):
        await self._send_embed(ctx, self.zrcon.unbanid(steam_id).response)

    @commands.command()
    async def ban_user(self, ctx, username: str):
        await self._send_embed(ctx, self.zrcon.banuser(username).response)

    @commands.command()
    async def unban_user(self, ctx, username: str):
        await self._send_embed(ctx, self.zrcon.unbanuser(username).response)

    @commands.command()
    async def grant_admin(self, ctx, username: str):
        await self._send_embed(ctx, self.zrcon.grantadmin(username).response)

    @commands.command()
    async def remove_admin(self, ctx, username: str):
        await self._send_embed(ctx, self.zrcon.removeadmin(username).response)

    @commands.command()
    async def kick_user(self, ctx, username: str):
        await self._send_embed(ctx, self.zrcon.kickuser(username).response)

    @commands.command()
    async def server_msg(self, ctx, *, message: str):
        await self._send_embed(ctx, self.zrcon.servermsg(message).response)

    @commands.command()
    async def set_access_level(self, ctx, username: str, access_level: str):
        await self._send_embed(ctx, self.zrcon.setaccesslevel(username, access_level).response)

    @commands.command()
    async def thunder(self, ctx, username: str):
        await self._send_embed(ctx, self.zrcon.command("thunder", username).response)

    @commands.command()
    async def add_item(self, ctx, username: str, item: str):
        await self._send_embed(ctx, self.zrcon.additem(username, item).response)

    @commands.command()
    async def add_vehicle(self, ctx, username: str):
        await self._send_embed(ctx, self.zrcon.addvehicle(username).response)

    @commands.command()
    async def add_xp(self, ctx, username: str, perk: str, xp: int):
        await self._send_embed(ctx, self.zrcon.addxp(username, perk, xp).response)

    @commands.command()
    async def alarm(self, ctx):
        await self._send_embed(ctx, self.zrcon.alarm().response)

    @commands.command()
    async def chopper(self, ctx):
        await self._send_embed(ctx, self.zrcon.chopper().response)

    @commands.command()
    async def create_horde(self, ctx, count: str):
        await self._send_embed(ctx, self.zrcon.createhorde(count).response)

    @commands.command()
    async def god_mode(self, ctx, username: str):
        await self._send_embed(ctx, self.zrcon.godmode(username).response)

    @commands.command()
    async def invisible(self, ctx, username: str):
        await self._send_embed(ctx, self.zrcon.invisible(username).response)

    @commands.command()
    async def noclip(self, ctx, username: str):
        await self._send_embed(ctx, self.zrcon.noclip(username).response)

    @commands.command()
    async def reload_options(self, ctx):
        await self._send_embed(ctx, self.zrcon.reloadoptions().response)

    @commands.command()
    async def save(self, ctx):
        await self._send_embed(ctx, self.zrcon.save().response)

    @commands.command()
    async def send_pulse(self, ctx):
        await self._send_embed(ctx, self.zrcon.sendpulse().response)

    @commands.command()
    async def show_options(self, ctx):
        await self._send_embed(ctx, self.zrcon.showoptions().response)

    @commands.command()
    async def start_rain(self, ctx):
        await self._send_embed(ctx, self.zrcon.startrain().response)

    @commands.command()
    async def stop_rain(self, ctx):
        await self._send_embed(ctx, self.zrcon.stoprain().response)

    @commands.command()
    async def teleport(self, ctx, from_user: str, to_user: str):
        await self._send_embed(ctx, self.zrcon.teleport(from_user, to_user).response)

    @commands.command()
    async def teleport_to(self, ctx, x: str, y: str, z: str):
        await self._send_embed(ctx, self.zrcon.teleportto(x, y, z).response)

    @commands.command()
    async def check_update(self, ctx):
        await self._send_embed(ctx, self.zrcon.checkModsNeedUpdate().response)
    @commands.command()
    async def change_option(self, ctx, option: str, new_option: str):
        await self._send_embed(ctx, self.zrcon.changeoption(option, new_option).response)

    @commands.command()
    async def change_password(self, ctx, password: str, new_password: str):
        await self._send_embed(ctx, self.zrcon.changepwd(password, new_password).response)

    @commands.command()
    async def gunshot(self, ctx):
        await self._send_embed(ctx, self.zrcon.gunshot().response)

    @commands.command()
    async def quit(self, ctx):
        await self._send_embed(ctx, self.zrcon.quit().response)

    @commands.command()
    async def release_safehouse(self, ctx):
        await self._send_embed(ctx, self.zrcon.releasesafehouse().response)

    @commands.command()
    async def reload_lua(self, ctx, filename: str):
        await self._send_embed(ctx, self.zrcon.reloadlua(filename).response)

    @commands.command()
    async def replay(self, ctx, username: str, action: str, filename: str):
        await self._send_embed(ctx, self.zrcon.replay(username, action, filename).response)

    @commands.command()
    async def voice_ban(self, ctx, username: str, enable: bool):
        flag = "-true" if enable else "-false"
        await self._send_embed(ctx, self.zrcon.voiceban(username, flag).response)


