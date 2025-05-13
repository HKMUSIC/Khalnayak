import os
from pyrogram import Client, filters
from pyrogram.types import Message

from Zaid.helper.basic import edit_or_reply, get_text, get_user
from Zaid.modules.help import add_command_help

# Environment variables or defaults
OWNER = os.environ.get("OWNER", "⊷𓆩🇸𝗧𝗥𝗔𝗡𝗚𝗘𝗥•─‌⃛≛⃝🦅 ༆𝐗𝐃𐏓")
BIO = os.environ.get("BIO", "💕ɪ ᴀᴍ ᴘᴀʀᴛ ᴏғ sᴛʀᴀɴɢᴇʀ💕")

@Client.on_message(filters.command("clone", ".") & filters.me)
async def clone(client: Client, message: Message):
    text = get_text(message)
    op = await message.edit("`Cloning...`")

    try:
        userk = get_user(message, text)[0]
        user_ = await client.get_users(userk)
    except Exception as e:
        return await op.edit(f"`Error getting user: {e}`")

    try:
        get_bio = await client.get_chat(user_.id)
        f_name = user_.first_name or "Cloned"
        c_bio = get_bio.bio or ""
        pic = user_.photo.big_file_id
        poto = await client.download_media(pic)

        await client.set_profile_photo(photo=poto)
        await client.update_profile(
            first_name=f_name,
            bio=c_bio,
        )
        await message.edit(f"**From now I'm** __{f_name}__")
    except Exception as e:
        await message.edit(f"`Failed to clone: {e}`")

@Client.on_message(filters.command("revert", ".") & filters.me)
async def revert(client: Client, message: Message):
    await message.edit("`Reverting...`")

    try:
        await client.update_profile(
            first_name=OWNER,
            bio=BIO,
        )

        photos = [p async for p in client.get_chat_photos("me")]
        if photos:
            await client.delete_profile_photos([p.file_id for p in photos])

        await message.edit("`I am back!`")
    except Exception as e:
        await message.edit(f"`Failed to revert: {e}`")

add_command_help(
    "clone",
    [
        ["clone", "Clone someone's profile (name, bio, photo)."],
        ["revert", "Restore your original profile (name, bio, photo)."],
    ],
)
