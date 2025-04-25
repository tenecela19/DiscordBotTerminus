# utils/embed_factory.py

import nextcord

def create_embed_response(
    title: str,
    message: str,
    color=nextcord.Color.blurple(),
    code_block: bool = True
) -> nextcord.Embed:
    description = f"```{message.strip()}```" if code_block else message.strip()
    embed = nextcord.Embed(title=title, description=description, color=color)
    embed.set_footer(text="TerminusBot • Project Zomboid")
    return embed

