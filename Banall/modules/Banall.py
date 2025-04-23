from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from pyrogram import Client, errors
from pyrogram.errors import FloodWait
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from pyrogram import Client, errors
from pyrogram import *
from pyrogram.enums import ChatMemberStatus, ParseMode
from pyrogram.enums import ChatType
import asyncio
import os
from os import getenv
import traceback
from pyrogram import filters, Client
from pyrogram.types import Message
from unidecode import unidecode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import random 
import time
import random
import requests

from Banall import app
from Banall import SUDO, BOT_ID

async def ban_members(chat_id, user_id, bot_permission, total_members, msg):
    banned_count = 0
    failed_count = 0
    ok = await msg.reply_text(
        f"ᴛᴏᴛᴀʟ ᴍᴇᴍʙᴇʀꜱ ꜰᴏᴜɴᴅ: {total_members}\nsᴛᴀʀᴛ.."
    )
    
    while failed_count <= 30:
        async for member in app.get_chat_members(chat_id):
            if failed_count > 30:
                break  # Stop if failed bans exceed 30
            
            try:
                if member.user.id != user_id and member.user.id not in SUDO:
                    await app.ban_chat_member(chat_id, member.user.id)
                    banned_count += 1

                    if banned_count % 5 == 0:
                        try:
                            await ok.edit_text(
                                f"ʙᴀɴɴᴇᴅ {banned_count} ᴍᴇᴍʙᴇʀs ᴏᴜᴛ ᴏғ {total_members}"
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


@app.on_message(filters.command(["banall"], prefixes=[".","/","!"]) & filters.group)
async def ban_all(_, msg):
    chat_id = msg.chat.id
    LOL = await msg.reply_text("banalll")
    x = 0
    user_id = msg.from_user.id  # ID of the user who issued the command
    
    bot = await app.get_chat_member(chat_id, BOT_ID)
    bot_permission = bot.privileges.can_restrict_members
    
    if bot_permission:
        total_members = 0
        async for _ in app.get_chat_members(chat_id):
            total_members += 1
        
        await ban_members(chat_id, user_id, bot_permission, total_members, msg)
    
    else:
        await msg.reply_text(
            "ᴇɪᴛʜᴇʀ ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴇ ʀɪɢʜᴛ ᴛᴏ ʀᴇꜱᴛʀɪᴄᴛ ᴜꜱᴇʀꜱ ᴏʀ ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ɪɴ ꜱᴜᴅᴏ ᴜꜱᴇʀꜱ"
        )
