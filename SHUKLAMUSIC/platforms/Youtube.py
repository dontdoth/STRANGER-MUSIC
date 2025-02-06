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

# تعریف مسیر فایل کوکی
COOKIES_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "cookies.txt")

# محتوای کوکی‌ها
COOKIES_CONTENT = """# Netscape HTTP Cookie File
# https://curl.haxx.se/rfc/cookie_spec.html
# This is a generated file! Do not edit.
.youtube.com	TRUE	/	TRUE	1735493186	GPS	1
.youtube.com	TRUE	/	TRUE	1751043400	VISITOR_INFO1_LIVE	WcywpbZGUHI
.youtube.com	TRUE	/	TRUE	0	YSC	R4vSYyZou1o
.youtube.com	TRUE	/	TRUE	1770051400	PREF	f6=40000080&tz=Africa.Cairo
.youtube.com	TRUE	/	TRUE	1770051399	SID	g.a000rwif6iD2x3FaYpNgivtJGWW4CL2MGOs6adyzfAkQyoatItYFWmYvnq-DEcLdEPAm1tgxigACgYKAR8SARYSFQHGX2MiOkr8hdmkOJ6-sdhSN0xB6BoVAUF8yKrrrdWhweezgbcwPZq9nueg0076
.youtube.com	TRUE	/	TRUE	1770051399	__Secure-1PSID	g.a000rwif6iD2x3FaYpNgivtJGWW4CL2MGOs6adyzfAkQyoatItYFMElO_tcyzuUUTuNAkTkHdgACgYKAQgSARYSFQHGX2MimwhaPxrvTpiQOHhSt-UAihoVAUF8yKpqjMkoVPMHp75Qsr2z8gCR0076
.youtube.com	TRUE	/	TRUE	1770051399	__Secure-3PSID	g.a000rwif6iD2x3FaYpNgivtJGWW4CL2MGOs6adyzfAkQyoatItYFkkIM9KpzRwW5Sll9u1i9mwACgYKARQSARYSFQHGX2Mig3N3Ccgnglx-hZyfW_3OuhoVAUF8yKrsJaDeKhz5y-gWWjsE-N6j0076
.youtube.com	TRUE	/	TRUE	1770051399	HSID	AODJM2g2pkpNICzL8
.youtube.com	TRUE	/	TRUE	1770051399	SSID	AkVwj6aTB0CC7IPY9
.youtube.com	TRUE	/	TRUE	1770051399	APISID	bXYtyFBoJGyxEtRA/A6-SFypzGfFmnohwL
.youtube.com	TRUE	/	TRUE	1770051399	SAPISID	fNwoSGQDglZOcDjQ/AVZWC-ogcRva_FaX1
.youtube.com	TRUE	/	TRUE	1770051399	__Secure-1PAPISID	fNwoSGQDglZOcDjQ/AVZWC-ogcRva_FaX1
.youtube.com	TRUE	/	TRUE	1770051399	__Secure-3PAPISID	fNwoSGQDglZOcDjQ/AVZWC-ogcRva_FaX1
.youtube.com	TRUE	/	TRUE	1767027405	SIDCC	AKEyXzVEw4P2t3_rzqJJQVbzJiw8LcK14Oan_PBlQSbFKPiUZ5oTuHPaiYquGrxEk4O2v-H_Lg
.youtube.com	TRUE	/	TRUE	1767027405	__Secure-1PSIDCC	AKEyXzWbH9dhGrbxD4WgxeGuoA-To6b6_Kuxge2QUZhFk3aYpm7mI-rdyVr8JDZMD65jEeb1
.youtube.com	TRUE	/	TRUE	1767027405	__Secure-3PSIDCC	AKEyXzXjhGhd0Vb4TfAAIifc_alE_BZ-NUVlulytsiQ36O2IlSixWGrAHIKYdex_R2BEX2FExA
.youtube.com	TRUE	/	TRUE	1770051400	LOGIN_INFO	AFmmF2swRAIgK1BeoDNqzFc9GY69uGJE5eorD47wBxzSHu97gotTceACIG39RoiGG2-ZH54hnAhKOuKBlGKjkN1wD5g5WrHxi3Fl:QUQ3MjNmempWX0JaRTBpNzdOYW12YVJlSGVZT2t5STU0cWVWU1dtRUpldEtEWXVWSXZSem1XU0N0UnZRejFIZnQxRnlFSXUzWGtpczZ5dHdvaVhGcFUwNjdUS1JlVnVtZmRDUHcyTkVYazRkZkZueVlvSElfV0F5anRGNllwVTcyZTJFR0NqalZuZXpEZThrdk5OTGR2dGlLTVNqZ0hLUThn
.youtube.com	TRUE	/	TRUE	1767027399	__Secure-1PSIDTS	sidts-CjEB7wV3sYE1exL2fUvO4gJEeHbpxu953fvdGGLfe5yu7sU3oqLrmu7MnThnDT75ht_DEAA
.youtube.com	TRUE	/	TRUE	1767027399	__Secure-3PSIDTS	sidts-CjEB7wV3sYE1exL2fUvO4gJEeHbpxu953fvdGGLfe5yu7sU3oqLrmu7MnThnDT75ht_DEAA"""

