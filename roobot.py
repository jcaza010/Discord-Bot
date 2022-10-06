import os
import sys
from pathlib import Path
from videodl import *
import disnake
from disnake.ext import commands
import json

DISCORDLIMIT = 8 #megabytes
FILELIMIT = 100

description = """A personal bot with a few useful features"""

intents = disnake.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("?"), description=description, intents=intents
)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

@bot.command()
async def mp3(ctx, url, dest=""):
    """Download video as mp3. Send link instead of file if file size exceeds discord limit"""
    if not validators.url(url.strip()):
        if DEBUGMODE: print("Invalid url")
        return
    res = downloadany([url], SAVE_PATH, MP3_OPTS)
    if res[0] != 0:
        if DEBUGMODE: print("download failed")
        return
    if dest == 'local': return #stop here and keep file if destination is local (personal use)
    path = os.path.join(SAVE_PATH, res[1])
    filesize = os.stat(path).st_size / (1024 * 1024)
    if DEBUGMODE: print(f"{filesize}MB file")
    if filesize < DISCORDLIMIT: # < 8MB
        try:
            with open(Path(path), 'rb') as fp:
                await ctx.send(file=disnake.File(fp))
        except disnake.errors.HTTPException:
            await ctx.send("Something went wrong, please try again later")
    elif DISCORDLIMIT < filesize < FILELIMIT: # > 8MB and < 100 MB
        resp = pixelupload(path)
        if resp['success']: # checks if pixeldrain upload was a success
            pixurl = r"https://www.pixeldrain.com/u/" + resp["id"]
            await ctx.send(f"Pixeldrain link: {pixurl}")
        else:
            await ctx.send(f"There was an issue the downloaded file, please try again later")
    elif filesize > DISCORDLIMIT: # > 100MB
        await ctx.send(f"File WAY too big: {int(filesize)}MB")
    if dest != "local": os.remove(path)

@bot.command()
async def mp4(ctx, url, dest=""): #same as mp3 except with mp4 options, will create singular function if necessary
    """Download video as mp4. Send link instead of file if file size exceeds discord limit"""
    if not validators.url(url.strip()):
        if DEBUGMODE: print("Invalid url")
        return
    res = downloadany([url], SAVE_PATH, MP4_OPTS)
    if res[0] != 0:
        if DEBUGMODE: print("download failed")
        return
    if dest == 'local': return #stop here and keep file if destination is local (personal use)
    path = os.path.join(SAVE_PATH, res[1])
    filesize = os.stat(path).st_size / (1024 * 1024)
    if DEBUGMODE: print(f"{filesize}MB file")
    if filesize < DISCORDLIMIT: # < 8MB
        try:
            with open(Path(path), 'rb') as fp:
                await ctx.send(file=disnake.File(fp))
        except disnake.errors.HTTPException:
            await ctx.send("Something went wrong, please try again later")
    elif DISCORDLIMIT < filesize < FILELIMIT: # > 8MB and < 100 MB
        resp = pixelupload(path)
        if resp['success']: # checks if pixeldrain upload was a success
            pixurl = r"https://www.pixeldrain.com/u/" + resp["id"]
            await ctx.send(f"Pixeldrain link: {pixurl}")
        else:
            await ctx.send(f"There was an issue the downloaded file, please try again later")
    elif filesize > DISCORDLIMIT: # > 100MB
        await ctx.send(f"File WAY too big: {int(filesize)}MB")
    if dest != "local": os.remove(path)

@bot.command()
async def clip(ctx, url, start, end, dest=""): #same as mp3 except with mp4 options, will create singular function if necessary
    """Download video clip as mp4 given timestamps. Send link instead of file if file size exceeds discord limit"""
    if not validators.url(url.strip()):
        if DEBUGMODE: print("Invalid url")
        return
    startseconds = timestampSeconds(start)
    if startseconds < 0:
        await ctx.send("invalid start time")
        return
    endseconds = timestampSeconds(end)
    if endseconds < 0:
        await ctx.send("invalid end time")
        return
    CLIP_OPTS["download_ranges"] = dranges(startseconds, endseconds)
    res = downloadany([url], SAVE_PATH, CLIP_OPTS)
    if res[0] != 0:
        if DEBUGMODE: print("download failed")
        return
    if dest == 'local': return #stop here and keep file if destination is local (personal use)
    path = os.path.join(SAVE_PATH, res[1])
    filesize = os.stat(path).st_size / (1024 * 1024)
    if DEBUGMODE: print(f"{filesize}MB file")
    if filesize < DISCORDLIMIT: # < 8MB
        try:
            with open(Path(path), 'rb') as fp:
                await ctx.send(file=disnake.File(fp))
        except disnake.errors.HTTPException:
            await ctx.send("Something went wrong, please try again later")
    elif DISCORDLIMIT < filesize < FILELIMIT: # > 8MB and < 100 MB
        resp = pixelupload(path)
        if resp['success']: # checks if pixeldrain upload was a success
            pixurl = r"https://www.pixeldrain.com/u/" + resp["id"]
            await ctx.send(f"Pixeldrain link: {pixurl}")
        else:
            await ctx.send(f"There was an issue the downloaded file, please try again later")
    elif filesize > DISCORDLIMIT: # > 100MB
        await ctx.send(f"File WAY too big: {int(filesize)}MB")
    if dest != "local": os.remove(path)

@bot.command()
@commands.has_permissions(administrator = True)
async def nuke(ctx, num=5):
    '''Deletes the last number of messages in a channel'''
    await ctx.channel.purge(limit=num)

@bot.command()
async def allcoms(ctx):
    '''Displays public commands for anyone to use'''
    message = "All commands\n?mp3 <url>\n?mp4 <url>\n?clip <url> <start_timestamp> <end_timestamp>\n"
    await ctx.send(message)

#@bot.command()
#@commands.is_owner() IN PROGRESS
#async def fetch(ctx, directory=""):
#    '''Get files and folders from given directory, similar to the cd terminal command'''
#    message = ""
#    if directory == "":
#        directory = os.getcwd()
#    else:
#        directory = f'{os.getcwd()}\\directory'

#@bot.command()
#@commands.is_owner()
#async def restart(ctx, directory=""): IN PROGRESS
#    "Restarts the bot in case any changes were made"
#    await ctx.send(f"Restarting...")
#    os.chdir(Path(sys.argv).parent)
#    os.execv(sys.executable, ['python'] + [os.path.basename(sys.argv[0])])

@bot.command()
async def add(ctx, left: int, right: int):
    '''Default command. Just to test if bot is online and working'''
    await ctx.send(left + right)

@bot.command()
async def joined(ctx, member: disnake.Member):
    """Default command. Sends message saying when user joined"""
    await ctx.send(f"{member.name} joined in {member.joined_at}")

@bot.event
async def on_command_error(ctx, error):
    '''Sends error messages according to permissions of user or bot'''
    if isinstance(error, disnake.ext.commands.errors.MissingPermissions):
        await ctx.send("You do not have adequate permissions for this command")
    #elif isinstance(error, disnake.ext.commands.errors.CommandInvokeError): Sometimes error not related to bot permissions
    #    await ctx.send("This bot does not have adequate permissions for this command") 
    print(error)   

if __name__ == "__main__":
    try:
        with open("config.json", "r") as c:
            data = json.load(c)
        if "savePath" in data.keys(): SAVE_PATH = Path(data["savePath"])
        bot.run(data["botToken"])
    except FileNotFoundError:
        print("Config file not found")