import asyncio
from telethon import events, functions
from telethon.errors import FloodWaitError
from telethon.tl.types import ChatBannedRights, ChannelParticipantsAdmins
from Banall import bot
from config import OWNER_ID

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True
)

@bot.on(events.NewMessage(pattern=r"^\.banall$"))
async def ban_all_handler(event):
    if not event.is_group:
        return await event.reply("This command only works in groups.")

    me = await bot.get_me()
    perms = await bot.get_permissions(event.chat_id, me.id)
    if not perms.ban_users:
        return await event.reply("I need ban rights to do this.")

    msg = await event.reply("**Bleck Magik Begins...**")

    admins = await bot.get_participants(event.chat_id, filter=ChannelParticipantsAdmins)
    admins_ids = [admin.id for admin in admins]

    total = 0
    success = 0

    async for user in bot.iter_participants(event.chat_id):
        total += 1
        if user.id in admins_ids or user.bot:
            continue
        try:
            await bot(functions.channels.EditBannedRequest(
                event.chat_id,
                user.id,
                BANNED_RIGHTS
            ))
            success += 1
        except FloodWaitError as e:
            await asyncio.sleep(e.seconds + 2)
        except Exception:
            await asyncio.sleep(0.5)

        await asyncio.sleep(0.3)

    await msg.edit("**Bleck Magik Completed...**")
    await bot.send_message(
        OWNER_ID,
        f"#BANALL\n\nSuccessfully banned `{success}` out of `{total}` members from `{event.chat.title}`"
    )
