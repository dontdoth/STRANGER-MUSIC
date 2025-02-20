from pyrogram import enums
from pyrogram.enums import ChatType
from pyrogram import filters, Client
from SHUKLAMUSIC import app
from config import OWNER_ID
from pyrogram.types import Message
from SHUKLAMUSIC.utils.Shukla_ban import admin_filter
from pyrogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from datetime import datetime
import pytz


# ------------------------------------------------------------------------------- #

# اضافه کردن دستورات جدید به کد قبلی

@app.on_message(filters.command(["setusername", "username"]) & admin_filter)
async def set_username(_, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    msg = await message.reply_text("🔄 در حال پردازش...")

    if message.chat.type == enums.ChatType.PRIVATE:
        return await msg.edit("❌ این دستور فقط در گروه‌ها کار می‌کند!")

    if len(message.command) < 2:
        return await msg.edit("❌ لطفا یوزرنیم جدید را وارد کنید!\n\nمثال: `/setusername گروه_من`")

    try:
        admin_check = await app.get_chat_member(chat_id, user_id)
        if not admin_check.privileges.can_change_info:
            return await msg.edit("❌ شما دسترسی تغییر اطلاعات گروه را ندارید!")

        new_username = message.command[1].lower()
        await app.set_chat_username(chat_id, new_username)
        await msg.edit(f"""✅ یوزرنیم گروه با موفقیت تغییر کرد!

👤 تغییر توسط: {message.from_user.mention}
🆔 یوزرنیم جدید: @{new_username}""")

    except Exception as e:
        await msg.edit(f"❌ خطا: {str(e)}")

@app.on_message(filters.command(["delusername", "rmusername"]) & admin_filter)
async def delete_username(_, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    msg = await message.reply_text("🔄 در حال پردازش...")

    if message.chat.type == enums.ChatType.PRIVATE:
        return await msg.edit("❌ این دستور فقط در گروه‌ها کار می‌کند!")

    try:
        admin_check = await app.get_chat_member(chat_id, user_id)
        if not admin_check.privileges.can_change_info:
            return await msg.edit("❌ شما دسترسی تغییر اطلاعات گروه را ندارید!")

        await app.set_chat_username(chat_id, "")
        await msg.edit(f"""✅ یوزرنیم گروه با موفقیت حذف شد!

👤 حذف توسط: {message.from_user.mention}""")

    except Exception as e:
        await msg.edit(f"❌ خطا: {str(e)}")

@app.on_message(filters.command("admins"))
async def list_admins(_, message):
    chat_id = message.chat.id
    msg = await message.reply_text("🔄 در حال دریافت لیست ادمین‌ها...")

    try:
        admins = []
        async for member in app.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            admin_info = f"👤 {member.user.mention}"
            if member.title:
                admin_info += f" | 📋 {member.title}"
            admins.append(admin_info)

        admins_text = "\n".join(admins)
        await msg.edit(f"""📜 لیست ادمین‌های گروه:

{admins_text}

📊 تعداد کل: {len(admins)} ادمین""")

    except Exception as e:
        await msg.edit(f"❌ خطا: {str(e)}")

@app.on_message(filters.command(["setdescription", "setdesc", "setbio"]) & admin_filter)
async def set_description(_, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    msg = await message.reply_text("🔄 در حال پردازش...")

    if message.chat.type == enums.ChatType.PRIVATE:
        return await msg.edit("❌ این دستور فقط در گروه‌ها کار می‌کند!")

    if not message.reply_to_message and len(message.command) == 1:
        return await msg.edit("""❌ لطفا متن توضیحات را وارد کنید یا به یک پیام ریپلای کنید!

مثال:
`/setdescription این گروه برای دوستان است`
یا ریپلای روی متن + `/setdescription`""")

    try:
        admin_check = await app.get_chat_member(chat_id, user_id)
        if not admin_check.privileges.can_change_info:
            return await msg.edit("❌ شما دسترسی تغییر اطلاعات گروه را ندارید!")

        if message.reply_to_message:
            description = message.reply_to_message.text
        else:
            description = message.text.split(None, 1)[1]

        await app.set_chat_description(chat_id, description)
        await msg.edit(f"""✅ توضیحات گروه با موفقیت تغییر کرد!

👤 تغییر توسط: {message.from_user.mention}""")

    except Exception as e:
        await msg.edit(f"❌ خطا: {str(e)}")

@app.on_message(filters.command("info"))
async def chat_info(_, message):
    chat = message.chat
    msg = await message.reply_text("🔄 در حال دریافت اطلاعات...")

    try:
        chat_info = await app.get_chat(chat.id)
        members_count = await app.get_chat_members_count(chat.id)
        
        info_text = f"""📊 اطلاعات گروه:

📝 نام: {chat_info.title}
🆔 آیدی: `{chat_info.id}`
👥 تعداد اعضا: {members_count}"""

        if chat_info.username:
            info_text += f"\n🔗 یوزرنیم: @{chat_info.username}"
            
        if chat_info.description:
            info_text += f"\n📋 توضیحات: {chat_info.description}"

        if chat_info.linked_chat:
            linked = await app.get_chat(chat_info.linked_chat.id)
            info_text += f"\n🔗 گروه/کانال مرتبط: {linked.title}"

        await msg.edit(info_text)

    except Exception as e:
        await msg.edit(f"❌ خطا: {str(e)}")

@app.on_message(filters.command(["autotitle", "autoname"]) & admin_filter)
async def auto_title(_, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    msg = await message.reply_text("🔄 در حال پردازش...")

    if message.chat.type == enums.ChatType.PRIVATE:
        return await msg.edit("❌ این دستور فقط در گروه‌ها کار می‌کند!")

    try:
        # بررسی دسترسی‌های ادمین
        admin_check = await app.get_chat_member(chat_id, user_id)
        if not admin_check.privileges.can_change_info:
            return await msg.edit("❌ شما دسترسی تغییر اطلاعات گروه را ندارید!")

        # دریافت نام اصلی گروه
        group = await app.get_chat(chat_id)
        base_title = group.title
        if "|" in base_title:
            base_title = base_title.split("|")[0].strip()

        await msg.edit("✅ تایتل خودکار فعال شد!\n\nهر دقیقه ساعت کنار نام گروه بروزرسانی می‌شود.")

        while True:
            # تنظیم زمان تهران
            tehran_tz = pytz.timezone('Asia/Tehran')
            current_time = datetime.now(tehran_tz).strftime("%H:%M")
            
            # ترکیب نام گروه با ساعت
            new_title = f"{base_title} | {current_time}"
            
            try:
                await app.set_chat_title(chat_id, new_title)
            except Exception as e:
                print(f"خطا در تغییر نام گروه: {e}")
                break
                
            await asyncio.sleep(60) # انتظار 60 ثانیه

    except Exception as e:
        await msg.edit(f"❌ خطا: {str(e)}")

@app.on_message(filters.command(["stoptitle", "stopname"]) & admin_filter)
async def stop_auto_title(_, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    
    try:
        # بررسی دسترسی‌های ادمین
        admin_check = await app.get_chat_member(chat_id, user_id)
        if not admin_check.privileges.can_change_info:
            return await message.reply("❌ شما دسترسی تغییر اطلاعات گروه را ندارید!")

        # دریافت نام فعلی گروه و حذف ساعت
        group = await app.get_chat(chat_id)
        current_title = group.title
        if "|" in current_title:
            new_title = current_title.split("|")[0].strip()
            await app.set_chat_title(chat_id, new_title)
            
        await message.reply("✅ تایتل خودکار غیرفعال شد و نام گروه به حالت اصلی برگشت.")
        
    except Exception as e:
        await message.reply(f"❌ خطا: {str(e)}")
@app.on_message(filters.command("pin") & admin_filter)
async def pin(_, message):
    replied = message.reply_to_message
    chat_title = message.chat.title
    chat_id = message.chat.id
    user_id = message.from_user.id
    name = message.from_user.mention
    
    if message.chat.type == enums.ChatType.PRIVATE:
        await message.reply_text("**ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴡᴏʀᴋs ᴏɴʟʏ ᴏɴ ɢʀᴏᴜᴘs !**")
    elif not replied:
        await message.reply_text("**ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ᴘɪɴ ɪᴛ !**")
    else:
        user_stats = await app.get_chat_member(chat_id, user_id)
        if user_stats.privileges.can_pin_messages and message.reply_to_message:
            try:
                await message.reply_to_message.pin()
                await message.reply_text(f"**sᴜᴄᴄᴇssғᴜʟʟʏ ᴘɪɴɴᴇᴅ ᴍᴇssᴀɢᴇ!**\n\n**ᴄʜᴀᴛ:** {chat_title}\n**ᴀᴅᴍɪɴ:** {name}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(" 📝 ᴠɪᴇᴡs ᴍᴇssᴀɢᴇ ", url=replied.link)]]))
            except Exception as e:
                await message.reply_text(str(e))


@app.on_message(filters.command("pinned"))
async def pinned(_, message):
    chat = await app.get_chat(message.chat.id)
    if not chat.pinned_message:
        return await message.reply_text("**ɴᴏ ᴘɪɴɴᴇᴅ ᴍᴇssᴀɢᴇ ғᴏᴜɴᴅ**")
    try:        
        await message.reply_text("ʜᴇʀᴇ ɪs ᴛʜᴇ ʟᴀᴛᴇsᴛ ᴘɪɴɴᴇᴅ ᴍᴇssᴀɢᴇ",reply_markup=
        InlineKeyboardMarkup([[InlineKeyboardButton(text="📝 ᴠɪᴇᴡ ᴍᴇssᴀɢᴇ",url=chat.pinned_message.link)]]))  
    except Exception as er:
        await message.reply_text(er)


# ------------------------------------------------------------------------------- #

@app.on_message(filters.command("unpin") & admin_filter)
async def unpin(_, message):
    replied = message.reply_to_message
    chat_title = message.chat.title
    chat_id = message.chat.id
    user_id = message.from_user.id
    name = message.from_user.mention
    
    if message.chat.type == enums.ChatType.PRIVATE:
        await message.reply_text("**ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴡᴏʀᴋs ᴏɴʟʏ ᴏɴ ɢʀᴏᴜᴘs !**")
    elif not replied:
        await message.reply_text("**ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴛᴏ ᴜɴᴘɪɴ ɪᴛ !**")
    else:
        user_stats = await app.get_chat_member(chat_id, user_id)
        if user_stats.privileges.can_pin_messages and message.reply_to_message:
            try:
                await message.reply_to_message.unpin()
                await message.reply_text(f"**sᴜᴄᴄᴇssғᴜʟʟʏ ᴜɴᴘɪɴɴᴇᴅ ᴍᴇssᴀɢᴇ!**\n\n**ᴄʜᴀᴛ:** {chat_title}\n**ᴀᴅᴍɪɴ:** {name}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(" 📝 ᴠɪᴇᴡs ᴍᴇssᴀɢᴇ ", url=replied.link)]]))
            except Exception as e:
                await message.reply_text(str(e))




# --------------------------------------------------------------------------------- #

@app.on_message(filters.command("removephoto") & admin_filter)
async def deletechatphoto(_, message):
      
      chat_id = message.chat.id
      user_id = message.from_user.id
      msg = await message.reply_text("**ᴘʀᴏᴄᴇssɪɴɢ....**")
      admin_check = await app.get_chat_member(chat_id, user_id)
      if message.chat.type == enums.ChatType.PRIVATE:
           await msg.edit("**ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴡᴏʀᴋ ᴏɴ ɢʀᴏᴜᴘs !**") 
      try:
         if admin_check.privileges.can_change_info:
             await app.delete_chat_photo(chat_id)
             await msg.edit("**sᴜᴄᴄᴇssғᴜʟʟʏ ʀᴇᴍᴏᴠᴇᴅ ᴘʀᴏғɪʟᴇ ᴘʜᴏᴛᴏ ғʀᴏᴍ ɢʀᴏᴜᴘ !\nʙʏ** {}".format(message.from_user.mention))    
      except:
          await msg.edit("**ᴛʜᴇ ᴜsᴇʀ ᴍᴏsᴛ ɴᴇᴇᴅ ᴄʜᴀɴɢᴇ ɪɴғᴏ ᴀᴅᴍɪɴ ʀɪɢʜᴛs ᴛᴏ ʀᴇᴍᴏᴠᴇ ɢʀᴏᴜᴘ ᴘʜᴏᴛᴏ !**")


# --------------------------------------------------------------------------------- #

@app.on_message(filters.command("setphoto")& admin_filter)
async def setchatphoto(_, message):
      reply = message.reply_to_message
      chat_id = message.chat.id
      user_id = message.from_user.id
      msg = await message.reply_text("ᴘʀᴏᴄᴇssɪɴɢ...")
      admin_check = await app.get_chat_member(chat_id, user_id)
      if message.chat.type == enums.ChatType.PRIVATE:
           await msg.edit("`ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴡᴏʀᴋ ᴏɴ ɢʀᴏᴜᴘs !`") 
      elif not reply:
           await msg.edit("**ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴘʜᴏᴛᴏ ᴏʀ ᴅᴏᴄᴜᴍᴇɴᴛ.**")
      elif reply:
          try:
             if admin_check.privileges.can_change_info:
                photo = await reply.download()
                await message.chat.set_photo(photo=photo)
                await msg.edit_text("**sᴜᴄᴄᴇssғᴜʟʟʏ ɴᴇᴡ ᴘʀᴏғɪʟᴇ ᴘʜᴏᴛᴏ ɪɴsᴇʀᴛ !\nʙʏ** {}".format(message.from_user.mention))
             else:
                await msg.edit("**sᴏᴍᴇᴛʜɪɴɢ ᴡʀᴏɴɢ ʜᴀᴘᴘᴇɴᴇᴅ ᴛʀʏ ᴀɴᴏᴛʜᴇʀ ᴘʜᴏᴛᴏ !**")
     
          except:
              await msg.edit("**ᴛʜᴇ ᴜsᴇʀ ᴍᴏsᴛ ɴᴇᴇᴅ ᴄʜᴀɴɢᴇ ɪɴғᴏ ᴀᴅᴍɪɴ ʀɪɢʜᴛs ᴛᴏ ᴄʜᴀɴɢᴇ ɢʀᴏᴜᴘ ᴘʜᴏᴛᴏ !**")


# --------------------------------------------------------------------------------- #

@app.on_message(filters.command("settitle")& admin_filter)
async def setgrouptitle(_, message):
    reply = message.reply_to_message
    chat_id = message.chat.id
    user_id = message.from_user.id
    msg = await message.reply_text("ᴘʀᴏᴄᴇssɪɴɢ...")
    if message.chat.type == enums.ChatType.PRIVATE:
          await msg.edit("**ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴡᴏʀᴋ ᴏɴ ɢʀᴏᴜᴘs !**")
    elif reply:
          try:
            title = message.reply_to_message.text
            admin_check = await app.get_chat_member(chat_id, user_id)
            if admin_check.privileges.can_change_info:
               await message.chat.set_title(title)
               await msg.edit("**sᴜᴄᴄᴇssғᴜʟʟʏ ɴᴇᴡ ɢʀᴏᴜᴘ ɴᴀᴍᴇ ɪɴsᴇʀᴛ !\nʙʏ** {}".format(message.from_user.mention))
          except AttributeError:
                await msg.edit("**ᴛʜᴇ ᴜsᴇʀ ᴍᴏsᴛ ɴᴇᴇᴅ ᴄʜᴀɴɢᴇ ɪɴғᴏ ᴀᴅᴍɪɴ ʀɪɢʜᴛs ᴛᴏ ᴄʜᴀɴɢᴇ ɢʀᴏᴜᴘ ᴛɪᴛʟᴇ !**")   
    elif len(message.command) >1:
        try:
            title = message.text.split(None, 1)[1]
            admin_check = await app.get_chat_member(chat_id, user_id)
            if admin_check.privileges.can_change_info:
               await message.chat.set_title(title)
               await msg.edit("**sᴜᴄᴄᴇssғᴜʟʟʏ ɴᴇᴡ ɢʀᴏᴜᴘ ɴᴀᴍᴇ ɪɴsᴇʀᴛ !\nʙʏ** {}".format(message.from_user.mention))
        except AttributeError:
               await msg.edit("**ᴛʜᴇ ᴜsᴇʀ ᴍᴏsᴛ ɴᴇᴇᴅ ᴄʜᴀɴɢᴇ ɪɴғᴏ ᴀᴅᴍɪɴ ʀɪɢʜᴛs ᴛᴏ ᴄʜᴀɴɢᴇ ɢʀᴏᴜᴘ ᴛɪᴛʟᴇ !**")
          

    else:
       await msg.edit("**ʏᴏᴜ ɴᴇᴇᴅ ʀᴇᴘʟʏ ᴛᴏ ᴛᴇxᴛ ᴏʀ ɢɪᴠᴇ sᴏᴍᴇ ᴛᴇxᴛ ᴛᴏ ᴄʜᴀɴɢᴇ ɢʀᴏᴜᴘ ᴛɪᴛʟᴇ **")


# --------------------------------------------------------------------------------- #



@app.on_message(filters.command("setdiscription") & admin_filter)
async def setg_discription(_, message):
    reply = message.reply_to_message
    chat_id = message.chat.id
    user_id = message.from_user.id
    msg = await message.reply_text("**ᴘʀᴏᴄᴇssɪɴɢ...**")
    if message.chat.type == enums.ChatType.PRIVATE:
        await msg.edit("**ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴡᴏʀᴋs ᴏɴ ɢʀᴏᴜᴘs!**")
    elif reply:
        try:
            discription = message.reply_to_message.text
            admin_check = await app.get_chat_member(chat_id, user_id)
            if admin_check.privileges.can_change_info:
                await message.chat.set_description(discription)
                await msg.edit("**sᴜᴄᴄᴇssғᴜʟʟʏ ɴᴇᴡ ɢʀᴏᴜᴘ ᴅɪsᴄʀɪᴘᴛɪᴏɴ ɪɴsᴇʀᴛ!**\nʙʏ {}".format(message.from_user.mention))
        except AttributeError:
            await msg.edit("**ᴛʜᴇ ᴜsᴇʀ ᴍᴜsᴛ ʜᴀᴠᴇ ᴄʜᴀɴɢᴇ ɪɴғᴏ ᴀᴅᴍɪɴ ʀɪɢʜᴛs ᴛᴏ ᴄʜᴀɴɢᴇ ɢʀᴏᴜᴘ ᴅɪsᴄʀɪᴘᴛɪᴏɴ!**")   
    elif len(message.command) > 1:
        try:
            discription = message.text.split(None, 1)[1]
            admin_check = await app.get_chat_member(chat_id, user_id)
            if admin_check.privileges.can_change_info:
                await message.chat.set_description(discription)
                await msg.edit("**sᴜᴄᴄᴇssғᴜʟʟʏ ɴᴇᴡ ɢʀᴏᴜᴘ ᴅɪsᴄʀɪᴘᴛɪᴏɴ ɪɴsᴇʀᴛ!**\nʙʏ {}".format(message.from_user.mention))
        except AttributeError:
            await msg.edit("**ᴛʜᴇ ᴜsᴇʀ ᴍᴜsᴛ ʜᴀᴠᴇ ᴄʜᴀɴɢᴇ ɪɴғᴏ ᴀᴅᴍɪɴ ʀɪɢʜᴛs ᴛᴏ ᴄʜᴀɴɢᴇ ɢʀᴏᴜᴘ ᴅɪsᴄʀɪᴘᴛɪᴏɴ!**")
    else:
        await msg.edit("**ʏᴏᴜ ɴᴇᴇᴅ ᴛᴏ ʀᴇᴘʟʏ ᴛᴏ ᴛᴇxᴛ ᴏʀ ɢɪᴠᴇ sᴏᴍᴇ ᴛᴇxᴛ ᴛᴏ ᴄʜᴀɴɢᴇ ɢʀᴏᴜᴘ ᴅɪsᴄʀɪᴘᴛᴏɴ!**")


# --------------------------------------------------------------------------------- #

@app.on_message(filters.command("lg")& filters.user(OWNER_ID))
async def bot_leave(_, message):
    chat_id = message.chat.id
    text = "**sᴜᴄᴄᴇssғᴜʟʟʏ ʜɪʀᴏ !!.**"
    await message.reply_text(text)
    await app.leave_chat(chat_id=chat_id, delete=True)


# --------------------------------------------------------------------------------- #


