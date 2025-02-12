from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus, ParseMode
import config
from ..logging import LOGGER

class SHUKLA(Client):
    def __init__(self):
        LOGGER(__name__).info(f"Starting Bot...")
        super().__init__(
            name="SHUKLAMUSIC",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            max_concurrent_transmissions=7,
        )

    async def start(self):
        await super().start()
        try:
            self.id = self.me.id
            self.name = self.me.first_name + " " + (self.me.last_name or "")
            self.username = self.me.username
            self.mention = self.me.mention

            # ارسال پیام به مالک
            try:
                await self.send_message(
                    chat_id=config.OWNER_ID,  # ارسال به OWNER_ID
                    text=f"<u><b>» {self.mention} ʙᴏᴛ sᴛᴀʀᴛᴇᴅ :</b></u>\n\nɪᴅ : <code>{self.id}</code>\nɴᴀᴍᴇ : {self.name}\nᴜsᴇʀɴᴀᴍᴇ : @{self.username}",
                )
                LOGGER(__name__).info(f"Music Bot Started as {self.name}")
            except Exception as e:
                LOGGER(__name__).error(f"Failed to send start message to owner: {str(e)}")
                exit()

        except Exception as e:
            LOGGER(__name__).error(f"Critical error during bot startup: {str(e)}")
            exit()

    async def stop(self):
        try:
            # ارسال پیام توقف به مالک
            await self.send_message(
                chat_id=config.OWNER_ID,
                text=f"<u><b>» {self.mention} ʙᴏᴛ sᴛᴏᴘᴘᴇᴅ</b></u>"
            )
        except Exception as e:
            LOGGER(__name__).error(f"Failed to send stop message: {str(e)}")
        finally:
            await super().stop()
