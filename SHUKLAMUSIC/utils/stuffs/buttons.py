from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram import Client, filters, enums 

class BUTTONS(object):
    MBUTTON = [[InlineKeyboardButton("🍡 شات جي بي تي 🍡", callback_data="mplus HELP_ChatGPT"),
                InlineKeyboardButton("▫️ المجموعات ▫️", callback_data="mplus HELP_Group"),
                InlineKeyboardButton("🦯 الملصقات 🦯", callback_data="mplus HELP_Sticker")],
               [InlineKeyboardButton("🏷️ منشن الكل 🏷️", callback_data="mplus HELP_TagAll"),
                InlineKeyboardButton("🎋 المعلومات 🎋", callback_data="mplus HELP_Info"),
                InlineKeyboardButton("🧨 إضافي 🧨", callback_data="mplus HELP_Extra")],
               [InlineKeyboardButton("🌾 الصور 🌾", callback_data="mplus HELP_Image"),
                InlineKeyboardButton("🕸️ الإجراءات 🕸️", callback_data="mplus HELP_Action"),
                InlineKeyboardButton("🔍 البحث 🔎", callback_data="mplus HELP_Search")],    
               [InlineKeyboardButton("🍭 الخطوط 🍭", callback_data="mplus HELP_Font"),
                InlineKeyboardButton("🍹 الألعاب 🍹", callback_data="mplus HELP_Game"),
                InlineKeyboardButton("🏮 تلغراف 🏮", callback_data="mplus HELP_TG")],
               [InlineKeyboardButton("🏓 المتنكر 🏓", callback_data="mplus HELP_Imposter"),
                InlineKeyboardButton("🗻 الحقيقة والجرأة 🗻", callback_data="mplus HELP_TD"),
                InlineKeyboardButton("📍 الهاشتاج 📍", callback_data="mplus HELP_HT")], 
               [InlineKeyboardButton("🛸 تحويل النص 🛸", callback_data="mplus HELP_TTS"),
                InlineKeyboardButton("🎐 المرح 🎐", callback_data="mplus HELP_Fun"),
                InlineKeyboardButton("🩹 الاقتباس 🩹", callback_data="mplus HELP_Q")],          
               [InlineKeyboardButton("<🔘", callback_data=f"settings_back_helper"), 
                InlineKeyboardButton("🔘>", callback_data=f"managebot123 settings_back_helper"),
               ]]
