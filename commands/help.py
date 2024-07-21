import discord
from discord.ext import commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help", help="Shows this help message.")
    async def help(self, ctx):
        """Displays a list of available commands and their descriptions."""
        embed = discord.Embed(title="MelodyBot Help", color=discord.Color.blue())

        # Music Commands
        music_commands = [
            "play",
            "pause",
            "resume",
            "skip",
            "stop",
            "queue",
            "clear",
            "shuffle",
            "volume",
        ]
        music_help_text = "\n".join(
            f"`{cmd}`: {self.bot.get_command(cmd).help}" for cmd in music_commands
        )
        embed.add_field(
            name="Music Commands", value=music_help_text, inline=False
        )

        # Admin Commands
        admin_commands = ["join", "leave", "setprefix", "ban", "kick"]
        admin_help_text = "\n".join(
            f"`{cmd}`: {self.bot.get_command(cmd).help}" for cmd in admin_commands
        )
        embed.add_field(
            name="Admin Commands", value=admin_help_text, inline=False
        )

        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))