# Python Discord Bot
### Personal project

This is a Discord bot made using the disnake library. This bot contains several useful commands, currently the most useful being downloading videos (either as mp3 or mp4s) and uploading them to Discord with a simple command. If the file is too big and exceeds Discord's limit, it instead uploads the file onto a file hosting site and provides the user with a link. To check out the other commands, use the "?help" command for an example on how to use them.

## To use:

To use this program on a desktop, you will need to install ytp-dl dependency, as well as download ffmpeg for mp3 converting capabilites

To install yt-dlp:

```
python3 -m pip install -U yt-dlp
```

To install [**ffmpeg**](https://www.ffmpeg.org), put the ffmpeg.exe file in your python's Scripts folder

## To run:
make sure you have a config.json file that has your bot's token as 'botToken'. Additionally, you can add 'savePath' and provide the path you wish the downloads to be in, otherwise they will be downloaded in the directory where the bot is run from

After that, launch the "roobot.py" file and it should be good to go

