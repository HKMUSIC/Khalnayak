# © By Shashank shukla Your motherfucker if uh Don't gives credits.
from Zaid import app, API_ID, API_HASH
from config import OWNER_ID, ALIVE_PIC
from pyrogram import Client, filters
from pyrogram.errors import SessionPasswordNeeded
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from Zaid.database.database import init_db, save_session, get_all_sessions, remove_session
import asyncio
import aiosqlite

user_sessions = {}

init_db()  # Initialize DB

# Restore sessions on bot start
async def restore_sessions():
    sessions = get_all_sessions()
    for uid, session in sessions:
        try:
            client = Client(
                name=f"AutoClone_{uid}",
                api_id=API_ID,
                api_hash=API_HASH,
                session_string=session,
                plugins=dict(root="Zaid/modules")
            )
            await client.start()
            print(f"[+] Restored session for user {uid}")
        except Exception as e:
            print(f"[!] Failed to restore session for {uid}: {e}")

app.start()
asyncio.get_event_loop().run_until_complete(restore_sessions())

PHONE_NUMBER_TEXT = (
    "**╭────── ˹ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ˼ ⏤͟͟͞͞★**\n**┆◍ ʜᴇʏ, ɪ ᴀᴍ : [𝛅ᴛʀᴀɴɢᴇʀ ꭙ 𝐔sᴇꝛвσᴛ](https://t.me/StrangerUBbot) **\n**┆● Sᴛʀᴀɴɢᴇʀ Bᴏᴛ Vᴇʀsɪᴏɴ :** `2.1.3`\n**┊● Pᴏᴡᴇʀғᴜʟ & Usᴇғᴜʟ Usᴇʀʙᴏᴛ**\n**╰─────────────────────────**\n**──────────────────────────**\n**❖ Hᴏᴡ Tᴏ Usᴇ Tʜɪs Bᴏᴛ - [Cʟɪᴄᴋ Hᴇʀᴇ](https://t.me/StrangerAssociation/539) **\n**──────────────────────────**\n**❖ Sᴇssɪᴏɴs Gᴇɴ Bᴏᴛ ⁚ [Sᴇssɪᴏɴ-Bᴏᴛ](https://t.me/StringSesssionGeneratorRobot) **\n**──────────────────────────**\n**❖ Cʟᴏɴᴇ Bᴏᴛ  ⁚ /clone [ Sᴛʀɪɴɢ Sᴇssɪᴏɴ ]**\n**❖ Hᴏsᴛ Bᴏᴛ : /add [ᴠɪᴀ ᴘʜᴏɴᴇ ɴᴏ. & ᴏᴛᴘ]**\n**──────────────────────────**\n**❖ Uᴘᴅᴀᴛᴇ ⏤͟͟͞͞  [❖ ∣ Tʜᴇ sᴛʀᴀɴɢᴇʀ ∣ ❖](https://t.me/SHIVANSH474) **\n**──────────────────────────**"
)

@app.on_message(filters.command("start"))
async def hello(client: app, message):
    buttons = [
              [
                  InlineKeyboardButton(text="sᴇssɪᴏɴ ɢᴇɴ ʙᴏᴛ", url="https://t.me/StringSesssionGeneratorRobot"),
              ],
              [
                  InlineKeyboardButton(text="ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴛʜɪs ʙᴏᴛ", url="https://t.me/StrangerAssociation/539"),
              ],
              [
                  InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url="https://t.me/MASTIWITHFRIENDSXD"),
                  InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇ", url="https://t.me/StrangerAssociation"),
              ],
              [
                  InlineKeyboardButton("sʜɪᴠàɴsʜ-xᴅ", url="https://t.me/ITSZ_SHIVANSH"),
              ],
              ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await client.send_photo(message.chat.id, ALIVE_PIC, caption=PHONE_NUMBER_TEXT, reply_markup=reply_markup)

@app.on_message(filters.command("clone"))
async def clone_session(client: app, msg: Message):
    if len(msg.command) < 2:
        await msg.reply("❌ ᴜsᴀɢᴇ: `/clone <string session>`", quote=True)
        return

    string = msg.command[1]
    try:
        clone_client = Client(
            name="clone_client",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=string,
            plugins=dict(root="Zaid/modules")
        )
        await clone_client.start()
        user = await clone_client.get_me()
        await msg.reply(f"✅ Successfully cloned session for **{user.first_name}**.")
    except Exception as e:
        await msg.reply(f"❌ ᴇʀʀᴏʀ:\n`{e}`")

