import random

from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters


async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    gif_url = ''
    match random.randint(1, 2):
        case 1: gif_url = 'https://tenor.com/suOYulGb5O6.gif'
        case _: gif_url = 'https://tenor.com/o1lxLRIGvE0.gif'
    await context.bot.send_document(chat_id=update.effective_chat.id,
                                    document=gif_url,
                                    reply_to_message_id=update.effective_message.id)

new_member_handler = MessageHandler(filters=filters.StatusUpdate.NEW_CHAT_MEMBERS,
                                         callback=new_member)
