import yt_dlp

class Yt:
    def __init__(self, url):
        self.url = url
        self.info_opts = {
                    'quiet': True,
                    'noplaylist': True,
                    'cookiefile': 'cookies.txt',
        }
        
        self.download_opts = {
                    'format': 'best[protocol^=m3u8]/bestaudio/best',
                    'ffmpeg_location': r'F:\WINDOWS\PROGRAMACAO_TUDO\Youtube_music_downloader\ffmpeg-8.0.1-essentials_build\bin',
                    'noplaylist': True,
                    'outtmpl': '%(title)s.%(ext)s',
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
            self.info = ydl.extract_info(self.url, download=False)
                
        self.title = self.info.get("title")
        self.author = self.info.get("uploader")
        self.lenght = self.info.get("duration")
        self.views = self.info.get("view_count")
        self.thumb = self.info.get("thumbnail")
    
    
    def download(self):
        with yt_dlp.YoutubeDL(self.download_opts) as ydl:
            ydl.download([self.url])


url = input(str("Cole o link:"))
yt = Yt(url)
yt.download()