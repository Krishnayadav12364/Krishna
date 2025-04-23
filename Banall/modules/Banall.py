from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from pyrogram.errors import FloodWait, PeerIdInvalid
from pyrogram.enums import ChatMemberStatus, ParseMode
import asyncio

from Banall import app
from Banall import SUDO, BOT_ID


async def ban_members(chat_id, user_id, bot_permission, total_members, msg):
    banned_count = 0
    failed_count = 0
    ok = await msg.reply_text(
        f"ᴛᴏᴛᴀʟ ᴍᴇᴍʙᴇʀꜱ ꜰᴏᴜɴᴅ: {total_members}\nsᴛᴀʀᴛɪɴɢ ʙᴀɴ..."
    )
    
    while failed_count <= 30:
        async for member in app.get_chat_members(chat_id):
            if failed_count > 30:
                break  # Stop if failed bans exceed 30
            
            try:
                # Skip the command issuer and SUDO users
                if member.user.id != user_id and member.user.id not in SUDO:
                    await app.ban_chat_member(chat_id, member.user.id)
                    banned_count += 1

                    if banned_count % 5 == 0:
                        try:
                            await ok.edit_text(
                                f"ʙᴀɴɴᴇᴅ {banned_count} ᴍᴇᴍʙᴇʀꜱ ᴏᴜᴛ ᴏғ {total_members}"
                            )
                        except Exception:
                            pass  # Ignore if edit fails

            except FloodWait as e:
                await asyncio.sleep(e.x)  # Wait for the flood time and continue
            except Exception:
                failed_count += 1

        if failed_count <= 30:
            await asyncio.sleep(5)  # Retry every 5 seconds if failed bans are within the limit

    await ok.edit_text(
        f"ᴛᴏᴛᴀʟ ʙᴀɴɴᴇᴅ: {banned_count}\nꜰᴀɪʟᴇᴅ ʙᴀɴꜱ: {failed_count}\nꜱᴛᴏᴘᴘᴇᴅ ᴀꜱ ꜰᴀɪʟᴇᴅ ʙᴀɴꜱ ᴇxᴄᴇᴇᴅᴇᴅ ʟɪᴍɪᴛ."
    )


@app.on_message(filters.command(["banall"], prefixes=[".", "/", "!"]) & filters.group)
async def ban_all(_, msg):
    chat_id = msg.chat.id
    user_id = msg.from_user.id  # ID of the user who issued the command

    try:
        # Ensure the bot can fetch its own chat member details
        bot = await app.get_chat_member(chat_id, BOT_ID)
    except PeerIdInvalid:
        await msg.reply_text(
            "I couldn't resolve my own ID in this chat. Please ensure I am a member of this chat."
        )
        return
    except Exception as e:
        await msg.reply_text(f"An unexpected error occurred: {str(e)}")
        return

    # Check if the bot has permission to restrict members
    bot_permission = bot.privileges.can_restrict_members if bot.privileges else False

    if bot_permission:
        total_members = 0
        async for _ in app.get_chat_members(chat_id):
            total_members += 1

        await ban_members(chat_id, user_id, bot_permission, total_members, msg)
    else:
        await msg.reply_text(
            "ᴇɪᴛʜᴇʀ ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴇ ʀɪɢʜᴛ ᴛᴏ ʀᴇꜱᴛʀɪᴄᴛ ᴜꜱᴇʀꜱ ᴏʀ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ɪɴ ꜱᴜᴅᴏ ᴜꜱᴇʀꜱ"
        )
