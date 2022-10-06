# importing the module
import yt_dlp
import os
import validators
import requests

# where to save
SAVE_PATH = os.getcwd()
URLS = []
DEBUGMODE = False

#MP3 OPTIONS
MP3_OPTS = {
    'format': 'mp3/bestaudio/best',
    'quiet': True if DEBUGMODE else False,
    'outtmpl': '%(title)s.%(ext)s',
    'postprocessors': [{  # Extract audio using ffmpeg
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
    }]
}

#MP4 OPTIONS
MP4_OPTS = {
    'format': 'mp4',
    'quiet': True if DEBUGMODE else False,
    'outtmpl': '%(title)s.%(ext)s'
}

#CLIP OPTIONS
CLIP_OPTS = {
    'format': 'mp4',
    'quiet': True if DEBUGMODE else False,
    'outtmpl': '%(title)s.%(ext)s',
    'download_ranges': None
}

def dranges(start, end):
    def timestamps(dict_info, ydl):
        return [{"start_time": start, "end_time": end}]
    return timestamps

def timestampSeconds(timestamp):
    convert = [1, 60, 60*60]
    hms = timestamp.split(':')
    hms.reverse()
    totalseconds = 0
    try:
        for i in range(len(hms)):
            totalseconds += int(hms[i]) * convert[i]
    except ValueError:
        return -1
    return totalseconds

def pixelupload(file):
    response = requests.post(
        "https://pixeldrain.com/api/file",
        data={"anonymous": True},
        files={"file": open(file, "rb")}
    )
    return response.json()

def downloadany(urls, location, opts):
    with yt_dlp.YoutubeDL(opts) as ydl:
        os.chdir(location)
        try:
            info = ydl.extract_info(urls[0], download=False)
            error_code = ydl.download(urls)
            return (error_code, info["title"] + "." + opts["format"].split("/")[0])
        except yt_dlp.utils.DownloadError as e:
            print(e) #print error
            return (-1, "None")

def downloadmp3(urls, location):
    with yt_dlp.YoutubeDL(MP3_OPTS) as ydl:
        os.chdir(location)
        try:
            info = ydl.extract_info(urls[0], download=False)
            error_code = ydl.download(urls)
            return (error_code, info["title"] + ".mp3")
        except yt_dlp.utils.DownloadError as e:
            print(e) #print error
            return (-1, "None")
    

def downloadmp4(urls, location):
    with yt_dlp.YoutubeDL(MP4_OPTS) as ydl:
        os.chdir(location)
        try:
            info = ydl.extract_info(urls[0], download=False)
            error_code = ydl.download(urls)
            return (error_code, info["title"] + ".mp4")
        except yt_dlp.utils.DownloadError as e:
            print(e) #print error
            return (-1, "None")
    
TEST_OPTS = { #this doesnt work :( --v
    'format': 'bestvideo[height<=720][ext=mp4]',
    'quiet': True if DEBUGMODE else False,
    'outtmpl': '%(title)s.%(ext)s'
}


if __name__ == '__main__':
    #testing without using bot
    url = []
    while True:
        userinput = input("Enter url: ")
        if not validators.url(userinput.strip()):
            if DEBUGMODE: print("Invalid url")
            break
        url.append(userinput)
    downloadany(url, SAVE_PATH, MP4_OPTS)
    pass



