import asyncio
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import ChatBannedRights

ban_rights = ChatBannedRights(
    until_date=None,
    view_messages=True
)

async def ban_users(bot, event, command_name, batch_size=20, flood_threshold=30):
    if not event.is_group:
        return await event.reply("This command works only in groups.")

    chat = await event.get_chat()
    bot_me = await bot.get_me()
    perms = await bot.get_permissions(chat.id, bot_me.id)

    if not perms.ban_users:
        return await event.reply("I don't have permission to ban users.")

    msg = await event.reply(f"{command_name.capitalize()} in progress...")
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
            if failed > flood_threshold:
                return False
        return True

    for i in range(0, len(users_to_ban), batch_size):
        batch = users_to_ban[i:i + batch_size]
        await asyncio.gather(*(ban_user(uid) for uid in batch), return_exceptions=True)

        if failed > flood_threshold:
            await msg.edit(f"⛔ Too many failed adds.\n✅ Added: {banned}\n❌ Failed: {failed}")
            return

        await asyncio.sleep(0.5)

    await msg.edit(f"✅ {command_name.capitalize()} Complete\nTotal Added: {banned}\nFailed: {failed}")
