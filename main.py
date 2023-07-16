import discord
from discord import app_commands
from discord.ext import commands
from discord.ext import tasks
from discord import ui
import asyncio
import aiohttp
import time
from datetime import datetime

bot = commands.Bot(command_prefix="!",intents=discord.Intents.all())
admin_role = 1049355483389108354
game_steam_id = 1943950
guild_id = 881579672725487656
token = "YOUR_TOKEN_HERE"

@bot.event
async def on_ready():
    print("The Discord bot is online...")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
            print(e)
    await my_loop.start()
    print("Started scanning for updates...")
   

@bot.tree.command(name="help")
async def help(interaction: discord.Integration):
    embed = discord.Embed(title = "Bot Commands" , description = f"`/help` - Get a list of commands.\n`/ping` - Get the current bot's ping." , color = discord.Color.green())
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="ping")
#@app_commands.describe(thing_to_say = "What should I say?")
async def ping(intergration: discord.Integration):
    bot_ping = round(bot.latency * 1000)
    embed = discord.Embed(title = "Bot's Ping" , description = f"🏓 Pong!\n The Discord bot's ping is {bot_ping}ms." , color = discord.Color.green())
    await intergration.response.send_message(embed=embed)

#!-- Dev tool
@bot.tree.command(name="publishbuild")
@commands.has_role(admin_role)
@app_commands.describe(build_id = "The Steam build ID.")
@app_commands.describe(build_time = "The time it was released. (UNIX Time)")
@app_commands.describe(public = "Is the build public? (True/False)")
@app_commands.describe(title = "What is the title of this build?")

async def ping(intergration: discord.Integration, build_id: int, build_time: int, public: bool, title: str = "No Title"):
    if title == "No Title":
        title = "No Title"
    if public == False:
        embed = discord.Embed(title = "Escape The Backrooms Development Build" , description = f"📖 **Title:** [Non Public] *{title}*\n📋 **Build ID:** `{build_id}`\n📆 **Released:** <t:{build_time}:f>\n⏰ **Relative:** <t:{build_time}:R>" , color = discord.Color.red())
        embed.set_footer(text=f"This is an automated request")
    else:
        embed = discord.Embed(title = "Escape The Backrooms Update" , description = f"📖 **Title:** [Public] *{title}*\n📋 **Build ID:** `{build_id}`\n📆 **Released:** <t:{build_time}:f>\n⏰ **Relative:** <t:{build_time}:R>" , color = discord.Color.green())
        embed.set_footer(text=f"This is an automated request")       
    channel = bot.get_channel(1049158707646320730)
    await channel.send(embed=embed)

@bot.tree.command(name="latestbuild")
async def latestbuild(intergration: discord.Integration):    
    api_id = game_steam_id
    api_url = f"https://api.steamcmd.net/v1/info/{api_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            api_data = await response.json()
    build_id = api_data['data'][f'{api_id}']['depots']['branches']['development']['buildid']
    build_time = api_data['data'][f'{api_id}']['depots']['branches']['development']['timeupdated']
    info = intergration.user
    embed = discord.Embed(title = "Escape The Backrooms Latest Development Build" , description = f"📖 **Title:** [Non Public] *No Title*\n📋 **Build ID:** `{build_id}`\n📆 **Released:** <t:{build_time}:f>\n⏰ **Relative:** <t:{build_time}:R>" , color = discord.Color.red())
    embed.set_footer(text=f"Requested by {info}")
    await intergration.response.send_message(embed=embed)    

@bot.tree.command(name="latestupdate")
async def latestbuild(intergration: discord.Integration):    
    api_id = game_steam_id
    api_url = f"https://api.steamcmd.net/v1/info/{api_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            api_data = await response.json()
    build_id = api_data['data'][f'{api_id}']['depots']['branches']['public']['buildid']
    build_time = api_data['data'][f'{api_id}']['depots']['branches']['public']['timeupdated']
    info = intergration.user
    embed = discord.Embed(title = "Escape The Backrooms Latest Update" , description = f"📖 **Title:** [Public] *No Title*\n📋 **Build ID:** `{build_id}`\n📆 **Released:** <t:{build_time}:f>\n⏰ **Relative:** <t:{build_time}:R>" , color = discord.Color.green())
    embed.set_footer(text=f"Requested by {info}")
    await intergration.response.send_message(embed=embed)

@bot.tree.command(name="players")
async def players(intergration: discord.Integration):    
    api_id = game_steam_id
    api_url = f"http://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/?appid={api_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            api_data = await response.json()
    player_count = api_data['response']['player_count']
    request_time = int(time.time())
    info = intergration.user
    embed = discord.Embed(title = "Escape The Backrooms Player Count" , description = f"📆 **Time:** <t:{request_time}:f>\n📖 **Players:** `{player_count}`" , color = discord.Color.green())
    embed.set_footer(text=f"Requested by {info}")
    await intergration.response.send_message(embed=embed)
    f = open("count.txt", "a")
    f.write(f"{player_count}, {request_time}\n")
    f.close()

