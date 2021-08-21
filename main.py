
#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to RC your mac with the Telegram Bot.

Fetch the token from the TG Bot Father and put it into token file.
Then run the bot. I personally use pm2 (
    npm install -g pm2
    pm2 start -n rc ./venv/bin/python3 -- main.py
)

Use the buttons to control the bot.

Author: Seva Oparin
"""

import logging

import applescript
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler

# Enable logging
from typing import Tuple

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

STEP = 5
MAX_VOLUME = 100

def settings() -> Tuple[str, bool]:
    '''
    Fetch the volume settings via apple script
    :return: (volume, sound on/off)
    '''
    tokens = applescript.run("get volume settings").out.split(',')
    logger.info(tokens)
    output = int([token for token in tokens if 'output volume' in token][0].split(':')[1])
    output = int(output / 5 + 0.5) * 5
    muted = bool([token for token in tokens if 'output muted' in token][0].split(':')[1])
    return output, muted


volume, sound_on = settings()
keyboard_markup = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("Up", callback_data='1')
    ],
    [
        InlineKeyboardButton("Down", callback_data='2'),
    ],
    [
        InlineKeyboardButton("Mute", callback_data='3'),
    ],
])


def status_msg() -> str:
    """Return status message for the bot"""
    return f"Hello, this is RC Volume Bot - {volume}{' (muted)' if not sound_on else ''}"


def status_update(update) -> None:
    """Update the previous message with the new status"""
    if update.callback_query:
        update.callback_query.edit_message_text(
            text=status_msg(),
            reply_markup=keyboard_markup
        )


# Define a few command handlers. These usually take the two arguments update and
# context.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    context.bot.send_message(
        text=status_msg(),
        chat_id=update.message.chat_id,
        reply_markup=keyboard_markup
    )


def up(update: Update, context: CallbackContext) -> None:
    """Increase volume by 5%."""
    global volume
    volume = min(volume + STEP, MAX_VOLUME)
    applescript.run(f"set volume output volume {volume}")
    status_update(update)


def down(update: Update, context: CallbackContext) -> None:
    """Decrease volume by 5%."""
    global volume
    volume = max(volume - STEP, 0)
    applescript.run(f"set volume output volume {volume}")
    status_update(update)


def mute(update: Update, context: CallbackContext) -> None:
    """Mute/unmute."""
    global sound_on
    sound_on = not sound_on
    word = 'without' if sound_on else 'with'
    applescript.run(f"set volume {word} output muted")
    status_update(update)


def status(update: Update, context: CallbackContext):
    """Show current status."""
    if update.message:
        chat_id = update.message.chat_id
        context.bot.send_message(
            text=f"Current status: {volume} / {'muted' if mute else 'unmuted'}",
            chat_id=chat_id,
            reply_markup=keyboard_markup
        )
    else:
        status_update(update)


def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    func_choice = {
        1: up,
        2: down,
        3: mute,
        4: status
    }
    try:
        arg = int(query.data)
        if arg in func_choice:
            func_choice[arg](update, context)
    except:
        logger.error(f'Failed to parse button arg: {query.data}')





def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    with open('token', 'r') as f:
        token = f.read()
    updater = Updater(token)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("up", up))
    dispatcher.add_handler(CommandHandler("down", down))
    dispatcher.add_handler(CommandHandler("mute", mute))
    dispatcher.add_handler(CommandHandler("status", status))

    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
