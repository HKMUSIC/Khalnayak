from Zaid import app, API_ID, API_HASH
from config import OWNER_ID, ALIVE_PIC, MONGO_URL
from pyrogram import Client, filters
from pyrogram.errors import SessionPasswordNeeded
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient
import asyncio

user_sessions = {}

mongo_client = MongoClient(MONGO_URL)
db = mongo_client["SessionDB"]
sessions_col = db["UserSessions"]

PHONE_NUMBER_TEXT = (
    "**╭────── ˹ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ˼ ⏤͟͟͞͞★**\n"
    "**┆◍ ʜᴇʏ, ɪ ᴀᴍ : [\u1d5eᴛʀᴀɴɢᴇʀ ꭙ \ud835\udd0asᴇꝛвσᴛ](https://t.me/StrangerUBbot) **\n"
    "**┆● Sᴛʀᴀɴɢᴇʀ Bᴏᴛ Vᴇʀsɪᴏɴ :** `2.1.3`\n"
    "**┊● Pᴏᴡᴇʀғᴜʟ & Usᴇғᴜʟ Usᴇʀʙᴏᴛ**\n"
    "**╰─────────────────────────**\n"
    "**──────────────────────────**\n"
    "**❖ Hᴏᴡ Tᴏ Usᴇ Tʜɪs Bᴏᴛ - [Cʟɪᴄᴋ Hᴇʀᴇ](https://t.me/StrangerAssociation/539) **\n"
    "**──────────────────────────**\n"
    "**❖ Sᴇssɪᴏɴs Gᴇɴ Bᴏᴛ ⁚ [Sᴇssɪᴏɴ-Bᴏᴛ](https://t.me/StringSesssionGeneratorRobot) **\n"
    "**──────────────────────────**\n"
    "**❖ Cʟᴏɴᴇ Bᴏᴛ  ⁚ /clone [ Sᴛʀɪɴɢ Sᴇssɪᴏɴ ]**\n"
    "**❖ Hᴏsᴛ Bᴏᴛ : /add [ᴠɪᴀ ᴘʜᴏɴᴇ ɴᴏ. & ᴏᴛᴘ]**\n"
    "**──────────────────────────**\n"
    "**❖ Uᴘᴅᴀᴛᴇ ⏤͟͟͞͞  [❖ ∣ Tʜᴇ sᴛʀᴀɴɢᴇʀ ∣ ❖](https://t.me/SHIVANSH474) **\n"
    "**──────────────────────────**"
)

@app.on_message(filters.command("start"))
async def hello(client: app, message):
    buttons = [
        [InlineKeyboardButton(text="sᴇssɪᴏɴ ɢᴇɴ ʙᴏᴛ", url="https://t.me/StringSesssionGeneratorRobot")],
        [InlineKeyboardButton(text="ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴛʜɪs ʙᴏᴛ", url="https://t.me/StrangerAssociation/539")],
        [
            InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url="https://t.me/MASTIWITHFRIENDSXD"),
            InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇ", url="https://t.me/StrangerAssociation")
        ],
        [InlineKeyboardButton("sʜɪᴠàɴsʜ-xᴅ", url="https://t.me/ITSZ_SHIVANSH")],
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await client.send_photo(message.chat.id, ALIVE_PIC, caption=PHONE_NUMBER_TEXT, reply_markup=reply_markup)

@app.on_message(filters.command("clone"))
async def clone(bot: app, msg: Message):
    try:
        phone = msg.command[1]
        await msg.reply("❖ ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ᴀ ᴍɪɴᴜᴛᴇ")
        client = Client(name="Melody", api_id=API_ID, api_hash=API_HASH, session_string=phone, plugins=dict(root="Zaid/modules"))
        await client.start()
        user = await client.get_me()
        await msg.reply(f"❖ ɴᴏᴡ ʏᴏᴜ ᴀʀᴇ ʀᴇᴀᴅʏ ᴛᴏ ғɪɢʜᴛ\n\n❍ [❖ │ sᴛʀᴀɴɢᴇʀ ꭙ ʙᴏᴛ │ ❖](https://t.me/SHIVANSH474)\n\n❖ {user.first_name}")
    except Exception as e:
        await msg.reply(f"**ERROR:** `{str(e)}`\nPress /start to Start again.")

@app.on_message(filters.command("add"))
async def start_generate(_, msg: Message):
    await msg.reply("📲 ᴘʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ ɪɴ ɪɴᴛᴇʀɴᴀᴛɪᴏɴᴀʟ ғᴏʀᴍᴀᴛ (e.g., +11234567890):")
    user_sessions[msg.from_user.id] = {"step": "awaiting_phone"}

