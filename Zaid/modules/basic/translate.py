import os
from pyrogram import Client, filters
from pyrogram.types import Message
from py_trans import Async_PyTranslator

from Zaid.modules.help import add_command_help
from Zaid.helper.utility import get_arg


@Client.on_message(filters.command(["tr", "translate"], ["."]) & filters.me)
async def pytrans_tr(_, message: Message):
    tr_msg = await message.edit("`Processing...`")
    r_msg = message.reply_to_message
    args = get_arg(message)

    if not args and not r_msg:
        return await tr_msg.edit("`Please reply to a message or provide text to translate.`")

    if r_msg and r_msg.text:
        to_tr = r_msg.text
        if not args:
            return await tr_msg.edit("`Please define a destination language.`\n\nExample: `.tr hi`")
        sp_args = args.split(" ", 1)
        dest_lang = sp_args[0]
        tr_engine = sp_args[1] if len(sp_args) == 2 else "google"

    elif args:
        sp_args = args.split(" ", 2)
        if len(sp_args) == 3:
            dest_lang, tr_engine, to_tr = sp_args
        elif len(sp_args) == 2:
            dest_lang, to_tr = sp_args
            tr_engine = "google"
        else:
            return await tr_msg.edit("`Please provide both language and text to translate.`\n\nExample: `.tr hi Hello World`")

    try:
        py_trans = Async_PyTranslator()
        await py_trans.ainit()  # important!
        translation = await py_trans.atranslate(to_tr, dest_lang, engine=tr_engine)
    except Exception as e:
        return await tr_msg.edit(f"`Translation failed:` {e}")

    if translation.get("status") == "success":
        tred_txt = f"""
**Translation Engine**: `{translation["engine"]}`
**Translated to:** `{translation["dest_lang"]}`
**Translation:**
`{translation["translation"]}`
"""
        if len(tred_txt) > 4096:
            temp_file = "translated.txt"
            with open(temp_file, "w", encoding="utf-8") as f:
                f.write(tred_txt)
            await tr_msg.reply_document(temp_file, caption="`Translated Text File`")
            os.remove(temp_file)
            await tr_msg.delete()
        else:
            await tr_msg.edit(tred_txt)
    else:
        await tr_msg.edit("`Failed to translate the text.`")


add_command_help(
    "translate",
    [
        [".tr [lang] [text]", "Translate the given text to the target language."],
        [".tr [lang]", "Reply to a message to translate it to the specified language."],
    ],
)
