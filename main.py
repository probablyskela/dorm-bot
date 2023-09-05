import logging
import os
import random
import re

from dotenv import load_dotenv
from telegram import Update, InputContactMessageContent
from telegram.ext import (ApplicationBuilder, CommandHandler, ContextTypes,
                          MessageHandler, filters)

load_dotenv()

TOKEN = os.getenv('TOKEN')
COPYPASTE = os.getenv('COPYPASTE')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="Шо хочеш")


async def new_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    room_regex = re.compile(r'хто з \d{3}')
    if update.effective_message.text.lower() == 'ні':
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='hello',
                                       reply_to_message_id=update.effective_message.id)
    if room_regex.search(update.effective_message.text.lower()) is not None:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='@kodein0slav, @Gwinbllade, @afekvova і @zemfirque (але останній лох)',
                                       reply_to_message_id=update.effective_message.id)
    elif random.randint(1, 300) == 69:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text=COPYPASTE,
                                       reply_to_message_id=update.effective_message.id)


async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    gif_url = ''
    match random.randint(1, 2):
        case 1: gif_url = 'asd'
        case _: gif_url = 'asd'
    await context.bot.send_document(chat_id=update.effective_chat.id,
                                    document=gif_url,
                                    reply_to_message_id=update.effective_message.id)


if __name__ == '__main__':
    application = ApplicationBuilder().token(token=TOKEN).build()

    start_handler = CommandHandler('start', start)
    new_message_handler = MessageHandler(filters=filters.TEXT & (~filters.COMMAND),
                                         callback=new_message)
    new_chat_member_handler = MessageHandler(filters=filters.StatusUpdate.NEW_CHAT_MEMBERS,
                                             callback=new_member)

    application.add_handler(start_handler)
    application.add_handler(new_message_handler)
    # application.add_handler(new_chat_member_handler)

    application.run_polling()
