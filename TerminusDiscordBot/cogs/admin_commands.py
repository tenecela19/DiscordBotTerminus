import nextcord
from nextcord.ext import commands
from nextcord import Interaction, SlashOption
from utils.admin_bypass import AdminBypassManager
import os

class BypassAdminLogs(commands.Cog):
    def __init__(self, bot, admin_manager):
        self.bot = bot
        self.admin_manager = admin_manager
    testServerId = 1349396630880915570

    @nextcord.slash_command(name="addbypassadmin", description="Add user to bypass admin list", guild_ids=[testServerId])
    async def add_admin(
        self,
        interaction: Interaction,
        name: str = SlashOption(description="Username to add")
    ):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)
            return

        name = name.strip()
        if not self.admin_manager.is_bypassed(name):
            self.admin_manager.add(name)
            await interaction.response.send_message(f"✅ Added `{name}` to admin bypass list.")
        else:
            await interaction.response.send_message(f"⚠️ `{name}` is already in the admin list.")

    @nextcord.slash_command(name="removebypassadmin", description="Remove user from bypass admin list", guild_ids=[testServerId])
    async def remove_admin(
        self,
        interaction: Interaction,
        name: str = SlashOption(description="Username to remove")
    ):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)
            return

        if self.admin_manager.is_bypassed(name):
            self.admin_manager.remove(name)
            await interaction.response.send_message(f"✅ Removed `{name}` from admin bypass list.")
        else:
            await interaction.response.send_message(f"❌ `{name}` is not in the admin list.")

    @nextcord.slash_command(name="listbypassadmins", description="List all bypassed admin users", guild_ids=[testServerId])
    async def list_admins(self, interaction: Interaction):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ You don't have permission to use this command.", ephemeral=True)
            return

        admins = self.admin_manager.list()
        if admins:
            admin_list = ', '.join(f"`{name}`" for name in sorted(admins))
            await interaction.response.send_message(f"👑 Admin Bypass List:\n{admin_list}")
        else:
            await interaction.response.send_message("🕳️ No admins in bypass list.")

def setup(bot):
    admin_manager = AdminBypassManager()
    bot.add_cog(BypassAdminLogs(bot, admin_manager))
