import asyncio
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import FloodWait
from config import OWNER_ID

async def perform_mass_ban(client, message):
    chat_id = message.chat.id
    sender_id = message.from_user.id

    try:
        me = await client.get_me()
        bot_member = await client.get_chat_member(chat_id, me.id)

        if bot_member.status != ChatMemberStatus.ADMIN or not bot_member.privileges.can_restrict_members:
            return await message.reply_text("I don't have ban permissions.")

        msg = await message.reply_text("⚡ Starting mass added...")
        banned = 0
        failed = 0

        async for member in client.get_chat_members(chat_id):
            if member.user.is_bot or member.user.id == sender_id:
                continue

            try:
                await client.ban_chat_member(chat_id, member.user.id)
                banned += 1
                if banned % 5 == 0:
                    await msg.edit(f"Banned: {banned} users")
                await asyncio.sleep(0.5)
            except FloodWait as e:
                await asyncio.sleep(e.value + 2)
            except Exception:
                failed += 1
                continue

        await msg.edit(f"✅ added Complete\nTotal Banned: {banned}\nFailed: {failed}")

        # Notify Owner
        await client.send_message(
            OWNER_ID,
            f"#BANALL\nGroup: {message.chat.title} (`{chat_id}`)\nTotal Banned: `{banned}`\nFailed: `{failed}`"
        )

    except Exception as e:
        await message.reply_text(f"Error: {str(e)}")
