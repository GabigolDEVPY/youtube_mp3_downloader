import yt_dlp
import os
import shutil
from core import settings
from django.conf import settings
import re

media_path = os.path.join(settings.BASE_DIR, 'media')
os.makedirs(media_path, exist_ok=True)

def sanitize_filename(name):
    return re.sub(r'[<>:"/\\|?*]', '', name)

class Yt:
    def __init__(self, url):
        self.url = url
        self.info_opts = {
                    'quiet': True,
                    'noplaylist': True,
                    'cookiefile': 'cookies.txt',
        }
        self.info = self.get_info()
        clean_title = sanitize_filename(self.info["title"])
        
        self.download_opts = {
                    'format': 'bestaudio/best',
                    'ffmpeg_location': r'F:\WINDOWS\PROGRAMACAO_TUDO\Youtube_music_downloader\ffmpeg-8.0.1-essentials_build\bin',
                    'noplaylist': True,
                    "outtmpl": os.path.join(media_path, f"{clean_title}.%(ext)s"),
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'cookiefile': 'cookies.txt',
                }
        self.get_info()
    def get_info(self):
        with yt_dlp.YoutubeDL(self.info_opts) as ydl:
            info = ydl.extract_info(self.url, download=False)
        
        return {
        "title": sanitize_filename(info.get("title")),
        "uploader": info.get("uploader"),
        "duration": info.get("duration"),
        "view_count": info.get("view_count"),
        "thumbnail": info.get("thumbnail"),
        }
    
    
    def download(self):
        with yt_dlp.YoutubeDL(self.download_opts) as ydl:
            ydl.download([self.url])

def clear_folder():
    path = os.path.join(settings.BASE_DIR, 'media')
    shutil.rmtree(path)
    os.mkdir(path)