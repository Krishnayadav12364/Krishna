import asyncio
from telethon import events
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights
from Banall import bot

ban_rights = ChatBannedRights(
    until_date=None,
    view_messages=True
)

BATCH_SIZE = 20            # Users per batch
FLOOD_THRESHOLD = 30       # Max fail count before abort

@bot.on(events.NewMessage(pattern=r"^.(bad|Bad)$"))
async def banall_handler(event):
    if not event.is_group:
        return await event.reply("This command works only in groups.")

    chat = await event.get_chat()
    perms = await bot.get_permissions(chat.id, bot.me.id)

    if not perms.ban_users:
        return await event.reply("I don't have permission to ban users.")

    msg = await event.reply("Banall...")
    banned, failed = 0, 0
    users_to_ban = []

    async for user in bot.iter_participants(chat.id):
        if user.bot or user.id == event.sender_id:
            continue
        users_to_ban.append(user.id)

    async def ban_user(uid):
        nonlocal banned, failed
        try:
            await bot(EditBannedRequest(chat.id, uid, ban_rights))
            banned += 1
        except Exception as e:
            failed += 1
            if "Flood" in str(e):
                secs = int(str(e).split("A wait of ")[-1].split(" ")[0])
                await asyncio.sleep(secs + 5)
            if failed > FLOOD_THRESHOLD:
                return False
        return True

    for i in range(0, len(users_to_ban), BATCH_SIZE):
        batch = users_to_ban[i:i + BATCH_SIZE]
        results = await asyncio.gather(*(ban_user(uid) for uid in batch), return_exceptions=True)

        if failed > FLOOD_THRESHOLD:
            await msg.edit(f"⛔ Too many failed bans.\n✅ Banned: {banned}\n❌ Failed: {failed}")
            return

        await asyncio.sleep(0.5)  # slight delay between batches

    await msg.edit(f"✅ Banall Complete\nTotal Banned: {banned}\nFailed: {failed}")
