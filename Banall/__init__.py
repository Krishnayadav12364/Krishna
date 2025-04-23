import os
import logging
from pyrogram import Client
from telethon import TelegramClient
from config import Config

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

LOG = logging.getLogger(__name__)

ENV = bool(os.environ.get("ENV", False))

if ENV:
    API_ID = int(os.environ.get("API_ID", ""))
    API_HASH = str(os.environ.get("API_HASH", ""))
    TOKEN = str(os.environ.get("TOKEN", ""))
    SUDO = list(int(i) for i in os.environ.get("SUDO", "443809517").split(" "))
    BOT_ID = int(os.environ.get("BOT_ID", ""))
    BOT_USERNAME = str(os.environ.get("BOT_USERNAME", ""))
    OWNER_ID = int(getenv("OWNER_ID", "443809517"))  # ʏᴏᴜʀ ᴏᴡɴᴇʀ ɪᴅ
else:
    API_ID = Config.API_ID
    API_HASH = Config.API_HASH
    TOKEN = Config.TOKEN
    SUDO = Config.SUDO
    BOT_ID = Config.BOT_ID
    BOT_USERNAME = Config.BOT_USERNAME
    BOT_NAME = Config.BOT_NAME
    OWNER_ID =Config.OWNER_ID

# Initialize Pyrogram Client
app = Client(
    "BOT",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=TOKEN,
    plugins=dict(root="Banall.modules")
)

# Initialize Telethon Client
bot = TelegramClient(
    "TelethonBOT",
    api_id=API_ID,
    api_hash=API_HASH
)

async def start(self):
    await super().start()
    self.id = self.me.id
    self.name = self.me.first_name + " " + (self.me.last_name or "")
    self.username = self.me.username
    self.mention = self.me.mention

async def stop(self):
    await super().stop()

LOG.info("Starting the bots...")
