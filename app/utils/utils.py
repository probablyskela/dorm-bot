from datetime import datetime

from telegram import Update
from telegram.ext import ContextTypes

from app.utils import cache


async def send_message_wrapper(update: Update,
                               context: ContextTypes.DEFAULT_TYPE,
                               text: str,
                               reply: bool = True,
                               save_reply_ids: bool = True):
    hour = datetime.now().hour

    if hour < 7 and '@' in text:
        text = 'Негоже людей в такий час тегати.'

    message = await context.bot.send_message(chat_id=update.effective_chat.id,
                                             text=text,
                                             reply_to_message_id=update.effective_message.id if reply else None)
    if save_reply_ids:
        await cache.cache.set(update.effective_message.id, message.id, ex=48*60*60)
