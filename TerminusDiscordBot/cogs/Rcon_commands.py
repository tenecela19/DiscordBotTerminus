import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
from zomboid_rcon import ZomboidRCON
from dotenv import load_dotenv
from utils.embed_factory import create_embed_response

import os

load_dotenv()

class Rcon_commands(commands.Cog):
    def __init__(self, bot, zrcon):
        self.bot = bot
        self.zrcon = zrcon
    
    testServerId = 1349396630880915570
   
    @nextcord.slash_command(name="additem", description="Give item to player", guild_ids=[testServerId],default_member_permissions=nextcord.Permissions(administrator=True))
    async def additem(
        self,
        interaction: Interaction,
        user: str = SlashOption(description="In-game username"),
        item: str = SlashOption(description="Item ID")
    ):
        await interaction.response.defer()
        result = self.zrcon.additem(user, item)
        interaction.followup.send(f"✅ {result.response}")

    @nextcord.slash_command(name="addvehicle", description="Spawn a vehicle for a player", guild_ids=[testServerId],default_member_permissions=nextcord.Permissions(administrator=True))
    async def addvehicle(
        self,
        interaction: Interaction,
        user: str = SlashOption(description="In-game username or x,y,z"),
        script: str = SlashOption(description="Script car name")
    ):
        await interaction.response.defer()
        result = self.zrcon.command("addvehicle", f'{script} "{user}"')
        await interaction.followup.send(f"✅ {result.response}")

    @nextcord.slash_command(name="addxp", description="Give XP to a player", guild_ids=[testServerId],default_member_permissions=nextcord.Permissions(administrator=True))
    async def addxp(
        self,
        interaction: Interaction,
        user: str = SlashOption(description="In-game username"),
        perk: str = SlashOption(description="Perk name"),
        xp: int = SlashOption(description="Amount of XP")
    ):
        await interaction.response.defer()
        result = self.zrcon.addxp(user, perk, xp)
        await interaction.followup.send(f"✅ {result.response}")
    
    @nextcord.slash_command(name="alarm", description="Sound a building alarm at your position", guild_ids=[testServerId],default_member_permissions=nextcord.Permissions(administrator=True))
    async def alarm(self, interaction: Interaction):
        await interaction.response.defer()
        result = self.zrcon.alarm()
        await interaction.followup.send(f"✅ {result.response}")

    @nextcord.slash_command(name="changeoption", description="Change a server option", guild_ids=[testServerId],default_member_permissions=nextcord.Permissions(administrator=True))
    async def changeoption(
        self,
        interaction: Interaction,
        option: str = SlashOption(description="Option name"),
        newoption: str = SlashOption(description="New value")
    ):
        await interaction.response.defer()
        result = self.zrcon.command("changeoption", f'{option} "{newoption}"')
        await interaction.followup.send(f"✅ {result.response}")

    @nextcord.slash_command(name="chopper", description="Trigger helicopter event on random player", guild_ids=[testServerId],default_member_permissions=nextcord.Permissions(administrator=True))
    async def chopper(self, interaction: Interaction):
        await interaction.response.defer()
        result = self.zrcon.chopper()
        await interaction.followup.send(f"✅ {result.response}")

    @nextcord.slash_command(name="changepwd", description="Change your admin password", guild_ids=[testServerId],default_member_permissions=nextcord.Permissions(administrator=True))
    async def changepwd(
        self,
        interaction: Interaction,
        pwd: str = SlashOption(description="Current password"),
        newpwd: str = SlashOption(description="New password")
    ):
        await interaction.response.defer()
        result = self.zrcon.changepwd(pwd,newpwd)
        await interaction.followup.send(f"✅ {result.response}")
    
    @nextcord.slash_command(name="createhorde", description="Spawn a horde near a player", guild_ids=[testServerId],default_member_permissions=nextcord.Permissions(administrator=True))
    async def createhorde(
        self,
        interaction: Interaction,
        user: str = SlashOption(description="player name"),
        number: int = SlashOption(description="Number of zombies")
    ):
        await interaction.response.defer()
        result = self.zrcon.createhorde(number)
        self.zrcon.command("createhorde", f'{number} "{user}"')
        await interaction.followup.send(f"✅ {result.response}")
 
    @nextcord.slash_command(name="godmode", description="Toggle godmode for a player", guild_ids=[testServerId],default_member_permissions=nextcord.Permissions(administrator=True))
    async def godmode(
        self,
        interaction: Interaction,
        user: str = SlashOption(description="In-game username")
    ):
        await interaction.response.defer()
        result = self.zrcon.godmode(user)
        await interaction.followup.send(f"✅ {result.response}")

    @nextcord.slash_command(name="gunshot", description="Make a gunshot sound near the player", guild_ids=[testServerId],default_member_permissions=nextcord.Permissions(administrator=True))
    async def gunshot(self, interaction: Interaction):
        await interaction.response.defer()
        result= self.zrcon.gunshot()
        await interaction.followup.send(f"✅ {result.response}")

    @nextcord.slash_command(name="help", description="Display native RCON help menu", guild_ids=[testServerId],default_member_permissions=nextcord.Permissions(administrator=True))
    async def command_help(self, interaction: Interaction):
        await interaction.response.defer()
        result = self.zrcon.help().response
        chunks = [result[i:i+1900] for i in range(0, len(result), 1900)]

        for i, chunk in enumerate(chunks):
            try:
                await interaction.followup.send(f"```ini\n{chunk}\n```")
            except nextcord.HTTPException as e:
                await interaction.followup.send(f"❌ Failed to send part {i+1}: {str(e)}")
                break
    @nextcord.slash_command(name="invisible", description="Make a player invisible to zombies", guild_ids=[testServerId],default_member_permissions=nextcord.Permissions(administrator=True))
    async def invisible(
        self,
        interaction: Interaction,
        user: str = SlashOption(description="In-game username"),
        toggle: str = SlashOption(description="SET '-' -true or -false ")
    ):
        await interaction.response.defer()
        result = self.zrcon.invisible(user)
        await interaction.followup.send(f"✅ {result.response}")

    @nextcord.slash_command(name="noclip", description="Allow player to walk through objects", guild_ids=[testServerId],default_member_permissions=nextcord.Permissions(administrator=True))
    async def noclip(
        self,
        interaction: Interaction,
        user: str = SlashOption(description="In-game username")
    ):
        await interaction.response.defer()
        result = self.zrcon.noclip(user)
        await interaction.followup.send(f"✅ {result.response}")
    @nextcord.slash_command(name="quit", description="Save the world", guild_ids=[testServerId],default_member_permissions=nextcord.Permissions(administrator=True))
    async def quit_command(self, interaction: Interaction):
        await interaction.response.defer()
        result = self.zrcon.quit()
        await interaction.followup.send(f"✅ stop server")
    @nextcord.slash_command(name="reloadoptions", description="Reload server options", guild_ids=[testServerId],default_member_permissions=nextcord.Permissions(administrator=True))
    async def reloadoptions(self, interaction: Interaction):
        await interaction.response.defer()
        result = self.zrcon.reloadoptions()
        await interaction.followup.send(f"✅ {result.response}")
    @nextcord.slash_command(name="save", description="Save the world", guild_ids=[testServerId],default_member_permissions=nextcord.Permissions(administrator=True))
    async def save(self, interaction: Interaction):
        await interaction.response.defer()
        result = self.zrcon.save()
        await interaction.followup.send(f"✅ world saved")
        
    @nextcord.slash_command(name="showoptions", description="Show current server options", guild_ids=[testServerId],default_member_permissions=nextcord.Permissions(administrator=True))
    async def showoptions(self, interaction: Interaction):
        await interaction.response.defer()
        result = self.zrcon.showoptions().response
        chunks = [result[i:i+1900] for i in range(0, len(result), 1900)]

        for i, chunk in enumerate(chunks):
            try:
                await interaction.followup.send(f"```ini\n{chunk}\n```")
            except nextcord.HTTPException as e:
                await interaction.followup.send(f"❌ Failed to send part {i+1}: {str(e)}")
                break

    @nextcord.slash_command(name="startrain", description="Start rain on the server", guild_ids=[testServerId],default_member_permissions=nextcord.Permissions(administrator=True))
    async def startrain(self, interaction: Interaction):
        await interaction.response.defer()
        result = self.zrcon.startrain()
        await interaction.followup.send(f"✅ {result.response}")

    @nextcord.slash_command(name="stoprain", description="Stop rain on the server", guild_ids=[testServerId],default_member_permissions=nextcord.Permissions(administrator=True))
    async def stoprain(self, interaction: Interaction):
        await interaction.response.defer()
        result = self.zrcon.stoprain()
        await interaction.followup.send(f"✅ {result.response}")

    @nextcord.slash_command(name="teleport", description="Teleport one player to another", guild_ids=[testServerId],default_member_permissions=nextcord.Permissions(administrator=True))
    async def teleport(
        self,
        interaction: Interaction,
        user: str = SlashOption(description="Player to teleport"),
        touser: str = SlashOption(description="Destination player")
    ):
        await interaction.response.defer()
        result = self.zrcon.teleport(user,touser)
        await interaction.followup.send(f"✅ {result.response}")
    
    
    @nextcord.slash_command(name="addalltowhitelist", description="Add all connected users with password to whitelist", guild_ids=[testServerId],default_member_permissions=nextcord.Permissions(administrator=True))
    async def addalltowhitelist(self, interaction: Interaction):
        await interaction.response.defer()
        result = self.zrcon.addalltowhitelist()
        await interaction.followup.send(f"✅ {result.response}")

    @nextcord.slash_command(name="adduser", description="Add a new user to whitelist", guild_ids=[testServerId],default_member_permissions=nextcord.Permissions(administrator=True))
    async def adduser(
        self,
        interaction: Interaction,
        user: str = SlashOption(description="Username"),
        pwd: str = SlashOption(description="Password")
    ):
        await interaction.response.defer()
        result = self.zrcon.adduser(user, pwd)
        await interaction.followup.send(f"✅ {result.response}")

    @nextcord.slash_command(name="addusertowhitelist", description="Add a single user to whitelist", guild_ids=[testServerId],default_member_permissions=nextcord.Permissions(administrator=True))
    async def addusertowhitelist(
        self,
        interaction: Interaction,
        user: str = SlashOption(description="Username")
    ):
        await interaction.response.defer()
        result = self.zrcon.addusertowhitelist(user)
        await interaction.followup.send(f"✅ {result.response}")

    @nextcord.slash_command(name="removeuserfromwhitelist", description="Remove user from whitelist", guild_ids=[testServerId],default_member_permissions=nextcord.Permissions(administrator=True))
    async def removeuserfromwhitelist(
        self,
        interaction: Interaction,
        user: str = SlashOption(description="Username")
    ):
        await interaction.response.defer()
        result = self.zrcon.removeuserfromwhitelist(user)
        await interaction.followup.send(f"✅ {result.response}")

    @nextcord.slash_command(name="banid", description="Ban a Steam ID", guild_ids=[testServerId],default_member_permissions=nextcord.Permissions(administrator=True))
    async def banid(
        self,
        interaction: Interaction,
        steamid: str = SlashOption(description="Steam ID")
    ):
        await interaction.response.defer()
        result = self.zrcon.banid(steamid)
        await interaction.followup.send(f"✅ {result.response}")

    @nextcord.slash_command(name="unbanid", description="Unban a Steam ID", guild_ids=[testServerId],default_member_permissions=nextcord.Permissions(administrator=True))
    async def unbanid(
        self,
        interaction: Interaction,
        steamid: str = SlashOption(description="Steam ID")
    ):
        await interaction.response.defer()
        result = self.zrcon.unbanid(steamid)
        await interaction.followup.send(f"✅ {result.response}")

    @nextcord.slash_command(name="banuser", description="Ban a user", guild_ids=[testServerId],default_member_permissions=nextcord.Permissions(administrator=True))
    async def banuser(
        self,
        interaction: Interaction,
        user: str = SlashOption(description="Username")
    ):
        await interaction.response.defer()
        result = self.zrcon.banuser(user)
        await interaction.followup.send(f"✅ {result.response}")

    @nextcord.slash_command(name="unbanuser", description="Unban a user", guild_ids=[testServerId],default_member_permissions=nextcord.Permissions(administrator=True))
    async def unbanuser(
        self,
        interaction: Interaction,
        user: str = SlashOption(description="Username")
    ):
        await interaction.response.defer()
        result = self.zrcon.unbanuser(user)
        await interaction.followup.send(f"✅ {result.response}")

    @nextcord.slash_command(name="checkmodsneedupdate", description="Check if any mods need an update", guild_ids=[testServerId],default_member_permissions=nextcord.Permissions(administrator=True))
    async def checkmodsneedupdate(self, interaction: Interaction):
        result = self.zrcon.checkModsNeedUpdate()
        await interaction.followup.send(f"✅ {result.response}")

    @nextcord.slash_command(name="grantadmin", description="Grant admin to a user", guild_ids=[testServerId],default_member_permissions=nextcord.Permissions(administrator=True))
    async def grantadmin(
        self,
        interaction: Interaction,
        user: str = SlashOption(description="Username")
    ):
        await interaction.response.defer()
        result = self.zrcon.grantadmin(user)
        await interaction.followup.send(f"✅ {result.response}")

    @nextcord.slash_command(name="removeadmin", description="Remove admin from a user", guild_ids=[testServerId],default_member_permissions=nextcord.Permissions(administrator=True))
    async def removeadmin(
        self,
        interaction: Interaction,
        user: str = SlashOption(description="Username")
    ):
        await interaction.response.defer()
        result = self.zrcon.removeadmin(user)
        await interaction.followup.send(f"✅ {result.response}")

    @nextcord.slash_command(name="kickuser", description="Kick a user from the server", guild_ids=[testServerId],default_member_permissions=nextcord.Permissions(administrator=True))
    async def kickuser(
        self,
        interaction: Interaction,
        user: str = SlashOption(description="Username")
    ):
        await interaction.response.defer()
        result = self.zrcon.kickuser(user)
        await interaction.followup.send(f"✅ {result.response}")

    @nextcord.slash_command(name="players", description="List connected players", guild_ids=[testServerId],default_member_permissions=nextcord.Permissions(administrator=True))
    async def players(self, interaction: Interaction):
        await interaction.response.defer()
        result = self.zrcon.players()
        await interaction.followup.send(result.response)

    @nextcord.slash_command(name="servermsg", description="Send a message to all players", guild_ids=[testServerId],default_member_permissions=nextcord.Permissions(administrator=True))
    async def servermsg(
        self,
        interaction: Interaction,
        message: str = SlashOption(description="Message to broadcast")
    ):
        await interaction.response.defer()
        result = self.zrcon.command("servermsg",message)
        await interaction.followup.send(f"✅ {result.response}")

    @nextcord.slash_command(name="setaccesslevel", description="Set access level of a player", guild_ids=[testServerId],default_member_permissions=nextcord.Permissions(administrator=True))
    async def setaccesslevel(
        self,
        interaction: Interaction,
        user: str = SlashOption(description="Username"),
        level: str = SlashOption(description="Access level (admin, moderator, overseer, gm, observer)")
    ):
        await interaction.response.defer()
        result = self.zrcon.setaccesslevel(user,level)
        await interaction.followup.send(f"✅ {result.response}")

    @nextcord.slash_command(name="voiceban", description="Toggle voice ban for user", guild_ids=[testServerId],default_member_permissions=nextcord.Permissions(administrator=True))
    async def voiceban(
        self,
        interaction: Interaction,
        user: str = SlashOption(description="Username"),
        toggle: str = SlashOption(description="-true to ban, -false to unban")
    ):
        await interaction.response.defer()
        result = self.zrcon.voiceban(user,toggle)
        await interaction.followup.send(f"✅ {result.response}")
        
def setup(bot):
    RCON_HOST = os.getenv("RCON_HOST")
    RCON_PORT = int(os.getenv("RCON_PORT"))
    RCON_PASSWORD = os.getenv("RCON_PASSWORD")
    zrcon = ZomboidRCON(RCON_HOST, RCON_PORT, RCON_PASSWORD)  # Replace with your actual credentials
    bot.add_cog(Rcon_commands(bot, zrcon))  # ✅ pass zrcon to the cog