#Modal Test
class my_modal(ui.Modal, title = "Say Somthing"):
    answer = ui.TextInput(label= "What would you like to say?", style= discord.TextStyle.short, placeholder= "Hello, World!", required= True)

    async def on_submit(self, interaction: discord.Integration):
        #embed = discord.Embed(title= self.title, description= f"**{self.answer.label}**\n{self.answer}", timestamp= datetime.now(), color = discord.Color.green())
        #embed.set_author(name= interaction.user, icon_url=interaction.user.avatar)
        channel = interaction.channel
        await interaction.response.send_message("Successfuly said your message.", ephemeral= True)
        await channel.send(f"{self.answer}")

@bot.tree.command(name="say")
@commands.has_role(admin_role)
async def send_modal(interaction: discord.Integration):
    await interaction.response.send_modal(my_modal())   


@tasks.loop(minutes=2)
async def my_loop():
    # Check for updates using the Steamcmd API
    api_id = game_steam_id
    api_url = f"https://api.steamcmd.net/v1/info/{api_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            api_data = await response.json()

    #!-- Development Branch Builds
    build_id = api_data['data'][f'{api_id}']['depots']['branches']['development']['buildid']
    f = open("dev_builds.txt", "r")
    file_info = f.read()
    file_result = build_id in file_info
    f.close()
    if file_result is True:
        await my_loop2()
        return
    else:
        f = open("dev_builds.txt", "a")
        f.write(f"\n{build_id}")
        f.close()
        print(f"Build detected, added a build with the id of \"{build_id}\" to database...")
        build_time = api_data['data'][f'{api_id}']['depots']['branches']['development']['timeupdated']
        embed = discord.Embed(title = "Escape The Backrooms Development Build" , description = f"📖 **Title:** [Non Public] *No Title*\n📋 **Build ID:** `{build_id}`\n📆 **Released:** <t:{build_time}:f>\n⏰ **Relative:** <t:{build_time}:R>" , color = discord.Color.red())
        embed.set_footer(text=f"This is an automated request")
        channel = bot.get_channel(1049158707646320730)
        #!-- Send the message
        await channel.send(embed=embed)
        ping = await channel.send("<@&1063059746430668820>")
        await asyncio.sleep(1)
        await ping.delete()
    await my_loop2()

async def my_loop2():
    # Check for updates using the Steamcmd API
    api_id = game_steam_id
    api_url = f"https://api.steamcmd.net/v1/info/{api_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as response:
            api_data = await response.json()
    #!-- Public Branch Builds
    build_id = api_data['data'][f'{api_id}']['depots']['branches']['public']['buildid']
    f = open("public_builds.txt", "r")
    file_info = f.read()
    file_result = build_id in file_info
    f.close()
    if file_result is True:
        return
    else:
        f = open("public_builds.txt", "a")
        f.write(f"\n{build_id}")
        f.close()
        build_time = api_data['data'][f'{api_id}']['depots']['branches']['public']['timeupdated']
        patch_api = f"http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid={api_id}&count=3&maxlength=3&format=JSON"
        async with aiohttp.ClientSession() as session:
            async with session.get(patch_api) as response:
                patch_data = await response.json()
        patch_id = patch_data['appnews']['newsitems'][0]['gid']
        f = open("patches.txt", "r")
        file_info = f.read()
        file_result = patch_id in file_info
        f.close()
        if file_result is True:
            build_title = "No Title"
            print(f"Update detected, added a build with the id of \"{build_id}\" to database...")
            return
        else:
            patch_title = patch_data['appnews']['newsitems'][0]['title']
            build_title = patch_title
            f = open("patches.txt", "a")
            f.write(f"{patch_id}, {build_id}\n")
            f.close()
            print(f"Update detected, added a build with the id of \"{build_id}\" and title of \"{build_title}\" to database...")
        embed = discord.Embed(title = "Escape The Backrooms Public Build" , description = f"📖 **Title:** [Public] *{build_title}*\n📋 **Build ID:** `{build_id}`\n📆 **Released:** <t:{build_time}:f>\n⏰ **Relative:** <t:{build_time}:R>" , color = discord.Color.green())
        embed.set_footer(text=f"This is an automated request")
        channel = bot.get_channel(1049158707646320730)
        # Send the message
        await channel.send(embed=embed)
        ping = await channel.send("<@&1063059606617718785>")
        await asyncio.sleep(1)
        await ping.delete()

bot.run(token)