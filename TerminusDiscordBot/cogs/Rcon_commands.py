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
        result = self.zrcon.additem(user, item)
        emoji = "✅" if getattr(result, "success", True) else "❌"
        await interaction.response.send_message(f"{emoji} {result.response}")

    @nextcord.slash_command(name="addvehicle", description="Spawn a vehicle for a player", guild_ids=[testServerId])
    async def addvehicle(
        self,
        interaction: Interaction,
        user: str = SlashOption(description="In-game username")
    ):
        result = self.zrcon.addvehicle(user)
        emoji = "✅" if getattr(result, "success", True) else "❌"
        await interaction.response.send_message(f"{emoji} {result.response}")

    @nextcord.slash_command(name="addxp", description="Give XP to a player", guild_ids=[testServerId])
    async def addxp(
        self,
        interaction: Interaction,
        user: str = SlashOption(description="In-game username"),
        perk: str = SlashOption(description="Perk name"),
        xp: int = SlashOption(description="Amount of XP")
    ):
        result = self.zrcon.addxp(user, perk, xp)
        emoji = "✅" if getattr(result, "success", True) else "❌"
        await interaction.response.send_message(f"{emoji} {result.response}")
    
    @nextcord.slash_command(name="alarm", description="Sound a building alarm at your position", guild_ids=[testServerId])
    async def alarm(self, interaction: Interaction):
        result = self.zrcon.alarm()
        emoji = "✅" if getattr(result, "success", True) else "❌"
        await interaction.response.send_message(f"{emoji} {result.response}")

    @nextcord.slash_command(name="changeoption", description="Change a server option", guild_ids=[testServerId])
    async def changeoption(
        self,
        interaction: Interaction,
        option: str = SlashOption(description="Option name"),
        newoption: str = SlashOption(description="New value")
    ):
        result = self.zrcon.changeoption(option,newoption)
        emoji = "✅" if getattr(result, "success", True) else "❌"
        await interaction.response.send_message(f"{emoji} {result.response}")

    @nextcord.slash_command(name="chopper", description="Trigger helicopter event on random player", guild_ids=[testServerId])
    async def chopper(self, interaction: Interaction):
        result = self.zrcon.chopper()
        emoji = "✅" if getattr(result, "success", True) else "❌"
        await interaction.response.send_message(f"{emoji} {result.response}")

    @nextcord.slash_command(name="changepwd", description="Change your admin password", guild_ids=[testServerId])
    async def changepwd(
        self,
        interaction: Interaction,
        pwd: str = SlashOption(description="Current password"),
        newpwd: str = SlashOption(description="New password")
    ):
        result = self.zrcon.changepwd(pwd,newpwd)
        emoji = "✅" if getattr(result, "success", True) else "❌"
        await interaction.response.send_message(f"{emoji} {result.response}")    
    
    @nextcord.slash_command(name="createhorde", description="Spawn a horde near a player", guild_ids=[testServerId])
    async def createhorde(
        self,
        interaction: Interaction,
        number: int = SlashOption(description="Number of zombies")
    ):
        result = self.zrcon.createhorde(number)
        emoji = "✅" if getattr(result, "success", True) else "❌"
        await interaction.response.send_message(f"{emoji} {result.response}")
 
    @nextcord.slash_command(name="godmode", description="Toggle godmode for a player", guild_ids=[testServerId])
    async def godmode(
        self,
        interaction: Interaction,
        user: str = SlashOption(description="In-game username")
    ):
        result = self.zrcon.godmode(user)
        emoji = "✅" if getattr(result, "success", True) else "❌"
        await interaction.response.send_message(f"{emoji} {result.response}")

    @nextcord.slash_command(name="gunshot", description="Make a gunshot sound near the player", guild_ids=[testServerId])
    async def gunshot(self, interaction: Interaction):
        result= self.zrcon.gunshot()
        emoji = "✅" if getattr(result, "success", True) else "❌"
        await interaction.response.send_message(f"{emoji} {result.response}")

    @nextcord.slash_command(name="help", description="Display native RCON help menu", guild_ids=[testServerId])
    async def command_help(self, interaction: Interaction):
        result = self.zrcon.help()
        emoji = "✅" if getattr(result, "success", True) else "❌"
        await interaction.response.send_message(f"{emoji} {result.response}")
    @nextcord.slash_command(name="invisible", description="Make a player invisible to zombies", guild_ids=[testServerId])
    async def invisible(
        self,
        interaction: Interaction,
        user: str = SlashOption(description="In-game username")
    ):
        result = self.zrcon.invisible(user)
        emoji = "✅" if getattr(result, "success", True) else "❌"
        await interaction.response.send_message(f"{emoji} {result.response}")

    @nextcord.slash_command(name="noclip", description="Allow player to walk through objects", guild_ids=[testServerId])
    async def noclip(
        self,
        interaction: Interaction,
        user: str = SlashOption(description="In-game username")
    ):
        result = self.zrcon.noclip(user)
        emoji = "✅" if getattr(result, "success", True) else "❌"
        await interaction.response.send_message(f"{emoji} {result.response}")

    @nextcord.slash_command(name="reloadoptions", description="Reload server options", guild_ids=[testServerId])
    async def reloadoptions(self, interaction: Interaction):
        result = self.zrcon.reloadoptions()
        emoji = "✅" if getattr(result, "success", True) else "❌"
        await interaction.response.send_message(f"{emoji} {result.response}")
    @nextcord.slash_command(name="save", description="Save the world", guild_ids=[testServerId])
    async def save(self, interaction: Interaction):
        result = self.zrcon.save()
        emoji = "✅" if getattr(result, "success", True) else "❌"
        await interaction.response.send_message(f"{emoji} {result.response}")
        
    @nextcord.slash_command(name="showoptions", description="Show current server options", guild_ids=[testServerId])
    async def showoptions(self, interaction: Interaction):
        result = self.zrcon.showoptions()
        emoji = "✅" if getattr(result, "success", True) else "❌"
        await interaction.response.send_message(f"{emoji} {result.response}")

    @nextcord.slash_command(name="startrain", description="Start rain on the server", guild_ids=[testServerId])
    async def startrain(self, interaction: Interaction):
        result = self.zrcon.startrain()
        emoji = "✅" if getattr(result, "success", True) else "❌"
        await interaction.response.send_message(f"{emoji} {result.response}")

    @nextcord.slash_command(name="stoprain", description="Stop rain on the server", guild_ids=[testServerId])
    async def stoprain(self, interaction: Interaction):
        result = self.zrcon.stoprain()
        emoji = "✅" if getattr(result, "success", True) else "❌"
        await interaction.response.send_message(f"{emoji} {result.response}")

    @nextcord.slash_command(name="teleport", description="Teleport one player to another", guild_ids=[testServerId])
    async def teleport(
        self,
        interaction: Interaction,
        user: str = SlashOption(description="Player to teleport"),
        touser: str = SlashOption(description="Destination player")
    ):
        result = self.zrcon.teleport(user,touser)
        emoji = "✅" if getattr(result, "success", True) else "❌"
        await interaction.response.send_message(f"{emoji} {result.response}")
    
    
    @nextcord.slash_command(name="addalltowhitelist", description="Add all connected users with password to whitelist", guild_ids=[testServerId])
    async def addalltowhitelist(self, interaction: Interaction):
        result = self.zrcon.addalltowhitelist()
        emoji = "✅" if getattr(result, "success", True) else "❌"
        await interaction.response.send_message(f"{emoji} {result.response}")

    @nextcord.slash_command(name="adduser", description="Add a new user to whitelist", guild_ids=[testServerId])
    async def adduser(
        self,
        interaction: Interaction,
        user: str = SlashOption(description="Username"),
        pwd: str = SlashOption(description="Password")
    ):
        result = self.zrcon.adduser(user, pwd)
        emoji = "✅" if getattr(result, "success", True) else "❌"
        await interaction.response.send_message(f"{emoji} {result.response}")

    @nextcord.slash_command(name="addusertowhitelist", description="Add a single user to whitelist", guild_ids=[testServerId])
    async def addusertowhitelist(
        self,
        interaction: Interaction,
        user: str = SlashOption(description="Username")
    ):
        result = self.zrcon.addusertowhitelist(user)
        emoji = "✅" if getattr(result, "success", True) else "❌"
        await interaction.response.send_message(f"{emoji} {result.response}")

    @nextcord.slash_command(name="removeuserfromwhitelist", description="Remove user from whitelist", guild_ids=[testServerId])
    async def removeuserfromwhitelist(
        self,
        interaction: Interaction,
        user: str = SlashOption(description="Username")
    ):
        result = self.zrcon.removeuserfromwhitelist(user)
        emoji = "✅" if getattr(result, "success", True) else "❌"
        await interaction.response.send_message(f"{emoji} {result.response}")

    @nextcord.slash_command(name="banid", description="Ban a Steam ID", guild_ids=[testServerId])
    async def banid(
        self,
        interaction: Interaction,
        steamid: str = SlashOption(description="Steam ID")
    ):
        result = self.zrcon.banid(steamid)
        emoji = "✅" if getattr(result, "success", True) else "❌"
        await interaction.response.send_message(f"{emoji} {result.response}")

    @nextcord.slash_command(name="unbanid", description="Unban a Steam ID", guild_ids=[testServerId])
    async def unbanid(
        self,
        interaction: Interaction,
        steamid: str = SlashOption(description="Steam ID")
    ):
        result = self.zrcon.unbanid(steamid)
        emoji = "✅" if getattr(result, "success", True) else "❌"
        await interaction.response.send_message(f"{emoji} {result.response}")

    @nextcord.slash_command(name="banuser", description="Ban a user", guild_ids=[testServerId])
    async def banuser(
        self,
        interaction: Interaction,
        user: str = SlashOption(description="Username")
    ):
        result = self.zrcon.banuser(user)
        emoji = "✅" if getattr(result, "success", True) else "❌"
        await interaction.response.send_message(f"{emoji} {result.response}")

    @nextcord.slash_command(name="unbanuser", description="Unban a user", guild_ids=[testServerId])
    async def unbanuser(
        self,
        interaction: Interaction,
        user: str = SlashOption(description="Username")
    ):
        result = self.zrcon.unbanuser(user)
        emoji = "✅" if getattr(result, "success", True) else "❌"
        await interaction.response.send_message(f"{emoji} {result.response}")

    @nextcord.slash_command(name="checkmodsneedupdate", description="Check if any mods need an update", guild_ids=[testServerId])
    async def checkmodsneedupdate(self, interaction: Interaction):
        result = self.zrcon.checkModsNeedUpdate()
        emoji = "✅" if getattr(result, "success", True) else "❌"
        await interaction.response.send_message(f"{emoji} {result.response}")

    @nextcord.slash_command(name="grantadmin", description="Grant admin to a user", guild_ids=[testServerId])
    async def grantadmin(
        self,
        interaction: Interaction,
        user: str = SlashOption(description="Username")
    ):
        result = self.zrcon.grantadmin(user)
        emoji = "✅" if getattr(result, "success", True) else "❌"
        await interaction.response.send_message(f"{emoji} {result.response}")

    @nextcord.slash_command(name="removeadmin", description="Remove admin from a user", guild_ids=[testServerId])
    async def removeadmin(
        self,
        interaction: Interaction,
        user: str = SlashOption(description="Username")
    ):
        result = self.zrcon.removeadmin(user)
        emoji = "✅" if getattr(result, "success", True) else "❌"
        await interaction.response.send_message(f"{emoji} {result.response}")

    @nextcord.slash_command(name="kickuser", description="Kick a user from the server", guild_ids=[testServerId])
    async def kickuser(
        self,
        interaction: Interaction,
        user: str = SlashOption(description="Username")
    ):
        result = self.zrcon.kickuser(user)
        emoji = "✅" if getattr(result, "success", True) else "❌"
        await interaction.response.send_message(f"{emoji} {result.response}")

    @nextcord.slash_command(name="players", description="List connected players", guild_ids=[testServerId])
    async def players(self, interaction: Interaction):
        result = self.zrcon.players().response
        await interaction.response.send_message(f"{emoji} {result.response}")

    @nextcord.slash_command(name="servermsg", description="Send a message to all players", guild_ids=[testServerId])
    async def servermsg(
        self,
        interaction: Interaction,
        message: str = SlashOption(description="Message to broadcast")
    ):
        result = self.zrcon.servermsg(message)
        emoji = "✅" if getattr(result, "success", True) else "❌"
        await interaction.response.send_message(f"{emoji} {result.response}")

    @nextcord.slash_command(name="setaccesslevel", description="Set access level of a player", guild_ids=[testServerId])
    async def setaccesslevel(
        self,
        interaction: Interaction,
        user: str = SlashOption(description="Username"),
        level: str = SlashOption(description="Access level (admin, moderator, overseer, gm, observer)")
    ):
        result = self.zrcon.setaccesslevel(user,level)
        emoji = "✅" if getattr(result, "success", True) else "❌"
        await interaction.response.send_message(f"{emoji} {result.response}")

    @nextcord.slash_command(name="voiceban", description="Toggle voice ban for user", guild_ids=[testServerId])
    async def voiceban(
        self,
        interaction: Interaction,
        user: str = SlashOption(description="Username"),
        toggle: str = SlashOption(description="-true to ban, -false to unban")
    ):
        result = self.zrcon.voiceban(user,toggle)
        emoji = "✅" if getattr(result, "success", True) else "❌"
        await interaction.response.send_message(f"{emoji} {result.response}")
        
def setup(bot):
    RCON_HOST = os.getenv("RCON_HOST")
    RCON_PORT = int(os.getenv("RCON_PORT"))
    RCON_PASSWORD = os.getenv("RCON_PASSWORD")
    zrcon = ZomboidRCON(RCON_HOST, RCON_PORT, RCON_PASSWORD)  # Replace with your actual credentials
    bot.add_cog(Rcon_commands(bot, zrcon))  # ✅ pass zrcon to the cog
