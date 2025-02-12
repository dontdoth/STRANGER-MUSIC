from SHUKLAMUSIC import app
from pyrogram.errors import RPCError
from pyrogram.types import ChatMemberUpdated, InlineKeyboardMarkup, InlineKeyboardButton
from os import environ
from typing import Union, Optional
from PIL import Image, ImageDraw, ImageFont
from os import environ
import random
from pyrogram import Client, filters
from pyrogram.types import ChatJoinRequest, InlineKeyboardButton, InlineKeyboardMarkup
from PIL import Image, ImageDraw, ImageFont
import asyncio, os, time, aiohttp
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
from asyncio import sleep
from pyrogram import filters, Client, enums
from pyrogram.enums import ParseMode
from logging import getLogger
from SHUKLAMUSIC.utils.Shukla_ban import admin_filter
from PIL import ImageDraw, Image, ImageFont, ImageChops
from pyrogram import *
from pyrogram.types import *
from logging import getLogger
from pyrogram import Client, filters
import requests
import random
import os
import re
import asyncio
import time
from SHUKLAMUSIC.utils.database import add_served_chat
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from SHUKLAMUSIC.utils.database import get_assistant
import asyncio
from SHUKLAMUSIC.misc import SUDOERS
from SHUKLAMUSIC.mongo.afkdb import PROCESS
from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant
from SHUKLAMUSIC import app
import asyncio
import random
from pyrogram import Client, filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import (
    ChatAdminRequired,
    InviteRequestSent,
    UserAlreadyParticipant,
    UserNotParticipant,
)
from SHUKLAMUSIC.utils.database import get_assistant, is_active_chat



random_photo = [
    "https://telegra.ph/file/1949480f01355b4e87d26.jpg",
    "https://telegra.ph/file/3ef2cc0ad2bc548bafb30.jpg",
    "https://telegra.ph/file/a7d663cd2de689b811729.jpg",
    "https://telegra.ph/file/6f19dc23847f5b005e922.jpg",
    "https://telegra.ph/file/2973150dd62fd27a3a6ba.jpg",
]

class WelDatabase:
    def __init__(self):
        self.data = {}

    async def find_one(self, chat_id):
        return chat_id in self.data

    async def add_wlcm(self, chat_id):
        self.data[chat_id] = {"state": "on"}

    async def rm_wlcm(self, chat_id):
        if chat_id in self.data:
            del self.data[chat_id]

wlcm = WelDatabase()

class temp:
    ME = None
    CURRENT = 2
    CANCEL = False
    MELCOW = {}
    U_NAME = None
    B_NAME = None

def circle(pfp, size=(500, 500), brightness_factor=10):
    try:
        pfp = pfp.resize(size, Image.ANTIALIAS).convert("RGBA")
        pfp = ImageEnhance.Brightness(pfp).enhance(brightness_factor)
        bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
        mask = Image.new("L", bigsize, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + bigsize, fill=255)
        mask = mask.resize(pfp.size, Image.ANTIALIAS)
        mask = ImageChops.darker(mask, pfp.split()[-1])
        pfp.putalpha(mask)
        return pfp
    except Exception as e:
        LOGGER.error(f"Error in circle function: {str(e)}")
        return None

def welcomepic(pic, user, chatname, id, uname):
    try:
        background = Image.open("SHUKLAMUSIC/assets/wel2.png")
        pfp = Image.open(pic).convert("RGBA")
        pfp = circle(pfp)
        pfp = pfp.resize((500, 500))
        background.paste(pfp, (48, 88), pfp)
        
        draw = ImageDraw.Draw(background)
        font = ImageFont.truetype('SHUKLAMUSIC/assets/font.ttf', size=60)
        draw.text((630, 450), f'ID: {id}', fill=(255, 255, 255), font=font)
        
        output_path = f"downloads/welcome#{id}.png"
        background.save(output_path)
        return output_path
    except Exception as e:
        LOGGER.error(f"Error in welcomepic function: {str(e)}")
        return None

@app.on_message(filters.command("welcome") & ~filters.private)
async def welcome_toggle(_, message):
    try:
        if len(message.command) != 2:
            return await message.reply_text("**روش استفاده:**\n**/welcome [on|off]**")

        status = message.command[1].lower()
        chat_id = message.chat.id
        user = await app.get_chat_member(chat_id, message.from_user.id)
        
        if user.status not in (ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER):
            return await message.reply("**فقط ادمین‌ها می‌توانند از این دستور استفاده کنند!**")

        if status == "on":
            await wlcm.rm_wlcm(chat_id)
            await message.reply_text("**خوش‌آمدگویی فعال شد ✅**")
        elif status == "off":
            await wlcm.add_wlcm(chat_id)
            await message.reply_text("**خوش‌آمدگویی غیرفعال شد ❌**")
        else:
            await message.reply_text("**لطفا فقط از on یا off استفاده کنید!**")
    except Exception as e:
        await message.reply_text(f"خطا: {str(e)}")

@app.on_chat_member_updated(filters.group)
async def welcome_handler(_, member: ChatMemberUpdated):
    try:
        chat_id = member.chat.id
        if await wlcm.find_one(chat_id):
            return

        if not member.new_chat_member or member.new_chat_member.status == "kicked":
            return

        user = member.new_chat_member.user
        count = await app.get_chat_members_count(chat_id)

        try:
            pic = await app.download_media(user.photo.big_file_id, file_name=f"pp{user.id}.png")
        except:
            pic = "SHUKLAMUSIC/assets/upic.png"

        welcome_photo = welcomepic(
            pic, user.first_name, member.chat.title, user.id, user.username
        )

        if welcome_photo:
            await app.send_photo(
                chat_id,
                photo=welcome_photo,
                caption=f"""
**⎊───── خوش آمدید ─────⎊**

**▬▭▬▭▬▭▬▭▬▭▬▭▬▭▬**

**☉ نام ⧽** {user.mention}
**☉ شناسه ⧽** `{user.id}`
**☉ نام کاربری ⧽** @{user.username or "ندارد"}
**☉ تعداد اعضا ⧽** {count}

**▬▭▬▭▬▭▬▭▬▭▬▭▬▭▬**

**⎉──────▢✭ 🌟 ✭▢──────⎉**
""",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("👋 مشاهده کاربر", url=f"tg://user?id={user.id}")],
                    [InlineKeyboardButton("➕ افزودن ربات", url=f"https://t.me/{app.username}?startgroup=true")]
                ])
            )
            
            try:
                os.remove(pic)
                os.remove(welcome_photo)
            except:
                pass

    except Exception as e:
        LOGGER.error(f"Error in welcome handler: {str(e)}")

# تمیز کردن سشن‌ها موقع خاموش شدن ربات
async def cleanup():
    try:
        for session in app.session:
            await session.close()
    except:
        pass

app.on_shutdown.append(cleanup)
