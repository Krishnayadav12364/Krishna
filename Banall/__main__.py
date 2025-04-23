import asyncio
import importlib

from pyrogram import idle
from pyrogram import filters, Client
from telethon import TelegramClient

from Banall import app, bot, LOG, BOT_USERNAME
from Banall.modules import ALL_MODULES


async def anony_boot():
    try:
        # Start Pyrogram Client
        await app.start()
        # Start Telethon Client
        await bot.start(bot_token=app.bot_token)
    except Exception as ex:
        LOG.error(ex)
        quit(1)

    # Load all modules
    for all_module in ALL_MODULES:
        importlib.import_module("Banall.modules." + all_module)

    LOG.info(f"@{BOT_USERNAME} Started with Pyrogram and Telethon.")
    await idle()


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(anony_boot())
    LOG.info("Stopping Banall Bot...")
