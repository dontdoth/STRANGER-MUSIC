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

# تنظیمات اصلی
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

def validate_cookies():
    """اعتبارسنجی کوکی‌ها"""
    if not os.path.exists(COOKIES_FILE):
        return False
    try:
        with open(COOKIES_FILE, 'r') as f:
            content = f.read()
            return 'youtube.com' in content and '.SIDCC' in content
    except:
        return False

def ensure_permissions():
    """اطمینان از دسترسی‌های لازم"""
    try:
        if os.path.exists(COOKIES_FILE):
            os.chmod(COOKIES_FILE, 0o644)
        if not os.path.exists("downloads"):
            os.makedirs("downloads")
        os.chmod("downloads", 0o755)
    except Exception as e:
        print(f"Permission error: {str(e)}")

def ensure_cookies_file():
    """اطمینان از وجود فایل کوکی"""
    os.makedirs(os.path.dirname(COOKIES_FILE), exist_ok=True)
    if not os.path.exists(COOKIES_FILE):
        with open(COOKIES_FILE, 'w', encoding='utf-8') as f:
            f.write(COOKIES_CONTENT)
    ensure_permissions()

async def shell_cmd(cmd):
    """اجرای دستورات شل"""
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
        try:
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
        except Exception as e:
            print(f"Error in details: {str(e)}")
            return None, None, None, None, None

    async def title(self, link: str, videoid: Union[bool, str] = None):
        try:
            if videoid:
                link = self.base + link
            if "&" in link:
                link = link.split("&")[0]
            results = VideosSearch(link, limit=1)
            for result in (await results.next())["result"]:
                title = result["title"]
            return title
        except Exception as e:
            print(f"Error in title: {str(e)}")
            return None

    async def duration(self, link: str, videoid: Union[bool, str] = None):
        try:
            if videoid:
                link = self.base + link
            if "&" in link:
                link = link.split("&")[0]
            results = VideosSearch(link, limit=1)
            for result in (await results.next())["result"]:
                duration = result["duration"]
            return duration
        except Exception as e:
            print(f"Error in duration: {str(e)}")
            return None

    async def thumbnail(self, link: str, videoid: Union[bool, str] = None):
        try:
            if videoid:
                link = self.base + link
            if "&" in link:
                link = link.split("&")[0]
            results = VideosSearch(link, limit=1)
            for result in (await results.next())["result"]:
                thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            return thumbnail
        except Exception as e:
            print(f"Error in thumbnail: {str(e)}")
            return None

    async def video(self, link: str, videoid: Union[bool, str] = None):
        try:
            if videoid:
                link = self.base + link
            if "&" in link:
                link = link.split("&")[0]

            ydl_opts = {
                'format': 'best[height<=?720][width<=?1280]',
                'quiet': True,
                'no_warnings': True,
                'cookiefile': COOKIES_FILE,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                try:
                    info = ydl.extract_info(link, download=False)
                    if info:
                        url = info.get('url', None)
                        if url:
                            return 1, url
                        else:
                            formats = info.get('formats', [None])
                            if formats[0]:
                                return 1, formats[0]['url']
                except Exception as e:
                    print(f"Error in video extraction: {str(e)}")
                    
            # اگر yt-dlp موفق نشد، از روش دوم استفاده کنیم
            proc = await asyncio.create_subprocess_exec(
                "yt-dlp",
                "--cookies", COOKIES_FILE,
                "-g",
                "-f", "best[height<=?720][width<=?1280]",
                f"{link}",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            stdout, stderr = await proc.communicate()
            if stdout:
                return 1, stdout.decode().strip()
            
            return 0, "Failed to extract video URL"
            
        except Exception as e:
            print(f"Error in video function: {str(e)}")
            return 0, str(e)

    async def playlist(self, link: str, limit: int, user_id: int, videoid: Union[bool, str] = None):
        try:
            if videoid:
                link = self.listbase + link
            if "&" in link:
                link = link.split("&")[0]
            playlist = await shell_cmd(
                f"yt-dlp --cookies {COOKIES_FILE} -i --get-id --flat-playlist --playlist-end {limit} --skip-download {link}"
            )
            try:
                result = playlist.split("\n")
                for key in result:
                    if key == "":
                        result.remove(key)
            except:
                result = []
            return result
        except Exception as e:
            print(f"Error in playlist: {str(e)}")
            return []

    async def track(self, link: str, videoid: Union[bool, str] = None):
        try:
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
        except Exception as e:
            print(f"Error in track: {str(e)}")
            return None, None

    async def formats(self, link: str, videoid: Union[bool, str] = None):
        try:
            if videoid:
                link = self.base + link
            if "&" in link:
                link = link.split("&")[0]
            ytdl_opts = {"quiet": True, "cookiefile": COOKIES_FILE}
            ydl = yt_dlp.YoutubeDL(ytdl_opts)
            with ydl:
                formats_available = []
                r = ydl.extract_info(link, download=False)
                for format in r["formats"]:
                    try:
                        str(format["format"])
                    except:
                        continue
                    if not "dash" in str(format["format"]).lower():
                        try:
                            format["format"]
                            format["filesize"]
                            format["format_id"]
                            format["ext"]
                            format["format_note"]
                        except:
                            continue
                        formats_available.append(
                            {
                                "format": format["format"],
                                "filesize": format["filesize"],
                                "format_id": format["format_id"],
                                "ext": format["ext"],
                                "format_note": format["format_note"],
                                "yturl": link,
                            }
                        )
            return formats_available, link
        except Exception as e:
            print(f"Error in formats: {str(e)}")
            return [], None

    async def slider(
        self,
        link: str,
        query_type: int,
        videoid: Union[bool, str] = None,
    ):
        try:
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
        except Exception as e:
            print(f"Error in slider: {str(e)}")
            return None, None, None, None

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
        try:
            if videoid:
                link = self.base + link
            loop = asyncio.get_running_loop()

            def audio_dl():
                try:
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
                except Exception as e:
                    print(f"Error in audio_dl: {str(e)}")
                    return None

            def video_dl():
                try:
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
                except Exception as e:
                    print(f"Error in video_dl: {str(e)}")
                    return None

            def song_video_dl():
                try:
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
                except Exception as e:
                    print(f"Error in song_video_dl: {str(e)}")

            def song_audio_dl():
                try:
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
                except Exception as e:
                    print(f"Error in song_audio_dl: {str(e)}")

            if songvideo:
                await loop.run_in_executor(None, song_video_dl)
                fpath = f"downloads/{title}.mp4"
                return fpath
            elif songaudio:
                await loop.run_in_executor(None, song_audio_dl)
                fpath = f"downloads/{title}.mp3"
                return fpath
            elif video:
                try:
                    if await is_on_off(1):
                        direct = True
                        downloaded_file = await loop.run_in_executor(None, video_dl)
                        if downloaded_file:
                            return downloaded_file, direct
                    
                    # اگر دانلود مستقیم موفق نبود، از روش دوم استفاده کنیم
                    status, url = await self.video(link)
                    if status == 1:
                        return url, None
                    else:
                        raise Exception("Failed to get video URL")
                except Exception as e:
                    print(f"Error in video download: {str(e)}")
                    return None, None
            else:
                direct = True
                downloaded_file = await loop.run_in_executor(None, audio_dl)
                if downloaded_file:
                    return downloaded_file, direct
                return None, None

        except Exception as e:
            print(f"Error in download function: {str(e)}")
            return None, None