def ensure_cookies_file():
    os.makedirs(os.path.dirname(COOKIES_FILE), exist_ok=True)
    if not os.path.exists(COOKIES_FILE):
        with open(COOKIES_FILE, 'w', encoding='utf-8') as f:
            f.write(COOKIES_CONTENT)

class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be)"
        self.status = "https://www.youtube.com/oembed?url="
        self.listbase = "https://youtube.com/playlist?list="
        self.reg = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
        ensure_cookies_file()

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
        proc = await asyncio.create_subprocess_exec(
            "yt-dlp",
            "--cookies", COOKIES_FILE,
            "-g",
            "-f",
            "best[height<=?720][width<=?1280]",
            f"{link}",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        if stdout:
            return 1, stdout.decode().split("\n")[0]
        else:
            return 0, stderr.decode()

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
        loop = asyncio.get_running_loop()

        def audio_dl():
            ydl_optssx = {
                "format": "bestaudio/best",
                "outtmpl": "downloads/%(id)s.%(ext)s",
                "geo_bypass": True,
                "nocheckcertificate": True,
                "quiet": True,
                "no_warnings": True,
                "cookiefile": COOKIES_FILE,
            }
            x = yt_dlp.YoutubeDL(ydl_optssx)
            info = x.extract_info(link, False)
            xyz = os.path.join("downloads", f"{info['id']}.{info['ext']}")
            if os.path.exists(xyz):
                return xyz
            x.download([link])
            return xyz

        def video_dl():
            ydl_optssx = {
                "format": "(bestvideo[height<=?720][width<=?1280][ext=mp4])+(bestaudio[ext=m4a])",
                "outtmpl": "downloads/%(id)s.%(ext)s",
                "geo_bypass": True,
                "nocheckcertificate": True,
                "quiet": True,
                "no_warnings": True,
                "cookiefile": COOKIES_FILE,
            }
            x = yt_dlp.YoutubeDL(ydl_optssx)
            info = x.extract_info(link, False)
            xyz = os.path.join("downloads", f"{info['id']}.{info['ext']}")
            if os.path.exists(xyz):
                return xyz
            x.download([link])
            return xyz

        def song_video_dl():
            formats = f"{format_id}+140"
            fpath = f"downloads/{title}"
            ydl_optssx = {
                "format": formats,
                "outtmpl": fpath,
                "geo_bypass": True,
                "nocheckcertificate": True,
                "quiet": True,
                "no_warnings": True,
                "prefer_ffmpeg": True,
                "merge_output_format": "mp4",
                "cookiefile": COOKIES_FILE,
            }
            x = yt_dlp.YoutubeDL(ydl_optssx)
            x.download([link])

        def song_audio_dl():
            fpath = f"downloads/{title}.%(ext)s"
            ydl_optssx = {
                "format": format_id,
                "outtmpl": fpath,
                "geo_bypass": True,
                "nocheckcertificate": True,
                "quiet": True,
                "no_warnings": True,
                "prefer_ffmpeg": True,
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": "mp3",
                        "preferredquality": "192",
                    }
                ],
                "cookiefile": COOKIES_FILE,
            }
            x = yt_dlp.YoutubeDL(ydl_optssx)
            x.download([link])

        if songvideo:
            await loop.run_in_executor(None, song_video_dl)
            fpath = f"downloads/{title}.mp4"
            return fpath
        elif songaudio:
            await loop.run_in_executor(None, song_audio_dl)
            fpath = f"downloads/{title}.mp3"
            return fpath
        elif video:
            if await is_on_off(1):
                direct = True
                downloaded_file = await loop.run_in_executor(None, video_dl)
            else:
                proc = await asyncio.create_subprocess_exec(
                    "yt-dlp",
                    "--cookies", COOKIES_FILE,
                    "-g",
                    "-f",
                    "best[height<=?720][width<=?1280]",
                    f"{link}",
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )
                stdout, stderr = await proc.communicate()
                if stdout:
                    downloaded_file = stdout.decode().split("\n")[0]
                    direct = None
                else:
                    return
        else:
            direct = True
            downloaded_file = await loop.run_in_executor(None, audio_dl)
        return downloaded_file, direct
