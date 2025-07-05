import discord
from discord import app_commands
from discord.ext import commands
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import os
from infoview import InfoView
from ids import discord_ids, GUILD_ID

scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_key(
    '1uq4M3zQJy6eozPHs2Zu2gPFtIPIF86Zz31QDpsZmf1c').get_worksheet(1)
s1sheet = client.open_by_key(
    '1kzEP6ouQulRBcEqWbEpFOQ9uwhIYDWPtGFe8IcNzJ6M').get_worksheet(1)

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

MY_GUILD = discord.Object(id=GUILD_ID)

season1stats = {}
season2stats = {}

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await tree.sync(guild=MY_GUILD)
        print(f"Synced {len(synced)} commands to guild {MY_GUILD.id}")
    except Exception as e:
        print(f"Error syncing commands: {e}")


@bot.tree.command(name="updatestats", description="update stats whenever needed", guild=MY_GUILD)
@app_commands.checks.has_permissions(administrator=True)
async def startup(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)

    # Season 1 Stats Setup
    s1_data = s1sheet.get_all_values()
    s1_rows = s1_data[1:]

    for row in s1_rows:
        season1stats[row[0].strip()] = row[1:]

    s2_data = sheet.get_all_values()
    s2_rows = s2_data[1:]

    for row in s2_rows:
        season2stats[row[0].strip()] = row[1:]

    await interaction.followup.send(f"Updated stats", ephemeral=True)


@startup.error
async def startup_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("you dont got perms cuh", ephemeral=True)
    else:
        await interaction.response.send_message(f"an error has occurred: {error}", ephemeral=True)


@bot.tree.command(name="update", description="update rating in nickname based on stats", guild=MY_GUILD)
@app_commands.checks.has_permissions(administrator=True)
async def update_nicknames(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)

    guild = interaction.guild
    all_data = sheet.get_all_values()
    rows = all_data[1:]

    filtered_data = [
        [row[0], row[4], row[5]]
        for row in rows
    ]

    id_rating = {}
    for row in filtered_data:
        if int(row[1]) > 100:
            id_rating[int(discord_ids[row[0].strip()])] = [
                row[0].strip(), row[2].strip()]

    updated = 0

    for member in guild.members:
        if member.bot:
            continue

        player_name = id_rating.get(member.id)[0]
        if not player_name:
            player_name = member.display_name
        rating = id_rating.get(member.id)[1]

        try:
            if rating:
                new_nick = f'{player_name} | {rating}'
            else:
                new_nick = f'{player_name} | NR'
            try:
                await member.edit(nick=new_nick)
                updated += 1
            except discord.Forbidden:
                continue
        except (ValueError, KeyError):
            continue
        except discord.HTTPException:
            continue

    await interaction.followup.send(f"Updated nicknames for {updated} member(s).", ephemeral=True)


@update_nicknames.error
async def update_nicknames_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("you dont got perms cuh", ephemeral=True)
    else:
        await interaction.response.send_message(f"an error has occurred: {error}", ephemeral=True)


@bot.tree.command(name="info", description="look at your or someone else's stats", guild=MY_GUILD)
@app_commands.describe(player="the player you are trying to look up (optional)")
async def info(interaction: discord.Interaction, player: discord.Member = None):
    await interaction.response.defer(thinking=True)
    target = player or interaction.user
    avatar_url = target.display_avatar.url
    key = next((k for k, v in discord_ids.items() if v == target.id), None)

    if not key:
        await interaction.followup.send("You don't have any stats! Play at least 1 game to record stats")
        return

    if season1stats.get(key) is not None:
        s1ps = season1stats[key]
    else:
        s1ps = ["N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A",
                "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"]

    if season2stats.get(key) is not None:
        s2ps = season2stats[key]
    else:
        s2ps = ["N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A",
                "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"]

    view = InfoView(key, s1ps[3], s1ps[4], s1ps[5], s1ps[6], s1ps[7], s1ps[8], s1ps[9], s1ps[10],
                    s1ps[11], s1ps[12], s1ps[13], s1ps[14], s1ps[15], s1ps[16], s1ps[17], s1ps[18], s1ps[
                        19], s2ps[3], s2ps[4], s2ps[5], s2ps[6], s2ps[7], s2ps[8], s2ps[9], s2ps[10],
                    s2ps[11], s2ps[12], s2ps[13], s2ps[14], s2ps[15], s2ps[16], s2ps[17], s2ps[18], s2ps[
                        19], interaction.user, avatar_url)

    embed = view.build_default_embed()

    await interaction.followup.send(embed=embed, ephemeral=True, view=view)


