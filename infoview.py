import discord
import datetime


class InfoView(discord.ui.View):
    def __init__(self, player_name, s1_round, s1_rating, s1_acs, s1_kd, s1_kast, s1_adr, s1_kpr, s1_apr, s1_fkpr, s1_fdpr, s1_hs, s1_kmax, s1_kills, s1_deaths, s1_assists, s1_fk, s1_fd, s2_round, s2_rating, s2_acs, s2_kd, s2_kast, s2_adr, s2_kpr, s2_apr, s2_fkpr, s2_fdpr, s2_hs, s2_kmax, s2_kills, s2_deaths, s2_assists, s2_fk, s2_fd, requester, avatar_url):
        super().__init__(timeout=60)
        self.player_name = player_name
        self.s1_round = s1_round
        self.s1_rating = s1_rating
        self.s1_acs = s1_acs
        self.s1_kd = s1_kd
        self.s1_kast = s1_kast
        self.s1_adr = s1_adr
        self.s1_kpr = s1_kpr
        self.s1_apr = s1_apr
        self.s1_fkpr = s1_fkpr
        self.s1_fdpr = s1_fdpr
        self.s1_hs = s1_hs
        self.s1_kmax = s1_kmax
        self.s1_kills = s1_kills
        self.s1_deaths = s1_deaths
        self.s1_assists = s1_assists
        self.s1_fk = s1_fk
        self.s1_fd = s1_fd

        self.s2_round = s2_round
        self.s2_rating = s2_rating
        self.s2_acs = s2_acs
        self.s2_kd = s2_kd
        self.s2_kast = s2_kast
        self.s2_adr = s2_adr
        self.s2_kpr = s2_kpr
        self.s2_apr = s2_apr
        self.s2_fkpr = s2_fkpr
        self.s2_fdpr = s2_fdpr
        self.s2_hs = s2_hs
        self.s2_kmax = s2_kmax
        self.s2_kills = s2_kills
        self.s2_deaths = s2_deaths
        self.s2_assists = s2_assists
        self.s2_fk = s2_fk
        self.s2_fd = s2_fd

        self.requester = requester
        self.avatar_url = avatar_url
        self.current_season = 2

        self.season2_button = discord.ui.Button(
            label="Season 2", style=discord.ButtonStyle.primary, disabled=True)
        self.season1_button = discord.ui.Button(
            label="Season 1", style=discord.ButtonStyle.primary)

        self.season2_button.callback = self.season2
        self.season1_button.callback = self.season1

        self.add_item(self.season1_button)
        self.add_item(self.season2_button)

    async def season2(self, interaction: discord.Interaction):
        if interaction.user != self.requester:
            await interaction.response.send_message("You can't interact with this button.", ephemeral=True)
            return

        self.current_season = 2
        self.season2_button.disabled = True
        self.season1_button.disabled = False

        embed = discord.Embed(
            title=f"{self.player_name}'s Season 2 Stats",
            description=f"# Rating - {self.s2_rating}",
            color=int("FDB927", 16)
        )
        embed.set_thumbnail(url=self.avatar_url)
        embed.timestamp = datetime.datetime.now()
        # embed.add_field(name="Rating", value=self.s2_rating, inline=True)
        embed.add_field(name="Rounds Played", value=self.s2_round, inline=False)
        embed.add_field(name="ACS", value=self.s2_acs, inline=True)
        embed.add_field(name="K/D", value=self.s2_kd, inline=True)
        embed.add_field(name="KAST", value=self.s2_kast, inline=True)
        embed.add_field(name="ADR", value=self.s2_adr, inline=True)
        embed.add_field(name="KPR", value=self.s2_kpr, inline=True)
        embed.add_field(name="APR", value=self.s2_apr, inline=True)
        embed.add_field(name="FKPR", value=self.s2_fkpr, inline=True)
        embed.add_field(name="FDPR", value=self.s2_fdpr, inline=True)
        embed.add_field(name="HS%", value=self.s2_hs, inline=True)
        embed.add_field(name="KMAX", value=self.s2_kmax, inline=True)
        embed.add_field(name="Kills", value=self.s2_kills, inline=True)
        embed.add_field(name="Deaths", value=self.s2_deaths, inline=True)
        embed.add_field(name="Assists", value=self.s2_assists, inline=True)
        embed.add_field(name="FK", value=self.s2_fk, inline=True)
        embed.add_field(name="FD", value=self.s2_fd, inline=True)

        await interaction.response.edit_message(embed=embed, view=self)

    async def season1(self, interaction: discord.Interaction):
        if interaction.user != self.requester:
            await interaction.response.send_message("You can't interact with this button.", ephemeral=True)
            return

        self.current_season = 1
        self.season1_button.disabled = True
        self.season2_button.disabled = False

        embed = discord.Embed(
            title=f"{self.player_name}'s Season 1 Stats",
            description=f"# Rating - {self.s1_rating}",
            color=int("FDB927", 16)
        )
        embed.set_thumbnail(url=self.avatar_url)
        embed.timestamp = datetime.datetime.now()
        # embed.add_field(name="Rating", value=self.s1_rating, inline=True)
        embed.add_field(name="Rounds Played", value=self.s1_round, inline=False)
        embed.add_field(name="ACS", value=self.s1_acs, inline=True)
        embed.add_field(name="K/D", value=self.s1_kd, inline=True)
        embed.add_field(name="KAST", value=self.s1_kast, inline=True)
        embed.add_field(name="ADR", value=self.s1_adr, inline=True)
        embed.add_field(name="KPR", value=self.s1_kpr, inline=True)
        embed.add_field(name="APR", value=self.s1_apr, inline=True)
        embed.add_field(name="FKPR", value=self.s1_fkpr, inline=True)
        embed.add_field(name="FDPR", value=self.s1_fdpr, inline=True)
        embed.add_field(name="HS%", value=self.s1_hs, inline=True)
        embed.add_field(name="KMAX", value=self.s1_kmax, inline=True)
        embed.add_field(name="Kills", value=self.s1_kills, inline=True)
        embed.add_field(name="Deaths", value=self.s1_deaths, inline=True)
        embed.add_field(name="Assists", value=self.s1_assists, inline=True)
        embed.add_field(name="FK", value=self.s1_fk, inline=True)
        embed.add_field(name="FD", value=self.s1_fd, inline=True)

        await interaction.response.edit_message(embed=embed, view=self)

    def build_default_embed(self):
        embed = discord.Embed(
            title=f"{self.player_name}'s Season 2 Stats",
            description=f"# Rating - {self.s2_rating}",
            color=int("FDB927", 16)
        )
        embed.set_thumbnail(url=self.avatar_url)
        embed.timestamp = datetime.datetime.now()
        # embed.add_field(name="Rating", value=self.s2_rating, inline=True)
        embed.add_field(name="Rounds Played", value=self.s2_round, inline=False)
        embed.add_field(name="ACS", value=self.s2_acs, inline=True)
        embed.add_field(name="K/D", value=self.s2_kd, inline=True)
        embed.add_field(name="KAST", value=self.s2_kast, inline=True)
        embed.add_field(name="ADR", value=self.s2_adr, inline=True)
        embed.add_field(name="KPR", value=self.s2_kpr, inline=True)
        embed.add_field(name="APR", value=self.s2_apr, inline=True)
        embed.add_field(name="FKPR", value=self.s2_fkpr, inline=True)
        embed.add_field(name="FDPR", value=self.s2_fdpr, inline=True)
        embed.add_field(name="HS%", value=self.s2_hs, inline=True)
        embed.add_field(name="KMAX", value=self.s2_kmax, inline=True)
        embed.add_field(name="Kills", value=self.s2_kills, inline=True)
        embed.add_field(name="Deaths", value=self.s2_deaths, inline=True)
        embed.add_field(name="Assists", value=self.s2_assists, inline=True)
        embed.add_field(name="FK", value=self.s2_fk, inline=True)
        embed.add_field(name="FD", value=self.s2_fd, inline=True)
        return embed
