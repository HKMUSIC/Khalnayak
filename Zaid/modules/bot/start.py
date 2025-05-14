from Zaid import app, API_ID, API_HASH
from config import OWNER_ID
from pyrogram import Client, filters
from pyrogram.errors import SessionPasswordNeeded
from pyrogram.types import Message

user_sessions = {}

PHONE_NUMBER_TEXT = (
    "**╭────── ˹ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ˼ ⏤͟͟͞͞★**\n**┆◍ ʜᴇʏ, ɪ ᴀᴍ : [𝛅ᴛʀᴀɴɢᴇʀ ꭙ 𝐔sᴇꝛвσᴛ](https://t.me/StrangerUBbot) **\n**┆● Sᴛʀᴀɴɢᴇʀ Bᴏᴛ Vᴇʀsɪᴏɴ :** `2.1.3`\n**┊● Pᴏᴡᴇʀғᴜʟ & Usᴇғᴜʟ Usᴇʀʙᴏᴛ**\n**╰─────────────────────────**\n**──────────────────────────**\n**❖ Hᴏᴡ Tᴏ Usᴇ Tʜɪs Bᴏᴛ - [Cʟɪᴄᴋ Hᴇʀᴇ](https://t.me/StrangerAssociation/539) **\n**──────────────────────────**\n**❖ Sᴇssɪᴏɴs Gᴇɴ Bᴏᴛ ⁚ [Sᴇssɪᴏɴ-Bᴏᴛ](https://t.me/StringSesssionGeneratorRobot) **\n**──────────────────────────**\n**❖ Cʟᴏɴᴇ Bᴏᴛ  ⁚ /clone [ Sᴛʀɪɴɢ Sᴇssɪᴏɴ ]**\n**──────────────────────────**\n**❖ Uᴘᴅᴀᴛᴇ ⏤͟͟͞͞  [❖ ∣ Tʜᴇ sᴛʀᴀɴɢᴇʀ ∣ ❖](https://t.me/SHIVANSH474) **\n**──────────────────────────**"
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

# © By Shashank shukla Your motherfucker if uh Don't gives credits.
@app.on_message(filters.command("clone"))
async def clone(bot: app, msg: Message):
    chat = msg.chat
    text = await msg.reply("❍ HOW TO USE \n\n𔓕 /clone session \n𔓕 /clone save msg code")
    cmd = msg.command
    phone = msg.command[1]
    try:
        await text.edit("❖ ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ ᴀ ᴍɪɴᴜᴛᴇ")
                   # change this Directry according to ur repo
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

    # Step 1: Receive Phone Number
    if step == "awaiting_phone":
        phone = msg.text.strip()
        client = Client(name=f"gen_session_{uid}", api_id=API_ID, api_hash=API_HASH, in_memory=True)
        session.update({"phone": phone, "client": client})

        try:
            await client.connect()
            sent = await client.send_code(phone)
            session["phone_code_hash"] = sent.phone_code_hash
            session["step"] = "awaiting_otp"
            await msg.reply("📨 OTP sᴇɴᴛ! ɴᴏᴡ sᴇɴᴅ ᴛʜᴇ OTP ᴄᴏᴅᴇ ʏᴏᴜ ʀᴇᴄᴇɪᴠᴇᴅ.")
        except Exception as e:
            await msg.reply(f"❌ ғᴀɪʟᴇᴅ ᴛᴏ sᴇɴᴅ ᴄᴏᴅᴇ:\n`{e}`")
            await client.disconnect()
            user_sessions.pop(uid, None)

    # Step 2: Receive OTP
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
            await msg.reply("🔐 2-sᴛᴇᴘ ᴠᴇʀɪғɪᴄᴀᴛɪᴏɴ ɪs ᴇɴᴀʙʟᴇᴅ.\nᴘʟᴇᴀsᴇ sᴇɴᴅ ʏᴏᴜʀ ᴘᴀssᴡᴏʀᴅ.")
            return
        except Exception as e:
            await msg.reply(f"❌ ғᴀɪʟᴇᴅ ᴛᴏ sɪɢɴ ɪɴ:\n`{e}`")
            await client.disconnect()
            user_sessions.pop(uid, None)
            return

        await complete_login(client, msg, uid)

    # Step 3: Receive 2FA Password
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
        await msg.reply(f"✅ ʟᴏɢɢᴇᴅ ɪɴ ᴀs **{user.first_name}**.\n\n🔐 sᴇssɪᴏɴ sᴛʀɪɴɢ:\n`{string}`\n\nᴀᴜᴛᴏ-ʜᴏsᴛ ɴᴏᴡ...")

        hosted = Client(
            name=f"AutoClone_{uid}",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=string,
            plugins=dict(root="Zaid/modules")
        )
        await hosted.start()
        await msg.reply(f"✅ sᴇssɪᴏɴ ᴀᴜᴛᴏ- ʜᴏsᴛᴇᴅ ᴀs **{user.first_name}**.")

    except Exception as e:
        await msg.reply(f"❌ ғɪɴᴀʟ sᴛᴇᴘ ғᴀɪʟᴇᴅ:\n`{e}`")

    finally:
        await client.disconnect()
        user_sessions.pop(uid, None)
