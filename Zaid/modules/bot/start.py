# © By Shashank shukla Your motherfucker if uh Don't gives credits.

from Zaid import app, API_ID, API_HASH
from config import OWNER_ID, ALIVE_PIC
from pyrogram import Client, filters
from pyrogram.errors import SessionPasswordNeeded
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from Zaid.database.database import *
import asyncio

user_sessions = {}

PHONE_NUMBER_TEXT = (
    "**╭────── ˹ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ˼ ⏤͟͟͞͞★**\n"
    "**┆◍ ʜᴇʏ, ɪ ᴀᴍ : [𝛅ᴛʀᴀɴɢᴇʀ ꭙ 𝐔sᴇꝛвσᴛ](https://t.me/StrangerUBbot)**\n"
    "**┆● Sᴛʀᴀɴɢᴇʀ Bᴏᴛ Vᴇʀsɪᴏɴ :** `2.1.3`\n"
    "**┊● Pᴏᴡᴇʀғᴜʟ & Usᴇғᴜʟ Usᴇʀʙᴏᴛ**\n"
    "**❖ Hᴏᴡ Tᴏ Usᴇ Tʜɪs Bᴏᴛ - [Cʟɪᴄᴋ Hᴇʀᴇ](https://t.me/StrangerAssociation/539)**\n"
    "**❖ Sᴇssɪᴏɴs Gᴇɴ Bᴏᴛ ⁚ [Sᴇssɪᴏɴ-Bᴏᴛ](https://t.me/StringSesssionGeneratorRobot)**\n"
    "**❖ Cʟᴏɴᴇ Bᴏᴛ  ⁚ /clone [session]**\n"
    "**❖ Hᴏsᴛ Bᴏᴛ : /add [ᴠɪᴀ ᴘʜᴏɴᴇ ɴᴏ. & ᴏᴛᴘ]**\n"
    "**❖ Uᴘᴅᴀᴛᴇ : [❖ ∣ Tʜᴇ sᴛʀᴀɴɢᴇʀ ∣ ❖](https://t.me/SHIVANSH474)**"
)

@app.on_message(filters.command("start"))
async def start_cmd(client: Client, message: Message):
    buttons = [
        [InlineKeyboardButton("sᴇssɪᴏɴ ɢᴇɴ ʙᴏᴛ", url="https://t.me/StringSesssionGeneratorRobot")],
        [InlineKeyboardButton("ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴛʜɪs ʙᴏᴛ", url="https://t.me/StrangerAssociation/539")],
        [
            InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url="https://t.me/MASTIWITHFRIENDSXD"),
            InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇ", url="https://t.me/StrangerAssociation"),
        ],
        [InlineKeyboardButton("sʜɪᴠàɴsʜ-xᴅ", url="https://t.me/ITSZ_SHIVANSH")],
    ]
    await message.reply_photo(ALIVE_PIC, caption=PHONE_NUMBER_TEXT, reply_markup=InlineKeyboardMarkup(buttons))


@app.on_message(filters.command("clone"))
async def clone(bot: Client, msg: Message):
    if len(msg.command) < 2:
        return await msg.reply("Usage: /clone <session_string>")
    phone = msg.command[1]
    status = await msg.reply("❖ ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ᴀ ᴍɪɴᴜᴛᴇ")
    try:
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
            await msg.reply("📨 OTP sᴇɴᴛ! ɴᴏᴡ sᴇɴᴅ ᴛʜᴇ OTP ʟɪᴋᴇ: `1 2 3 4`")
        except Exception as e:
            await msg.reply(f"❌ ғᴀɪʟᴇᴅ ᴛᴏ sᴇɴᴅ ᴄᴏᴅᴇ: `{e}`\nTry /add again.")
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
            await msg.reply(f"❌ ғᴀɪʟᴇᴅ ᴛᴏ sɪɢɴ ɪɴ: `{e}`\nTry /add again.")
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
            await msg.reply(f"❌ ɪɴᴄᴏʀʀᴇᴄᴛ ᴘᴀssᴡᴏʀᴅ: `{e}`")
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
        await update_session(user.id, string)
    except Exception as e:
        await msg.reply(f"❌ Final step failed: `{e}`")
    finally:
        await client.disconnect()
        user_sessions.pop(uid, None)


@app.on_message(filters.command("remove"))
async def remove_sessions(_, message: Message):
    sessions = await get_all_sessions()
    if not sessions:
        return await message.reply("⚠ No sessions found.")

    buttons = [
        [InlineKeyboardButton(f"Remove {s['user_id']}", callback_data=f"rm_session:{s['user_id']}")]
        for s in sessions
    ]
    buttons.append([InlineKeyboardButton("Cancel ❌", callback_data="auth_close")])
    await message.reply("Choose a session to delete:", reply_markup=InlineKeyboardMarkup(buttons))


@app.on_callback_query(filters.regex(r"rm_session:(\d+)"))
async def handle_rm_session(client: Client, cb: CallbackQuery):
    user_id = int(cb.data.split(":")[1])
    try:
        await rm_session(user_id)
        await cb.message.edit("✅ Session removed successfully.")
    except Exception as e:
        await cb.message.edit(f"❌ Failed to remove session: `{e}`")


@app.on_message(filters.command("list"))
async def list_all_sessions(_, message: Message):
    sessions = await get_all_sessions()
    if not sessions:
        return await message.reply("⚠ No active sessions found.")
    
    reply_text = "**📄 Active Sessions:**\n\n"
    for i, s in enumerate(sessions, 1):
        reply_text += f"**{i}.** User ID: `{s['user_id']}`\n"

    await message.reply(reply_text)
