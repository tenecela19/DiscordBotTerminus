from discord.ext import commands

class AdminCommands(commands.Cog):
    def __init__(self, bot, admin_manager):
        self.bot = bot
        self.admin_manager = admin_manager

    @commands.command(name="addadmin")
    @commands.has_permissions(administrator=True)
    async def add_admin(self, ctx, name: str):
        name = name.strip()
        if not self.admin_manager.is_bypassed(name):
            self.admin_manager.add(name)
            await ctx.send(f"✅ Added `{name}` to admin bypass list.")
        else:
            await ctx.send(f"⚠️ `{name}` is already in the admin list.")

    @commands.command(name="removeadmin")
    @commands.has_permissions(administrator=True)
    async def remove_admin(self, ctx, name: str):
        if self.admin_manager.is_bypassed(name):
            self.admin_manager.remove(name)
            await ctx.send(f"✅ Removed `{name}` from admin bypass list.")
        else:
            await ctx.send(f"❌ `{name}` is not in the admin list.")

    @commands.command(name="listadmins")
    @commands.has_permissions(administrator=True)
    async def list_admins(self, ctx):
        admins = self.admin_manager.list()
        if admins:
            admin_list = ', '.join(f"`{name}`" for name in sorted(admins))
            await ctx.send(f"👑 Admin Bypass List:\n{admins}")
        else:
            await ctx.send("🕳️ No admins in bypass list.")

def setup_admin_commands(bot, admin_manager):
    return AdminCommands(bot, admin_manager)
