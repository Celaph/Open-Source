import os
import discord
from discord.commands import slash_command
from discord.ext import commands


class Dropdown(discord.ui.Select):
    def __init__(self, bot):
        self.bot = bot
        options = []

        for files in os.listdir("./commands"):
            if files.endswith(".py"):
                if files.startswith("_"):
                    options.append(discord.SelectOption(label=f"{files[:-3]}", description="Private Addon.."))
                elif files.startswith(""):
                    options.append(discord.SelectOption(label=f"{files[:-3]}", description="Public Addon.."))

        super().__init__(
            placeholder="Choose the addon to reload...",
            max_values=len(options),
            options=options)

    async def callback(self, interaction: discord.Interaction):
        try:
            for e in self.values:
                self.bot.reload_extension(f"commands.{e}")
            await interaction.response.send_message(f"Reloaded {', '.join([f'`{v}`' for v in self.values])}",
                                                    ephemeral=True)
        except discord.errors.ExtensionNotLoaded:
            for e in self.values:
                self.bot.load_extension(f"commands.{e}")
            await interaction.response.send_message(f"Reloaded {', '.join([f'`{v}`' for v in self.values])}",
                                                    ephemeral=True)


class DropdownView(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()
        self.add_item(Dropdown(self.bot))


class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="reload", guild_ids=[995015765382139954])
    @commands.is_owner()
    async def _reload(self, i: discord.Interaction):
        view = DropdownView(self.bot)
        await i.response.send_message(view=view)


def setup(bot):
    bot.add_cog(Settings(bot))
