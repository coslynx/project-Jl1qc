import discord
from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="join", help="Makes the bot join a specified voice channel.")
    @commands.has_permissions(manage_channels=True) # Ensure only users with manage_channels permission can use this command
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Makes the bot join a specified voice channel.

        Parameters
        ----------
        ctx : commands.Context
            The context of the command.
        channel : discord.VoiceChannel
            The voice channel to join.
        """
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()
        await channel.connect()
        await ctx.send(f"Joined {channel.name}")

    @commands.command(name="leave", help="Makes the bot leave the current voice channel.")
    @commands.has_permissions(manage_channels=True) # Ensure only users with manage_channels permission can use this command
    async def leave(self, ctx):
        """Makes the bot leave the current voice channel.

        Parameters
        ----------
        ctx : commands.Context
            The context of the command.
        """
        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()
            await ctx.send("Left the voice channel.")
        else:
            await ctx.send("I am not in a voice channel.")

    @commands.command(name="setprefix", help="Sets the bot's command prefix.")
    @commands.has_permissions(administrator=True) # Ensure only administrators can change the prefix
    async def setprefix(self, ctx, prefix):
        """Sets the bot's command prefix.

        Parameters
        ----------
        ctx : commands.Context
            The context of the command.
        prefix : str
            The new command prefix.
        """
        self.bot.command_prefix = prefix
        await ctx.send(f"Command prefix set to {prefix}")

    @commands.command(name="ban", help="Bans a user from the server.")
    @commands.has_permissions(ban_members=True) # Ensure only users with ban_members permission can use this command
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Bans a user from the server.

        Parameters
        ----------
        ctx : commands.Context
            The context of the command.
        member : discord.Member
            The member to ban.
        reason : str, optional
            The reason for the ban, by default None
        """
        try:
            await member.ban(reason=reason)
            await ctx.send(f"{member.name} was banned.")
        except discord.Forbidden:
            await ctx.send("I don't have permission to ban this user.")

    @commands.command(name="kick", help="Kicks a user from the server.")
    @commands.has_permissions(kick_members=True) # Ensure only users with kick_members permission can use this command
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Kicks a user from the server.

        Parameters
        ----------
        ctx : commands.Context
            The context of the command.
        member : discord.Member
            The member to kick.
        reason : str, optional
            The reason for the kick, by default None
        """
        try:
            await member.kick(reason=reason)
            await ctx.send(f"{member.name} was kicked.")
        except discord.Forbidden:
            await ctx.send("I don't have permission to kick this user.")


def setup(bot):
    bot.add_cog(Admin(bot))