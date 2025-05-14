from Zaid import app, API_ID, API_HASH
from config import OWNER_ID, ALIVE_PIC
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
import asyncio

# Temporary state store
user_sessions = {}

PHONE_NUMBER_TEXT = (
    "**╭────── ˹ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ˼ ⏤͟͟͞͞★**\n"
    "**┆◍ ʜᴇʏ, ɪ ᴀᴍ : [𝛅ᴛʀᴀɴɢᴇʀ ꭙ 𝐔sᴇꝛвσᴛ](https://t.me/Shukla_op_clone1bot)**\n"
    "**┆● Vᴇʀsɪᴏɴ :** `2.1.3`\n"
    "**┊● Pᴏᴡᴇʀғᴜʟ & Usᴇғᴜʟ Usᴇʀʙᴏᴛ**\n"
    "**❖ Hᴏᴡ Tᴏ Usᴇ - [Click Here](https://t.me/StrangerAssociation/539)**\n"
    "**❖ Sᴇssɪᴏɴs Gᴇɴ : [Generator Bot](https://t.me/StringSesssionGeneratorRobot)**\n"
    "**❖ Cʟᴏɴᴇ Cᴏᴍᴍᴀɴᴅ ⁚ /clone [session_string]**\n"
    "**❖ Uᴘᴅᴀᴛᴇs ⁚ [❖ ∣ Tʜᴇ sᴛʀᴀɴɢᴇʀ ∣ ❖](https://t.me/SHIVANSH474)**"
)

@app.on_message(filters.command("start"))
async def hello(client: Client, message: Message):
    buttons = [
        [InlineKeyboardButton("sᴇssɪᴏɴ ɢᴇɴ ʙᴏᴛ", url="https://t.me/StringSesssionGeneratorRobot")],
        [InlineKeyboardButton("ʜᴏᴡ ᴛᴏ ᴜsᴇ ᴛʜɪs ʙᴏᴛ", url="https://t.me/StrangerAssociation/539")],
        [
            InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url="https://t.me/MASTIWITHFRIENDSXD"),
            InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇ", url="https://t.me/StrangerAssociation"),
        ],
        [InlineKeyboardButton("sʜɪᴠàɴsʜ-xᴅ", url="https://t.me/ITSZ_SHIVANSH")],
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await client.send_photo(message.chat.id, ALIVE_PIC, caption=PHONE_NUMBER_TEXT, reply_markup=reply_markup)


@app.on_message(filters.user(OWNER_ID) & filters.command("generate"))
async def start_generate(_, msg: Message):
    await msg.reply("📲 Please send your phone number in international format (e.g., +11234567890):")
    user_sessions[msg.from_user.id] = {"step": "awaiting_phone"}


@app.on_message(filters.user(OWNER_ID))
async def session_flow(_, msg: Message):
    uid = msg.from_user.id

    if uid not in user_sessions:
        return

    session = user_sessions[uid]
    step = session.get("step")

    if step == "awaiting_phone":
        session["phone"] = msg.text
        session["client"] = Client(
            name="gen_session",
            api_id=API_ID,
            api_hash=API_HASH,
            in_memory=True
        )
        try:
            await session["client"].connect()
            sent = await session["client"].send_code(session["phone"])
            session["phone_code_hash"] = sent.phone_code_hash
            session["step"] = "awaiting_otp"
            await msg.reply("📨 OTP sent! Now send the OTP code you received.")
        except Exception as e:
            del user_sessions[uid]
            await msg.reply(f"❌ Failed to send OTP:\n`{e}`")

    elif step == "awaiting_otp":
        otp_code = msg.text.strip()
        try:
            await session["client"].sign_in(
                phone_number=session["phone"],
                phone_code_hash=session["phone_code_hash"],
                phone_code=otp_code
            )
            string = await session["client"].export_session_string()
            user = await session["client"].get_me()
            await msg.reply(f"✅ Logged in as {user.first_name}.\n\n🔐 Session String:\n`{string}`\n\nAuto-hosting now...")

            hosted_client = Client(
                name="AutoClone",
                api_id=API_ID,
                api_hash=API_HASH,
                session_string=string,
                plugins=dict(root="Zaid/modules")
            )
            await hosted_client.start()
            await msg.reply(f"✅ Session auto-hosted as **{user.first_name}**.")
            await session["client"].disconnect()
            del user_sessions[uid]
        except Exception as e:
            if "2FA" in str(e):
                session["step"] = "awaiting_2fa"
                await msg.reply("🔐 This account has 2-Step Verification.\nPlease send your password.")
            else:
                await msg.reply(f"❌ Failed to sign in:\n`{e}`")
                del user_sessions[uid]

    elif step == "awaiting_2fa":
        password = msg.text.strip()
        try:
            await session["client"].check_password(password)
            string = await session["client"].export_session_string()
            user = await session["client"].get_me()
            await msg.reply(f"✅ Logged in as {user.first_name}.\n\n🔐 Session String:\n`{string}`\n\nAuto-hosting now...")

            hosted_client = Client(
                name="AutoClone",
                api_id=API_ID,
                api_hash=API_HASH,
                session_string=string,
                plugins=dict(root="Zaid/modules")
            )
            await hosted_client.start()
            await msg.reply(f"✅ Session auto-hosted as **{user.first_name}**.")
            await session["client"].disconnect()
        except Exception as e:
            await msg.reply(f"❌ 2FA Error:\n`{e}`")
        del user_sessions[uid]


@app.on_message(filters.command("clone"))
async def clone(bot: Client, msg: Message):
    if len(msg.command) < 2:
        return await msg.reply("❍ HOW TO USE\n\n𔓕 /clone <session_string>\n𔓕 /clone save msg code")
    phone = msg.command[1]
    text = await msg.reply("❖ ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ᴀ ᴍɪɴᴜᴛᴇ")
    try:
        client = Client(
            name="Melody",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=phone,
            plugins=dict(root="Zaid/modules")
        )
        await client.start()
        user = await client.get_me()
        await msg.reply(
            f"❖ ɴᴏᴡ ʏᴏᴜ ᴀʀᴇ ʀᴇᴀᴅʏ ᴛᴏ ғɪɢʜᴛ\n\n"
            f"❍ [❖ │ sᴛʀᴀɴɢᴇʀ ꭙ ʙᴏᴛ │ ❖](https://t.me/SHIVANSH474)\n\n"
            f"❖ {user.first_name}"
        )
    except Exception as e:
        await msg.reply(f"**ERROR:** `{str(e)}`\nPress /start to try again.")
