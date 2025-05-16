import os
from pyrogram import Client, filters
from pyrogram.types import Message

from Zaid.helper.basic import edit_or_reply, get_text, get_user
from Zaid.modules.help import add_command_help

# Store your original name and bio
OWNER = os.environ.get("OWNER", "Your Name")
BIO = os.environ.get("BIO", "💕ɪ ᴀᴍ ᴘᴀʀᴛ ᴏғ sᴛʀᴀɴɢᴇʀ💕")

# Save original profile picture (once)
ORIGINAL_DP = None

@Client.on_message(filters.command("clone", ".") & filters.me)
async def clone(client: Client, message: Message):
    op = await edit_or_reply(message, "`Cloning...`")

    try:
        if message.reply_to_message:
            user_ = message.reply_to_message.from_user
        else:
            text = get_text(message)
            user_id = get_user(message, text)[0]
            user_ = await client.get_users(user_id)

        get_bio = await client.get_chat(user_.id)
        f_name = user_.first_name or "Cloned"
        c_bio = get_bio.bio or ""

        # Get profile photo
        if user_.photo:
            pic = user_.photo.big_file_id
            poto = await client.download_media(pic)

            # Save original photo if not saved
            global ORIGINAL_DP
            if ORIGINAL_DP is None:
                photos = [p async for p in client.get_chat_photos("me", limit=1)]
                if photos:
                    ORIGINAL_DP = photos[0].file_id

            await client.set_profile_photo(photo=poto)

        await client.update_profile(first_name=f_name, bio=c_bio)
        await op.edit(f"**Now cloning**: [{f_name}](tg://user?id={user_.id})")

    except Exception as e:
        await op.edit(f"`Failed to clone: {e}`")

@Client.on_message(filters.command("revert", ".") & filters.me)
async def revert(client: Client, message: Message):
    op = await edit_or_reply(message, "`Reverting...`")

    try:
        await client.update_profile(first_name=OWNER, bio=BIO)

        # Restore profile photo if backup exists
        global ORIGINAL_DP
        if ORIGINAL_DP:
            await client.set_profile_photo(photo=ORIGINAL_DP)
        else:
            # If no backup, remove all
            photos = [p async for p in client.get_chat_photos("me")]
            if photos:
                await client.delete_profile_photos([p.file_id for p in photos])

        await op.edit("`I am back to original!`")

    except Exception as e:
        await op.edit(f"`Failed to revert: {e}`")

add_command_help(
    "clone",
    [
        ["clone", "Reply to a user or use `.clone <username>` to copy their name, bio, and profile picture."],
        ["revert", "Restore your original name, bio, and profile photo."],
    ],
)
