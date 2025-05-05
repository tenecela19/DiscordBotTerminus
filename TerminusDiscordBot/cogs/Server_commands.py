import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
from pydactyl import PterodactylClient

# Replace with your actual values
PANEL_URL = 'http://89.28.237.60/'
API_KEY = 'ptlc_6v3vqpnKrzfX03aUuH6Srnr3ieiLzEsQA0pbI63XshZ'
SERVER_ID = '22aae990-e69e-4482-afcc-12a860687710'
testServerId = 1349396630880915570  # Replace with your test server's ID

client = PterodactylClient(PANEL_URL, API_KEY)
my_servers = client.client.servers.list_servers()
# Get the unique identifier for the first server.
srv_id = my_servers[0]['attributes']['identifier']

class Server_commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @nextcord.slash_command(
        name="server_control",
        description="Start, stop, restart, or kill the Project Zomboid server",
        guild_ids=[testServerId],
        default_member_permissions=nextcord.Permissions(administrator=True)
    )
    async def server_control(
        self,
        interaction: Interaction,
        action: str = SlashOption(
            name="action",
            description="Power action to perform on the server",
            choices=["start", "stop", "restart", "kill"]
        )
    ):
        await interaction.response.defer()
        try:
            client.client.servers.send_power_action(srv_id, action)
            await interaction.followup.send(f"✅ Server `{action}` command sent.")
        except Exception as e:
            await interaction.followup.send(f"❌ Failed to send `{action}` command:\n```{e}```")


def setup(bot):
    bot.add_cog(Server_commands(bot))