@bot.tree.command(name="muteall", description="mute everyone in the vc", guild=MY_GUILD)
@app_commands.describe(exempt_member1="optional", exempt_member2="optional")
@app_commands.checks.has_permissions(administrator=True)
async def mute_all(interaction: discord.Interaction, exempt_member1: discord.Member = None, exempt_member2: discord.Member = None):
    await interaction.response.defer(thinking=True)

    member = interaction.user
    voice = member.voice

    if not voice or not voice.channel:
        await interaction.response.send_message("join a vc cuhzo")
        return

    channel = voice.channel
    muted = 0

    exempt_ids = set()
    if exempt_member1:
        exempt_ids.add(exempt_member1.id)
    if exempt_member2:
        exempt_ids.add(exempt_member2.id)

    for m in channel.members:
        if m.id in exempt_ids:
            continue
        try:
            await m.edit(mute=True)
            muted += 1
        except discord.Forbidden:
            continue

    exempt_names = ", ".join(
        m.display_name for m in channel.members if m.id in exempt_ids)
    exempt_text = f", except {exempt_names}" if exempt_names else ""
    await interaction.followup.send(f"Muted {muted} people in {channel.name}{exempt_text}", ephemeral=True)


@mute_all.error
async def mute_all_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("you dont got perms cuh", ephemeral=True)
    else:
        await interaction.response.send_message(f"an error has occurred: {error}", ephemeral=True)


@bot.tree.command(name="unmuteall", description="unmute everyone in the vc", guild=MY_GUILD)
@app_commands.checks.has_permissions(administrator=True)
async def unmute_all(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)

    member = interaction.user
    voice = member.voice

    if not voice or not voice.channel:
        await interaction.response.send_message("join a vc cuhzo")
        return

    channel = voice.channel
    unmuted = 0

    for m in channel.members:
        try:
            await m.edit(mute=False)
            unmuted += 1
        except discord.Forbidden:
            continue

    await interaction.followup.send(f"Unmuted {unmuted} people in {channel.name}", ephemeral=True)


@unmute_all.error
async def unmute_all_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("you dont got perms cuh", ephemeral=True)
    else:
        await interaction.response.send_message(f"an error has occurred: {error}", ephemeral=True)


@bot.tree.command(name="unmute", description="unmute someone", guild=MY_GUILD)
@app_commands.describe(member="the person to unmute")
@app_commands.checks.has_permissions(administrator=True)
async def unmute_member(interaction: discord.Interaction, member: discord.Member):
    if not member.voice or not member.voice.channel:
        await interaction.response.send_message(f"{member.display_name} is not in the vc", ephemeral=True)
        return

    try:
        await member.edit(mute=False)
        await interaction.response.send_message(f"Unmuted {member.display_name} in {member.voice.channel.name}", ephemeral=True)
    except discord.Forbidden:
        await interaction.response.send_message("no perms to unmute that person", ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"something went wrong: {e}", ephemeral=True)


@unmute_member.error
async def unmute_member_error(interaction: discord.Interaction, error):
    if isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message("you dont got perms cuh", ephemeral=True)
    else:
        await interaction.response.send_message(f"an error occurred: {error}", ephemeral=True)

bot.run(TOKEN)
