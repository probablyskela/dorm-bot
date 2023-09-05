import logging
import os
import random
import re
from datetime import datetime

from dotenv import load_dotenv
from telegram import InputContactMessageContent, Update
from telegram.ext import (ApplicationBuilder, CommandHandler, ContextTypes,
                          MessageHandler, filters)

load_dotenv()

TOKEN = os.getenv('TOKEN')
COPYPASTE = os.getenv('COPYPASTE')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# TODO: clear data from time to time shob pamyat` ne zasiralasya
message_replies: dict[int, int]


async def send_message_wrapper(update: Update,
                               context: ContextTypes.DEFAULT_TYPE,
                               text: str,
                               save_reply_ids: bool = True):
    if datetime.now().hour < 7 and '@' in text:
        text = 'Негоже людей в такий час тегати.'

    message = await context.bot.send_message(chat_id=update.effective_chat.id,
                                             text=text,
                                             reply_to_message_id=update.effective_message.id)
    if save_reply_ids:
        message_replies[update.effective_message.id] = message_replies.get(
            update.effective_message.id, []) + [message.id]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Шо хочеш")


async def new_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.edited_message is not None:
        message_ids = message_replies.get(update.edited_message.id, [])
        for id in message_ids:
            await context.bot.edit_message_text(text='редачери гавноєди',
                                                chat_id=update.effective_chat.id,
                                                message_id=id)
        message_replies.pop(update.edited_message.id)
    elif update.effective_message.text.lower() == 'ні':
        await send_message_wrapper(update=update,
                                   context=context,
                                   text='hello')
    elif re.compile(r'хто з \d{3}').search(update.effective_message.text.lower()) is not None:
        await send_message_wrapper(update=update,
                                   context=context,
                                   text='@kodein0slav, @Gwinbllade, @afekvova і @zemfirque (але останній лох)')
    elif random.randint(1, 200) == 69:
        await send_message_wrapper(update=update,
                                   context=context,
                                   text=COPYPASTE)
    elif '@probablyskela' in update.effective_message.text.lower() is not None:
        await send_message_wrapper(update=update,
                                   context=context,
                                   text='скела крутий')


async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    gif_url = ''
    match random.randint(1, 2):
        case 1: gif_url = 'https://tenor.com/suOYulGb5O6.gif'
        case _: gif_url = 'https://tenor.com/o1lxLRIGvE0.gif'
    await context.bot.send_document(chat_id=update.effective_chat.id,
                                    document=gif_url,
                                    reply_to_message_id=update.effective_message.id)


if __name__ == '__main__':
    application = ApplicationBuilder().token(token=TOKEN).build()

    message_replies = dict()

    start_handler = CommandHandler('start', start)
    new_message_handler = MessageHandler(filters=filters.TEXT & (~filters.COMMAND),
                                         callback=new_message)
    new_chat_member_handler = MessageHandler(filters=filters.StatusUpdate.NEW_CHAT_MEMBERS,
                                             callback=new_member)

    application.add_handler(start_handler)
    application.add_handler(new_message_handler)
    application.add_handler(new_chat_member_handler)

    application.run_polling()