@app.on_message(filters.command("add"))
async def add_session_cmd(_, msg: Message):
    await msg.reply("📲 sᴇɴᴅ ʏᴏᴜʀ ᴘʜᴏɴᴇ ɴᴜᴍʙᴇʀ ɪɴ ɪɴᴛᴇʀɴᴀᴛɪᴏɴᴀʟ ғᴏʀᴍᴀᴛ (e.g., +9123456789):")
    user_sessions[msg.from_user.id] = {"step": "awaiting_phone"}

@app.on_message()
async def handle_flow(_, msg: Message):
    uid = msg.from_user.id
    if uid not in user_sessions:
        return

    session = user_sessions[uid]
    step = session.get("step")

    if step == "awaiting_phone":
        phone = msg.text.strip()
        client = Client(f"login_{uid}", api_id=API_ID, api_hash=API_HASH, in_memory=True)
        session.update({"phone": phone, "client": client})

        try:
            await client.connect()
            code = await client.send_code(phone)
            session["phone_code_hash"] = code.phone_code_hash
            session["step"] = "awaiting_otp"
            await msg.reply("📨 OTP sent! Please reply with the code (e.g., 1 2 3 4):")
        except Exception as e:
            await msg.reply(f"❌ ᴇʀʀᴏʀ sᴇɴᴅɪɴɢ ᴄᴏᴅᴇ:\n`{e}`")
            await client.disconnect()
            user_sessions.pop(uid, None)

    elif step == "awaiting_otp":
        code = msg.text.replace(" ", "")
        client = session["client"]

        try:
            await client.sign_in(
                phone_number=session["phone"],
                phone_code_hash=session["phone_code_hash"],
                phone_code=code
            )
        except SessionPasswordNeeded:
            session["step"] = "awaiting_2fa"
            await msg.reply("🔐 2ғᴀ ɪs ᴇɴᴀʙʟᴇᴅ. sᴇɴᴅ ʏᴏᴜʀ ᴘᴀssᴡᴏʀᴅ.")
            return
        except Exception as e:
            await msg.reply(f"❌ sɪɢɴ-ɪɴ ғᴀɪʟᴇᴅ:\n`{e}`")
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
            await msg.reply(f"❌ ɪɴᴄᴏʀʀᴇᴄᴛ ᴘᴀssᴡᴏʀᴅ:\n`{e}`")
            await client.disconnect()
            user_sessions.pop(uid, None)
            return

        await complete_login(client, msg, uid)

async def complete_login(client: Client, msg: Message, uid: int):
    try:
        string = await client.export_session_string()
        user = await client.get_me()
        save_session(uid, string)
        await msg.reply(f"✅ ʟᴏɢɢᴇᴅ ɪɴ ᴀs **{user.first_name}**.\n🔐 Session:\n`{string}`\n\nᴀᴜᴛᴏ-ʜᴏsᴛɪɴɢ...")

        hosted = Client(
            name=f"AutoClone_{uid}",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=string,
            plugins=dict(root="Zaid/modules")
        )
        await hosted.start()
        await msg.reply("✅ sᴇssɪᴏɴ ʜᴏsᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ.")
    except Exception as e:
        await msg.reply(f"❌ ғɪɴᴀʟ sᴛᴇᴘ ғᴀɪʟᴇᴅ:\n`{e}`")
    finally:
        await client.disconnect()
        user_sessions.pop(uid, None)

@app.on_message(filters.command("remove"))
async def remove_session(_, msg: Message):
    uid = msg.from_user.id
    db_path = "sessions.db"
    table = "sessions"

    async with aiosqlite.connect(db_path) as db:
        await db.execute(f"CREATE TABLE IF NOT EXISTS {table} (user_id INTEGER PRIMARY KEY, session TEXT)")
        async with db.execute(f"SELECT session FROM {table} WHERE user_id = ?", (uid,)) as cursor:
            row = await cursor.fetchone()

        if not row:
            await msg.reply("❌ ɴᴏ sᴇssɪᴏɴ ғᴏᴜɴᴅ ᴛᴏ ʀᴇᴍᴏᴠᴇ.")
            return

        session_string = row[0]
        try:
            rm_client = Client(name=f"remove_{uid}", api_id=API_ID, api_hash=API_HASH, session_string=session_string)
            await rm_client.start()
            await rm_client.log_out()
            await rm_client.stop()
        except Exception as e:
            await msg.reply(f"⚠️ ʟᴏɢᴏᴜᴛ ғᴀɪʟᴇᴅ:\n`{e}`")
            return

        await db.execute(f"DELETE FROM {table} WHERE user_id = ?", (uid,))
        await db.commit()
        await msg.reply("✅ sᴇssɪᴏɴ ʀᴇᴍᴏᴠᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ.")
