from pyrogram.types import Message
import asyncio

async def perform_mass_ban(client, message: Message):
    chat_id = message.chat.id    
    reply_message = await message.reply_text("Processing bans...")
    app = await client.get_me()
    bot_id = app.id
    banned_count = 0

    # Check bot permissions
    bot_status = await client.get_chat_member(chat_id, bot_id)
    if bot_status.privileges and bot_status.privileges.can_restrict_members:
        # Iterate through chat members and ban them
        async for member in client.get_chat_members(chat_id):
            try:
                await client.ban_chat_member(chat_id, member.user.id)
                banned_count += 1
                await reply_message.edit_text(f"✫ Users banned: {banned_count} ✫")
                # Add a delay to avoid hitting API limits
                await asyncio.sleep(0.5)
            except Exception as e:
                print(f"Failed to ban user {member.user.id}: {e}")
    else:
        await message.reply_text("I don't have the right to restrict users.")
