from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram import Client, filters, enums 

class BUTTONS(object):
    MBUTTON = [[InlineKeyboardButton("⚡ چت جی‌پی‌تی ⚡", callback_data="mplus HELP_ChatGPT"),
                InlineKeyboardButton("👥 گروه‌ها 👥", callback_data="mplus HELP_Group"),
                InlineKeyboardButton("💫 استیکرها 💫", callback_data="mplus HELP_Sticker")],
               
               [InlineKeyboardButton("📢 تگ همگانی 📢", callback_data="mplus HELP_TagAll"),
                InlineKeyboardButton("ℹ️ اطلاعات ℹ️", callback_data="mplus HELP_Info"),
                InlineKeyboardButton("⚙️ امکانات اضافه ⚙️", callback_data="mplus HELP_Extra")],
               
               [InlineKeyboardButton("🖼️ تصاویر 🖼️", callback_data="mplus HELP_Image"),
                InlineKeyboardButton("⚔️ اقدامات ⚔️", callback_data="mplus HELP_Action"),
                InlineKeyboardButton("🔍 جستجو 🔎", callback_data="mplus HELP_Search")],
               
               [InlineKeyboardButton("💎 فونت 💎", callback_data="mplus HELP_Font"),
                InlineKeyboardButton("🎮 بازی‌ها 🎮", callback_data="mplus HELP_Game"),
                InlineKeyboardButton("📝 تلگراف 📝", callback_data="mplus HELP_TG")],
               
               [InlineKeyboardButton("👁️ ناظر 👁️", callback_data="mplus HELP_Imposter"),
                InlineKeyboardButton("🎲 جرأت یا حقیقت 🎲", callback_data="mplus HELP_TD"),
                InlineKeyboardButton("#️⃣ هشتگ #️⃣", callback_data="mplus HELP_HT")],
               
               [InlineKeyboardButton("🔊 متن به گفتار 🔊", callback_data="mplus HELP_TTS"),
                InlineKeyboardButton("🎯 سرگرمی 🎯", callback_data="mplus HELP_Fun"),
                InlineKeyboardButton("💬 نقل قول 💬", callback_data="mplus HELP_Q")],
               
               [InlineKeyboardButton("⬅️", callback_data=f"settings_back_helper"),
                InlineKeyboardButton("➡️", callback_data=f"managebot123 settings_back_helper"),
               ]]
