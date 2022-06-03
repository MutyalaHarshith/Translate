# Made with python3
# (C) @MutyalaHarshith
# Copyright permission under MIT License
# All rights reserved by Doreamon Fans
# License -> https://github.com/MutyalaHarshith/Translate/blob/master/LICENSE

import os
from io import BytesIO
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from googletrans import Translator

MutyalaHarshith = Client(
    "Translator Bot",
    bot_token = os.environ["BOT_TOKEN"],
    api_id = int(os.environ["API_ID"]),
    api_hash = os.environ["API_HASH"]
)

START_TEXT = """
Hello {}, I am a google translator telegram bot.Project By @MutyalaHarshith To Know How To Use Me Do /help.
Made by @MutyalaHarshith
"""
HELP_TEXT = """
- Just send a text with language code
example :- `MutyalaHarshith | te    for telugu`
           `MutyalaHarshith | ml for malayalam`
           `MutyalaHarshith | kn for kannada`
           `MutyalaHarshith | ta for Tamil`
Still more feature adding 😉
Any doubt contact @Harshith_support 
Made by @MutyalaHarshith
"""
ABOUT_TEXT = """
- **Bot :** `[Google Translator Bot](https://github.com/MutyalaHarshith/Translate)`
- **Creator :** [Harshith](https://telegram.me/Develoveper)
- **Channel :** [Mutyala Harshith](https://telegram.me/MutyalaHarshith)
- **Developer :** [Harshith](https://github.com/MutyalaHarshith)
- **Language :** [Python3](https://python.org)
- **Library :** [Pyrogram](https://pyrogram.org)
- **Server :** [Heroku](https://heroku.com)
"""
START_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Help', callback_data='help'),
        InlineKeyboardButton('About', callback_data='about'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
HELP_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Home', callback_data='home'),
        InlineKeyboardButton('About', callback_data='about'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
ABOUT_BUTTONS = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Channel', url='https://telegram.me/MutyalaHarshith'),
        InlineKeyboardButton('Feedback', url='https://telegram.me/Harshith_Support')
        ],[
        InlineKeyboardButton('Home', callback_data='home'),
        InlineKeyboardButton('Help', callback_data='help'),
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
CLOSE_BUTTON = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Close', callback_data='close')
        ]]
    )
TRANSLATE_BUTTON = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('👨‍🔧 Join Updates Channel 👨‍🔧', url='https://telegram.me/MutyalaHarshith')
        ]]
    )
DEFAULT_LANGUAGE = os.environ.get("DEFAULT_LANGUAGE", "en")

@MutyalaHarshith.on_callback_query()
async def cb_data(bot, update):
    if update.data == "home":
        await update.message.edit_text(
            text=START_TEXT.format(update.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=START_BUTTONS
        )
    elif update.data == "help":
        await update.message.edit_text(
            text=HELP_TEXT,
            disable_web_page_preview=True,
            reply_markup=HELP_BUTTONS
        )
    elif update.data == "about":
        await update.message.edit_text(
            text=ABOUT_TEXT,
            disable_web_page_preview=True,
            reply_markup=ABOUT_BUTTONS
        )
    else:
        await update.message.delete()
    

@MutyalaHarahith.on_message(filters.command(["start"]))
async def start(bot, update):
    text = START_TEXT.format(update.from_user.mention)
    reply_markup = START_BUTTONS
    await update.reply_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )

@MutyalaHarshith.on_message((filters.private | filters.group | ~filters.channel) & filters.text)
async def translate(bot, update):
    if update.chat.type == "private":
        if " | " in update.text:
            text, language = update.text.split(" | ", 1)
        else:
            text = update.text
            language = DEFAULT_LANGUAGE
    else:
        text = update.reply_to_message.text
        if " " in update.text:
            command, language = update.text.split(" | ", 1)
        else:
            language = DEFAULT_LANGUAGE
    translator = Translator()
    await update.reply_chat_action("typing")
    message = await update.reply_text("`Translating 1 sec...`")
    try:
        translate = translator.translate(text, dest=language)
        translate_text = f"**Translated to {language}**"
        translate_text += f"\n\n{translate.text}"
        translate_text += "\n\nMade by @MutyalaHarshith"
        if len(translate_text) < 4096:
            await message.edit_text(
                text=translate_text,
                disable_web_page_preview=True,
                reply_markup=TRANSLATE_BUTTON
            )
        else:
            with BytesIO(str.encode(str(translate_text))) as translate_file:
                translate_file.name = language + ".txt"
                await update.reply_document(
                    document=translate_file,
                    caption="Made by @MutyalaHarshith",
                    reply_markup=TRANSLATE_BUTTON
                )
                await message.delete()
    except Exception as error:
        print(error)
        await message.edit_text("Something wrong. Contact @MutyalaHarshith.")
        return

MutyalaHarshith.run()
