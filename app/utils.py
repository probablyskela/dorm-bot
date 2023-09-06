from datetime import datetime

from telegram import Update
from telegram.ext import ContextTypes


class ReplyInfo():
    def __init__(self, reply_id: int, hour: int) -> None:
        self.reply_id = reply_id
        self.hour = hour


message_replies: dict[int, ReplyInfo]
last_clear_time: int = 0


def get_replies():
    return message_replies


def init_data():
    global message_replies
    message_replies = dict()
    last_clear_time = 0


async def send_message_wrapper(update: Update,
                               context: ContextTypes.DEFAULT_TYPE,
                               text: str,
                               reply: bool = True,
                               save_reply_ids: bool = True):
    global last_clear_time
    global message_replies

    hour = datetime.now().hour

    if hour < 7 and '@' in text:
        text = 'Негоже людей в такий час тегати.'

    message = await context.bot.send_message(chat_id=update.effective_chat.id,
                                             text=text,
                                             reply_to_message_id=update.effective_message.id if reply else None)
    if save_reply_ids:
        message_replies[update.effective_message.id] = ReplyInfo(reply_id=message.id,
                                                                 hour=hour)

    # Clear data every 8 hours if data is older than 8 hours
    if last_clear_time != hour % 8:
        for key, value in message_replies.items():
            if hour - value.hour > 8 or hour - value.hour < 0:
                message_replies.pop(key, None)
        last_clear_time = hour % 8
