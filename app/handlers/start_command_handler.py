from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
from app.utils import send_message_wrapper


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_message_wrapper(update=update,
                               context=context,
                               text="Шо хочеш")

start_handler = CommandHandler('start', start)
