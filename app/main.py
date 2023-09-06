import logging
import os

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder

from app.handlers import (new_member_handler, new_message_handler,
                          start_command_handler)
from app.utils import init_data

load_dotenv()

TOKEN = os.getenv('TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


if __name__ == '__main__':
    application = ApplicationBuilder().token(token=TOKEN).build()

    application.add_handler(start_command_handler.start_handler)
    application.add_handler(new_message_handler.new_message_handler)
    application.add_handler(new_member_handler.new_member_handler)

    init_data()

    application.run_polling()