@app.on_message(filters.command("remove"))
async def remove_session(_, msg: Message):
    uid = msg.from_user.id
    session_data = sessions_col.find_one({"_id": uid})

    if not session_data:
        return await msg.reply("❌ ɴᴏ ᴀᴄᴛɪᴠᴇ sᴇssɪᴏɴ ғᴏᴜɴᴅ.")

    try:
        temp_client = Client(
            name=f"TempRemove_{uid}",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=session_data["session"]
        )
        await temp_client.start()
        await temp_client.stop()
    except Exception as e:
        await msg.reply(f"⚠️ Fᴀɪʟᴇᴅ ᴛᴏ sᴛᴏᴘ sᴇssɪᴏɴ:\n`{e}`")

    sessions_col.delete_one({"_id": uid})
    await msg.reply("✅ ʏᴏᴜʀ sᴇssɪᴏɴ ʜᴀs ʙᴇᴇɴ ʀᴇᴍᴏᴠᴇᴅ.")

@app.on_message()
async def session_flow(_, msg: Message):
    uid = msg.from_user.id
    if uid not in user_sessions:
        return

    session = user_sessions[uid]
    step = session.get("step")

    if step == "awaiting_phone":
        phone = msg.text.strip()
        client = Client(name=f"gen_session_{uid}", api_id=API_ID, api_hash=API_HASH, in_memory=True)
        session.update({"phone": phone, "client": client})

        try:
            await client.connect()
            sent = await client.send_code(phone)
            session["phone_code_hash"] = sent.phone_code_hash
            session["step"] = "awaiting_otp"
            await msg.reply("📨 OTP sᴇɴᴛ! Sᴇɴᴅ ɪɴ ғᴏʀᴍᴀᴛ: 1 2 3 4")
        except Exception as e:
            await msg.reply(f"❌ ғᴀɪʟᴇᴅ ᴛᴏ sᴇɴᴅ ᴄᴏᴅᴇ:\n`{e}`")
            await client.disconnect()
            user_sessions.pop(uid, None)

    elif step == "awaiting_otp":
        otp = msg.text.strip()
        client = session["client"]
        try:
            await client.sign_in(
                phone_number=session["phone"],
                phone_code_hash=session["phone_code_hash"],
                phone_code=otp
            )
        except SessionPasswordNeeded:
            session["step"] = "awaiting_2fa"
            await msg.reply("🔐 Sᴇɴᴅ ʏᴏᴜʀ 2FA ᴘᴀssᴡᴏʀᴅ.")
            return
        except Exception as e:
            await msg.reply(f"❌ ғᴀɪʟᴇᴅ ᴛᴏ sɪɢɴ ɪɴ:\n`{e}`")
            await client.disconnect()
            user_sessions.pop(uid, None)
            return

        await complete_login(client, msg, uid)

    elif step == "awaiting_2fa":
        password = msg.text.strip()
        client = session["client"]
        try:
            await client.check_password(password)
        except Exception as e:
            await msg.reply(f"❌ ᴡʀᴏɴɢ ᴘᴀssᴡᴏʀᴅ:\n`{e}`")
            await client.disconnect()
            user_sessions.pop(uid, None)
            return

        await complete_login(client, msg, uid)

async def complete_login(client: Client, msg: Message, uid: int):
    try:
        string = await client.export_session_string()
        user = await client.get_me()

        sessions_col.update_one(
            {"_id": uid},
            {"$set": {
                "session": string,
                "name": user.first_name,
                "user_id": user.id,
                "username": user.username
            }},
            upsert=True
        )

        await msg.reply(
            f"✅ ʟᴏɢɢᴇᴅ ɪɴ ᴀs **{user.first_name}**.\n"
            f"🔐 sᴇssɪᴏɴ:\n`{string}`\n\nᴀᴜᴛᴏ-ʜᴏsᴛɪɴɢ..."
        )

        hosted = Client(
            name=f"AutoClone_{uid}",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=string,
            plugins=dict(root="Zaid/modules")
        )
        await hosted.start()
        await msg.reply(f"✅ ᴀᴜᴛᴏ-ʜᴏsᴛᴇᴅ **{user.first_name}**")
    except Exception as e:
        await msg.reply(f"❌ ғɪɴᴀʟ sᴛᴇᴘ ғᴀɪʟᴇᴅ:\n`{e}`")
    finally:
        await client.disconnect()
        user_sessions.pop(uid, None)
