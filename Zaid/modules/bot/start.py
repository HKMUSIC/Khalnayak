# © By Shashank Shukla — Don't forget to credit the author.

from Zaid import app, API_ID, API_HASH
from config import OWNER_ID, ALIVE_PIC, MONGO_URL
from pyrogram import Client, filters
from pyrogram.errors import SessionPasswordNeeded
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from Zaid.database.database import Database
import asyncio
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(asctime)s - %(message)s")
logger = logging.getLogger(__name__)

# Initialize the database
db = Database(MONGO_URL)
user_sessions = {}

PHONE_NUMBER_TEXT = (
    "**┆◙ ʕᴇʏ, ɪ ᴀᴍ : [𝕅ᴛʀᴀɴɢʀ ꞅ  𝕊sᴇẇᴿᴇʀʙᴏᴛ]**"
)

@app.on_message(filters.command("start"))
async def start_cmd(client: Client, message: Message):
    buttons = [
        [InlineKeyboardButton("sᴇsᴏʟ ɢᴇɴ ʙᴏᴛ", url="https://t.me/StringSesssionGeneratorRobot")],
        [InlineKeyboardButton("ʜᴏᴡ ᴛᴏ ᴜᴇ ᴛʜɪᴛ ʙᴏᴛ", url="https://t.me/StrangerAssociation/539")],
        [
            InlineKeyboardButton("sᴜᴛᴇʀɿ", url="https://t.me/MASTIWITHFRIENDSXD"),
            InlineKeyboardButton("ᴜᴛᴅᴀᴛᴇ", url="https://t.me/StrangerAssociation"),
        ],
        [InlineKeyboardButton("sʜɪᴡàɴsʜ-xᴅ", url="https://t.me/ITSZ_SHIVANSH")],
    ]
    await message.reply_photo(ALIVE_PIC, caption=PHONE_NUMBER_TEXT, reply_markup=InlineKeyboardMarkup(buttons))


@app.on_message(filters.command("clone"))
async def clone(bot: Client, msg: Message):
    if len(msg.command) < 2:
        return await msg.reply("Usage: /clone <session_string>")
    session_string = msg.command[1]
    try:
        client = Client(name="Melody", api_id=API_ID, api_hash=API_HASH, session_string=session_string, plugins=dict(root="Zaid/modules"))
        await client.start()
        user = await client.get_me()
        await msg.reply(f"❖ Logged in as **{user.first_name}** using the cloned session.")
    except Exception as e:
        logger.error(f"Clone error: {e}")
        await msg.reply(f"**ERROR:** `{str(e)}`\nPress /start to try again.")


@app.on_message(filters.command("add"))
async def start_generate(_, msg: Message):
    await msg.reply("📲 Please send your phone number in international format (e.g., +11234567890):")
    user_sessions[msg.from_user.id] = {"step": "awaiting_phone"}


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
            await msg.reply("📨 OTP sent! Now send it like: `1 2 3 4`")
        except Exception as e:
            logger.error(f"Send code error: {e}")
            await msg.reply(f"❌ Failed to send code: `{e}`\nTry /add again.")
            await client.disconnect()
            user_sessions.pop(uid, None)

    elif step == "awaiting_otp":
        otp = msg.text.strip().replace(" ", "")
        client = session["client"]
        try:
            await client.sign_in(
                phone_number=session["phone"],
                phone_code_hash=session["phone_code_hash"],
                phone_code=otp
            )
        except SessionPasswordNeeded:
            session["step"] = "awaiting_2fa"
            await msg.reply("🔐 2FA enabled. Send your password.")
            return
        except Exception as e:
            logger.error(f"Sign-in error: {e}")
            await msg.reply(f"❌ Failed to sign in: `{e}`\nTry /add again.")
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
            logger.error(f"2FA error: {e}")
            await msg.reply(f"❌ Incorrect password: `{e}`")
            await client.disconnect()
            user_sessions.pop(uid, None)
            return

        await complete_login(client, msg, uid)


async def complete_login(client: Client, msg: Message, uid: int):
    try:
        string = await client.export_session_string()
        user = await client.get_me()
        await msg.reply(f"✅ Logged in as **{user.first_name}**.\n\n🔐 Session string:\n\n`{string}`\n\nAuto-hosting...")

        hosted = Client(
            name=f"AutoClone_{uid}",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=string,
            plugins=dict(root="Zaid/modules")
        )
        await hosted.start()
        await msg.reply(f"✅ Auto-hosted session for **{user.first_name}**.")
        await db.update_session(user.id, string)
    except Exception as e:
        logger.error(f"Complete login error: {e}")
        await msg.reply(f"❌ Final step failed: `{e}`")
    finally:
        await client.disconnect()
        user_sessions.pop(uid, None)


@app.on_message(filters.command("remove"))
async def remove_sessions(_, message: Message):
    if len(message.command) == 1:
        return await message.reply(
            "**Usage:** /remove `<user_id>`\n\nExample: `/remove 123456789`\n\nOr select a session below:",
            reply_markup=await generate_session_buttons()
        )

    try:
        user_id = int(message.command[1])
        success = await db.rm_session(user_id)
        if success:
            await message.reply(f"✅ Session for user `{user_id}` removed successfully.")
        else:
            await message.reply(f"⚠ No session found for user `{user_id}`.")
    except Exception as e:
        logger.error(f"Remove session error: {e}")
        await message.reply(f"❌ Error removing session: `{e}`")


async def generate_session_buttons():
    sessions = await db.get_all_sessions()
    if not sessions:
        return InlineKeyboardMarkup([[InlineKeyboardButton("No sessions available", callback_data="noop")]])

    buttons = []
    for session in sessions:
        user_id = session["user_id"]
        buttons.append([InlineKeyboardButton(f"Remove User ID: {user_id}", callback_data=f"rm_session:{user_id}")])
    return InlineKeyboardMarkup(buttons)


@app.on_callback_query(filters.regex("^rm_session:"))
async def handle_rm_session(client: Client, cb: CallbackQuery):
    user_id = int(cb.data.split(":")[1])
    try:
        success = await db.rm_session(user_id)
        if success:
            await cb.message.edit_text(f"✅ Session for user `{user_id}` removed successfully.")
        else:
            await cb.answer("⚠ Session not found.", show_alert=True)
    except Exception as e:
        logger.error(f"Callback remove session error: {e}")
        await cb.message.edit_text(f"❌ Error removing session: `{e}`")


@app.on_message(filters.command("list"))
async def list_all_sessions(_, message: Message):
    sessions = await db.get_all_sessions()
    if not sessions:
        return await message.reply("⚠ No active sessions found.")

    reply_text = "**📄 Active Sessions:**\n\n"
    for i, s in enumerate(sessions, 1):
        reply_text += f"**{i}.** User ID: `{s['user_id']}`\n"

    await message.reply(reply_text)


@app.on_message(filters.command("clearall") & filters.user(OWNER_ID))
async def clear_all_sessions_cmd(_, message: Message):
    success = await db.clear_all_sessions()
    if success:
        await message.reply("✅ All sessions have been removed from the database.")
    else:
        await message.reply("❌ Failed to clear sessions.")
