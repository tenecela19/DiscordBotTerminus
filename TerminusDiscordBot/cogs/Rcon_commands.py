import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
from zomboid_rcon import ZomboidRCON
from dotenv import load_dotenv
import os

load_dotenv()

class Rcon_commands(commands.Cog):
    def __init__(self, bot, zrcon):
        self.bot = bot
        self.zrcon = zrcon
    
    testServerId = 928563012875468801

    @nextcord.slash_command(name="additem", description="Give item to player", guild_ids=[testServerId])
    async def additem(
        self,
        interaction: Interaction,
        user: str = SlashOption(description="In-game username"),
        item: str = SlashOption(description="Item ID")
    ):
        self.zrcon.additem(user, item)
        await interaction.response.send_message(f"✅ Added **{item}** to `{user}`'s inventory!")

    @nextcord.slash_command(name="addvehicle", description="Spawn a vehicle for a player", guild_ids=[testServerId])
    async def addvehicle(
        self,
        interaction: Interaction,
        user: str = SlashOption(description="In-game username")
    ):
        self.zrcon.addvehicle(user)
        await interaction.response.send_message(f"✅ Spawned a vehicle for `{user}`!")

    @nextcord.slash_command(name="addxp", description="Give XP to a player", guild_ids=[testServerId])
    async def addxp(
        self,
        interaction: Interaction,
        user: str = SlashOption(description="In-game username"),
        perk: str = SlashOption(description="Perk name"),
        xp: int = SlashOption(description="Amount of XP")
    ):
        self.zrcon.addxp(user, perk, xp)
        await interaction.response.send_message(f"✅ Gave **{xp} XP** in **{perk}** to `{user}`!")
    
    @nextcord.slash_command(name="alarm", description="Sound a building alarm at your position", guild_ids=[testServerId])
    async def alarm(self, interaction: Interaction):
        self.zrcon.alarm()
        await interaction.response.send_message("✅ Alarm sounded at your current location!")

    @nextcord.slash_command(name="changeoption", description="Change a server option", guild_ids=[testServerId])
    async def changeoption(
        self,
        interaction: Interaction,
        option: str = SlashOption(description="Option name"),
        newoption: str = SlashOption(description="New value")
    ):
        self.zrcon.changeoption(option,newoption)
        await interaction.response.send_message(f"✅ Changed option `{option}` to `{newoption}`!")

    @nextcord.slash_command(name="chopper", description="Trigger helicopter event on random player", guild_ids=[testServerId])
    async def chopper(self, interaction: Interaction):
        self.zrcon.chopper()
        await interaction.response.send_message("✅ Helicopter event triggered on a random player!")

    @nextcord.slash_command(name="changepwd", description="Change your admin password", guild_ids=[testServerId])
    async def changepwd(
        self,
        interaction: Interaction,
        pwd: str = SlashOption(description="Current password"),
        newpwd: str = SlashOption(description="New password")
    ):
        self.zrcon.changepwd(pwd,newpwd)
        await interaction.response.send_message("✅ Admin password changed successfully!")    
    
    @nextcord.slash_command(name="createhorde", description="Spawn a horde near a player", guild_ids=[testServerId])
    async def createhorde(
        self,
        interaction: Interaction,
        number: int = SlashOption(description="Number of zombies")
    ):
        self.zrcon.createhorde(number)
        await interaction.response.send_message(f"✅ Spawned a horde of **{number}** zombies!")
 
    @nextcord.slash_command(name="godmode", description="Toggle godmode for a player", guild_ids=[testServerId])
    async def godmode(
        self,
        interaction: Interaction,
        user: str = SlashOption(description="In-game username")
    ):
        self.zrcon.godmode(user)
        await interaction.response.send_message(f"✅ Toggled godmode for `{user}`!")

    @nextcord.slash_command(name="gunshot", description="Make a gunshot sound near the player", guild_ids=[testServerId])
    async def gunshot(self, interaction: Interaction):
        self.zrcon.gunshot()
        await interaction.response.send_message("✅ Gunshot sound triggered!")

    @nextcord.slash_command(name="help", description="Display native RCON help menu", guild_ids=[testServerId])
    async def command_help(self, interaction: Interaction):
        self.zrcon.help()
        await interaction.response.send_message("✅ Help menu opened. Check your client or console!")

    @nextcord.slash_command(name="invisible", description="Make a player invisible to zombies", guild_ids=[testServerId])
    async def invisible(
        self,
        interaction: Interaction,
        user: str = SlashOption(description="In-game username")
    ):
        self.zrcon.invisible(user)
        await interaction.response.send_message(f"✅ `{user}` is now invisible to zombies!")

    @nextcord.slash_command(name="noclip", description="Allow player to walk through objects", guild_ids=[testServerId])
    async def noclip(
        self,
        interaction: Interaction,
        user: str = SlashOption(description="In-game username")
    ):
        self.zrcon.noclip(user)
        await interaction.response.send_message(f"✅ Noclip enabled for `{user}`!")

    @nextcord.slash_command(name="reloadoptions", description="Reload server options", guild_ids=[testServerId])
    async def reloadoptions(self, interaction: Interaction):
        self.zrcon.reloadoptions()
        await interaction.response.send_message("✅ Server options reloaded!")
    @nextcord.slash_command(name="save", description="Save the world", guild_ids=[testServerId])
    async def save(self, interaction: Interaction):
        self.zrcon.save()
        await interaction.response.send_message("✅ World saved successfully!")
        
    @nextcord.slash_command(name="showoptions", description="Show current server options", guild_ids=[testServerId])
    async def showoptions(self, interaction: Interaction):
        self.zrcon.showoptions()
        await interaction.response.send_message("✅ Displayed server options (check client console)")

    @nextcord.slash_command(name="startrain", description="Start rain on the server", guild_ids=[testServerId])
    async def startrain(self, interaction: Interaction):
        self.zrcon.startrain()
        await interaction.response.send_message("🌧️ Rain started!")

    @nextcord.slash_command(name="stoprain", description="Stop rain on the server", guild_ids=[testServerId])
    async def stoprain(self, interaction: Interaction):
        self.zrcon.stoprain()
        await interaction.response.send_message("🌤️ Rain stopped!")

    @nextcord.slash_command(name="teleport", description="Teleport one player to another", guild_ids=[testServerId])
    async def teleport(
        self,
        interaction: Interaction,
        user: str = SlashOption(description="Player to teleport"),
        touser: str = SlashOption(description="Destination player")
    ):
        self.zrcon.teleport(user,touser)
        await interaction.response.send_message(f"✅ Teleported `{user}` to `{toUser}`!")
    
    
    @nextcord.slash_command(name="addalltowhitelist", description="Add all connected users with password to whitelist", guild_ids=[testServerId])
    async def addalltowhitelist(self, interaction: Interaction):
        self.zrcon.addalltowhitelist()
        await interaction.response.send_message("✅ All connected users added to whitelist!")

    @nextcord.slash_command(name="adduser", description="Add a new user to whitelist", guild_ids=[testServerId])
    async def adduser(
        self,
        interaction: Interaction,
        user: str = SlashOption(description="Username"),
        pwd: str = SlashOption(description="Password")
    ):
        self.zrcon.adduser(user, pwd)
        await interaction.response.send_message(f"✅ User `{user}` added to whitelist!")

    @nextcord.slash_command(name="addusertowhitelist", description="Add a single user to whitelist", guild_ids=[testServerId])
    async def addusertowhitelist(
        self,
        interaction: Interaction,
        user: str = SlashOption(description="Username")
    ):
        self.zrcon.addusertowhitelist(user)
        await interaction.response.send_message(f"✅ Added `{user}` to whitelist!")

    @nextcord.slash_command(name="removeuserfromwhitelist", description="Remove user from whitelist", guild_ids=[testServerId])
    async def removeuserfromwhitelist(
        self,
        interaction: Interaction,
        user: str = SlashOption(description="Username")
    ):
        self.zrcon.removeuserfromwhitelist(user)
        await interaction.response.send_message(f"✅ Removed `{user}` from whitelist!")

    @nextcord.slash_command(name="banid", description="Ban a Steam ID", guild_ids=[testServerId])
    async def banid(
        self,
        interaction: Interaction,
        steamid: str = SlashOption(description="Steam ID")
    ):
        self.zrcon.banid(steamid)
        await interaction.response.send_message(f"✅ Banned Steam ID `{steamid}`!")

    @nextcord.slash_command(name="unbanid", description="Unban a Steam ID", guild_ids=[testServerId])
    async def unbanid(
        self,
        interaction: Interaction,
        steamid: str = SlashOption(description="Steam ID")
    ):
        self.zrcon.unbanid(steamid)
        await interaction.response.send_message(f"✅ Unbanned Steam ID `{steamid}`!")

    @nextcord.slash_command(name="banuser", description="Ban a user", guild_ids=[testServerId])
    async def banuser(
        self,
        interaction: Interaction,
        user: str = SlashOption(description="Username")
    ):
        self.zrcon.banuser(user)
        await interaction.response.send_message(f"✅ Banned user `{user}`!")

    @nextcord.slash_command(name="unbanuser", description="Unban a user", guild_ids=[testServerId])
    async def unbanuser(
        self,
        interaction: Interaction,
        user: str = SlashOption(description="Username")
    ):
        self.zrcon.unbanuser(user)
        await interaction.response.send_message(f"✅ Unbanned user `{user}`!")

    @nextcord.slash_command(name="checkmodsneedupdate", description="Check if any mods need an update", guild_ids=[testServerId])
    async def checkmodsneedupdate(self, interaction: Interaction):
        self.zrcon.checkModsNeedUpdate()
        await interaction.response.send_message("✅ Checked mod updates. See log file for results.")

    @nextcord.slash_command(name="grantadmin", description="Grant admin to a user", guild_ids=[testServerId])
    async def grantadmin(
        self,
        interaction: Interaction,
        user: str = SlashOption(description="Username")
    ):
        self.zrcon.grantadmin(user)
        await interaction.response.send_message(f"✅ Granted admin rights to `{user}`!")

    @nextcord.slash_command(name="removeadmin", description="Remove admin from a user", guild_ids=[testServerId])
    async def removeadmin(
        self,
        interaction: Interaction,
        user: str = SlashOption(description="Username")
    ):
        self.zrcon.removeadmin(user)
        await interaction.response.send_message(f"✅ Removed admin rights from `{user}`!")

    @nextcord.slash_command(name="kickuser", description="Kick a user from the server", guild_ids=[testServerId])
    async def kickuser(
        self,
        interaction: Interaction,
        user: str = SlashOption(description="Username")
    ):
        self.zrcon.kickuser(user)
        await interaction.response.send_message(f"✅ Kicked `{user}` from the server!")

    @nextcord.slash_command(name="players", description="List connected players", guild_ids=[testServerId])
    async def players(self, interaction: Interaction):
        result = self.zrcon.players().response
        await interaction.response.send_message(f"✅ Connected players:\n```{result}```")

    @nextcord.slash_command(name="servermsg", description="Send a message to all players", guild_ids=[testServerId])
    async def servermsg(
        self,
        interaction: Interaction,
        message: str = SlashOption(description="Message to broadcast")
    ):
        self.zrcon.servermsg(message)
        await interaction.response.send_message("✅ Message sent to all players!")

    @nextcord.slash_command(name="setaccesslevel", description="Set access level of a player", guild_ids=[testServerId])
    async def setaccesslevel(
        self,
        interaction: Interaction,
        user: str = SlashOption(description="Username"),
        level: str = SlashOption(description="Access level (admin, moderator, overseer, gm, observer)")
    ):
        self.zrcon.setaccesslevel(user,level)
        await interaction.response.send_message(f"✅ Access level for `{user}` set to `{level}`!")

    @nextcord.slash_command(name="voiceban", description="Toggle voice ban for user", guild_ids=[testServerId])
    async def voiceban(
        self,
        interaction: Interaction,
        user: str = SlashOption(description="Username"),
        toggle: str = SlashOption(description="-true to ban, -false to unban")
    ):
        self.zrcon.voiceban(user,toggle)
        await interaction.response.send_message(f"✅ Voice ban for `{user}` set to `{toggle}`!")
        
def setup(bot):
    RCON_HOST = os.getenv("RCON_HOST")
    RCON_PORT = int(os.getenv("RCON_PORT"))
    RCON_PASSWORD = os.getenv("RCON_PASSWORD")
    zrcon = ZomboidRCON(RCON_HOST, RCON_PORT, RCON_PASSWORD)  # Replace with your actual credentials
    bot.add_cog(Rcon_commands(bot, zrcon))  # ✅ pass zrcon to the cog