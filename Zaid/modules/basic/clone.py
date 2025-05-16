import os, sys, io, random
from pyrogram import Client, filters
from pyrogram.types import Message
from Zaid.helper.basic import edit_or_reply, get_text, get_user
from Zaid.modules.help import add_command_help

FName = ""
LName = ""
Bio = ""

@Client.on_message(filters.command("clone", ".") & filters.me)
async def clone_user(Shashank: Client, message: Message):
    global FName 
    global LName
    global Bio
    try:
       user = await user_only(Shashank, message)
       if not user:
          return 
    except Exception as er:
       await message.reply(user_errors(er))
       return
    Mai = await Shashank.get_me()
    FName = Mai.first_name
    if Mai.last_name:
       LName = Mai.last_name
    siu = await Shashank.get_chat("me")
    if siu.bio:
       Bio = siu.bio
    Reply = await message.reply("cloning...")
    _bio = await Shashank.get_chat(user.id)
    if _bio.bio:
       user_bio = _bio.bio
    else:
       user_bio = None
    pic = await Shashank.download_media(user.photo.big_file_id)
    try:
       await Shashank.set_profile_photo(photo=pic)
       if user.last_name:
          await Shashank.update_profile(first_name=user.first_name, last_name=user.last_name, bio=user_bio)
       else:
          await Shashank.update_profile(first_name=user.first_name, bio=user_bio)
       await delete_reply(message, Reply, f"Now I'm {user.first_name} \n\n Note: Don't restart until you revert me!")
    except Exception as eror:
       await delete_reply(message, Reply, str(eror))

@Client.on_message(filters.command("revert", ".") & filters.me)
async def _revert(Shashank: Client, message: Message):
    global FName 
    global LName
    global Bio
    Mai = await Shashank.get_me()
    photos = [x async for x in Shashank.get_chat_photos("me")]
    if not FName:
       await message.reply(f"Error: You didn't cloned anyone!")
       return
    user_bio = Bio
    if not user_bio:
       user_bio = "💕ɪ ᴀᴍ ᴘᴀʀᴛ ᴏғ sᴛʀᴀɴɢᴇʀ💕"
    Reply = await message.reply("reverting...")
    try:
       if LName:
          await Shashank.update_profile(first_name=FName, last_name=LName, bio=user_bio)
       else:
          await Shashank.update_profile(first_name=FName, bio=user_bio)
       await Shashank.delete_profile_photos(photos[0].file_id)
       await delete_reply(message, Reply, f"I'm Back!")
       FName = ""
       LName = ""
       Bio = ""
    except Exception as eror:
       await delete_reply(message, Reply, str(eror))


add_command_help(
    "clone",
    [
        ["clone", "Clone someone’s profile (name, bio, photo). Reply to a user or use `.clone <username>`."],
        ["revert", "Restore your original profile (name, bio, photo) using data saved in MongoDB."],
    ],
)
