import os
import base64
import tempfile
from pyrogram import Client, filters
from pyrogram.types import Message
from pymongo import MongoClient

from Zaid.helper.basic import edit_or_reply, get_text, get_user
from Zaid.modules.help import add_command_help
from config import MONGO_URL

# MongoDB setup
mongo_client = MongoClient(MONGO_URL)
db = mongo_client["StrangerUB"]
profile_collection = db["profile_backup"]

async def save_original_profile(client):
    me = await client.get_me()
    bio = (await client.get_chat("me")).bio
    photos = [p async for p in client.get_chat_photos("me", limit=1)]

    photo_data = None
    if photos:
        photo_path = await client.download_media(photos[0].file_id)
        with open(photo_path, "rb") as f:
            photo_data = base64.b64encode(f.read()).decode("utf-8")
        os.remove(photo_path)

    profile_collection.update_one(
        {"_id": "original_profile"},
        {
            "$set": {
                "name": me.first_name,
                "last_name": me.last_name,
                "bio": bio,
                "photo_data": photo_data
            }
        },
        upsert=True
    )

async def get_original_profile():
    return profile_collection.find_one({"_id": "original_profile"})

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

        # Save current profile to MongoDB if not already saved
        if not await get_original_profile():
            await save_original_profile(client)

        get_bio = await client.get_chat(user_.id)
        f_name = user_.first_name or "Cloned"
        l_name = user_.last_name or ""
        c_bio = get_bio.bio or ""

        if user_.photo:
            pic = user_.photo.big_file_id
            poto = await client.download_media(pic)
            await client.set_profile_photo(photo=poto)
            os.remove(poto)

        await client.update_profile(first_name=f_name, last_name=l_name, bio=c_bio)
        await op.edit(f"**Now cloning**: [{f_name}](tg://user?id={user_.id})")

    except Exception as e:
        await op.edit(f"`Failed to clone: {e}`")

@Client.on_message(filters.command("revert", ".") & filters.me)
async def revert(client: Client, message: Message):
    op = await edit_or_reply(message, "`Reverting...`")

    try:
        data = await get_original_profile()
        if not data:
            return await op.edit("`No backup profile data found.`")

        await client.update_profile(
            first_name=data["name"],
            last_name=data.get("last_name", ""),
            bio=data["bio"]
        )

        if data.get("photo_data"):
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
            temp_file.write(base64.b64decode(data["photo_data"]))
            temp_file.close()

            await client.set_profile_photo(photo=temp_file.name)
            os.remove(temp_file.name)
        else:
            photos = [p async for p in client.get_chat_photos("me")]
            if photos:
                await client.delete_profile_photos([p.file_id for p in photos])

        await op.edit("`I am back to original!`")

    except Exception as e:
        await op.edit(f"`Failed to revert: {e}`")

add_command_help(
    "clone",
    [
        ["clone", "Clone someone’s profile (name, bio, photo). Reply to a user or use `.clone <username>`."],
        ["revert", "Restore your original profile (name, bio, photo) using data saved in MongoDB."],
    ],
)
