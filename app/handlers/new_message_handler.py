import os
import random
import re

from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from app.utils import get_replies, send_message_wrapper

COPYPASTE = os.getenv('COPYPASTE')


async def new_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.edited_message is not None:
        reply_info = get_replies().get(update.edited_message.id, None)
        if reply_info is not None:
            await context.bot.edit_message_text(text='редачери гавноєди',
                                                chat_id=update.effective_chat.id,
                                                message_id=reply_info.reply_id)
            get_replies().pop(update.edited_message.id, None)
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

new_message_handler = MessageHandler(filters=filters.TEXT & (~filters.COMMAND),
                                     callback=new_message)
