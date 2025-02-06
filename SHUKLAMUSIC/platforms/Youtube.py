import asyncio
import os
import re
from typing import Union
import yt_dlp
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message
from youtubesearchpython.__future__ import VideosSearch
from SHUKLAMUSIC.utils.database import is_on_off
from SHUKLAMUSIC.utils.formatters import time_to_seconds

# تنظیمات پیشرفته برای yt-dlp
YDL_OPTIONS = {
    'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
    'geo-bypass': True,
    'nocheckcertificate': True,
    'noplaylist': True,
    'quiet': True,
    'no_warnings': True,
    'cookiefile': 'SHUKLAMUSIC/assets/cookies.txt',
    'age-limit': 99,
    'extract_flat': True,
    'youtube_include_dash_manifest': False,
    'allow_unplayable_formats': True,
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'extractor-args': 'youtube:player-client=android',
    'allow_multiple_video_streams': True,
    'allow_multiple_audio_streams': True,
    'check_formats': True,
    'prefer_ffmpeg': True,
    'concurrent_fragment_downloads': 10,
}

async def shell_cmd(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    out, errorz = await proc.communicate()
    if errorz:
        if "unavailable videos are hidden" in (errorz.decode("utf-8")).lower():
            return out.decode("utf-8")
        else:
            return errorz.decode("utf-8")
    return out.decode("utf-8")

class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be)"
        self.status = "https://www.youtube.com/oembed?url="
        self.listbase = "https://youtube.com/playlist?list="
        self.reg = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
        self.ydl = yt_dlp.YoutubeDL(YDL_OPTIONS)

    async def exists(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if re.search(self.regex, link):
            return True
        else:
            return False

    async def url(self, message_1: Message) -> Union[str, None]:
        messages = [message_1]
        if message_1.reply_to_message:
            messages.append(message_1.reply_to_message)
        text = ""
        offset = None
        length = None
        for message in messages:
            if offset:
                break
            if message.entities:
                for entity in message.entities:
                    if entity.type == MessageEntityType.URL:
                        text = message.text or message.caption
                        offset, length = entity.offset, entity.length
                        break
            elif message.caption_entities:
                for entity in message.caption_entities:
                    if entity.type == MessageEntityType.TEXT_LINK:
                        return entity.url
        if offset in (None,):
            return None
        return text[offset : offset + length]

    async def details(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            title = result["title"]
            duration_min = result["duration"]
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            vidid = result["id"]
            if str(duration_min) == "None":
                duration_sec = 0
            else:
                duration_sec = int(time_to_seconds(duration_min))
        return title, duration_min, duration_sec, thumbnail, vidid

    async def title(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            title = result["title"]
        return title

    async def duration(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            duration = result["duration"]
        return duration

    async def thumbnail(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        return thumbnail

    async def video(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
            
        try:
            info = await asyncio.get_event_loop().run_in_executor(
                None, 
                lambda: self.ydl.extract_info(link, download=False)
            )
            
            formats = info.get('formats', [])
            best_video = None
            for f in formats:
                if f.get('ext') == 'mp4' and f.get('format_note'):
                    if not best_video or int(f.get('height', 0)) > int(best_video.get('height', 0)):
                        best_video = f
            
            if best_video:
                return 1, best_video['url']
            else:
                return 0, "No suitable format found"
                
        except Exception as e:
            return 0, str(e)

    async def playlist(self, link, limit, user_id, videoid: Union[bool, str] = None):
        if videoid:
            link = self.listbase + link
        if "&" in link:
            link = link.split("&")[0]
        
        try:
            info = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.ydl.extract_info(link, download=False)
            )
            
            entries = info.get('entries', [])
            playlist_urls = []
            for entry in entries[:limit]:
                playlist_urls.append(entry.get('id', ''))
            return playlist_urls
            
        except Exception as e:
            print(f"Playlist Error: {str(e)}")
            return []

    async def track(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        results = VideosSearch(link, limit=1)
        for result in (await results.next())["result"]:
            title = result["title"]
            duration_min = result["duration"]
            vidid = result["id"]
            yturl = result["link"]
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
        track_details = {
            "title": title,
            "link": yturl,
            "vidid": vidid,
            "duration_min": duration_min,
            "thumb": thumbnail,
        }
        return track_details, vidid

    async def formats(self, link: str, videoid: Union[bool, str] = None):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
            
        try:
            info = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.ydl.extract_info(link, download=False)
            )
            
            formats = info.get('formats', [])
            formats_list = []
            
            for f in formats:
                if f.get('format_note') and f.get('ext') == 'mp4':
                    formats_list.append({
                        'format': f.get('format', ''),
                        'filesize': f.get('filesize', 0),
                        'format_id': f.get('format_id', ''),
                        'ext': f.get('ext', ''),
                        'format_note': f.get('format_note', ''),
                        'yturl': link
                    })
                    
            return formats_list, link
            
        except Exception as e:
            print(f"Formats Error: {str(e)}")
            return [], link

    async def slider(
        self,
        link: str,
        query_type: int,
        videoid: Union[bool, str] = None,
    ):
        if videoid:
            link = self.base + link
        if "&" in link:
            link = link.split("&")[0]
        a = VideosSearch(link, limit=10)
        result = (await a.next()).get("result")
        title = result[query_type]["title"]
        duration_min = result[query_type]["duration"]
        vidid = result[query_type]["id"]
        thumbnail = result[query_type]["thumbnails"][0]["url"].split("?")[0]
        return title, duration_min, thumbnail, vidid

    async def download(
        self,
        link: str,
        mystic,
        video: Union[bool, str] = None,
        videoid: Union[bool, str] = None,
        songaudio: Union[bool, str] = None,
        songvideo: Union[bool, str] = None,
        format_id: Union[bool, str] = None,
        title: Union[bool, str] = None,
    ) -> str:
        if videoid:
            link = self.base + link
            
        ydl_opts = {
            **YDL_OPTIONS,
            'format': 'bestvideo[height<=?1080][ext=mp4]+bestaudio[ext=m4a]' if video else 'bestaudio/best',
            'outtmpl': f"downloads/{title if title else '%(title)s'}.%(ext)s",
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4',
            }] if video else [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]
        }

        try:
            info = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.ydl.extract_info(link, download=True)
            )
            
            path = self.ydl.prepare_filename(info)
            if not video:
                path = path.rsplit(".", 1)[0] + '.mp3'
            return path
            
        except Exception as e:
            print(f"Download Error: {str(e)}")
            return None
