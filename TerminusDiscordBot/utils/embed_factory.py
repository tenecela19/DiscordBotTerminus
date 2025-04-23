# utils/embed_factory.py

import discord

def create_embed_response(title: str, message: str, color=discord.Color.blurple()) -> discord.Embed:
    embed = discord.Embed(
        title=title,
        description=f"```{message.strip()}```",
        color=color
    )
    embed.set_footer(text="TerminusBot • Project Zomboid")
    return embed
