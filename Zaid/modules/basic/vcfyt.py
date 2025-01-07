from pyrogram import Client, filters, enums
from config import SUDO_USERS
from tts_utils import generate_tts
from Zaid import app, SUDO_USER

@Client.on_message(
    filters.command(["tts"], ".") & (filters.me | filters.user(SUDO_USER))
)
async def text_to_speech(client, message):
    """Handles the text-to-speech command."""
    reply = message.reply_to_message

    # If no reply and no text provided
    if not reply:
        if len(message.command) < 2:
            return await message.edit("Reply to a message or provide some text.")

    # If replying to a message
    if reply:
        if not reply.text and not reply.caption:
            return await message.edit("Text not found in the replied message.")
        txt = reply.text if reply.text else reply.caption
    else:
        # If text provided in the command
        txt = message.text.split(None, 1)[1]

    # Generate TTS and save as 'shiv.mp3'
    path = generate_tts(txt)

    try:
        # Delete the original command message
        await message.delete()
    except:
        pass

    try:
        # Send voice message (shiv.mp3) to chat
        await client.send_chat_action(message.chat.id, enums.ChatAction.RECORD_AUDIO)
        await message.reply_voice(path)
        await client.send_chat_action(message.chat.id, enums.ChatAction.CANCEL)
    except:
        await client.send_chat_action(message.chat.id, enums.ChatAction.RECORD_AUDIO)
        await message.reply_audio(path)
        await client.send_chat_action(message.chat.id, enums.ChatAction.CANCEL)

    # Join the voice chat and play 'shiv.mp3'
    try:
        chat_id = message.chat.id
        # Ensure the bot joins the voice chat
        await client.join_voice_chat(chat_id)
        await client.send_audio(chat_id, path)
        await client.leave_voice_chat(chat_id)
    except Exception as e:
        print(f"Error while handling voice chat: {e}")
        await message.reply("Failed to join or play in the voice chat.")