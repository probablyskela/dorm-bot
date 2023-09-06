import logging

import openai
from redis.asyncio.client import Redis
from telegram.ext import ApplicationBuilder

from app.handlers import (new_member_handler, new_message_handler,
                          start_command_handler)
from app.utils import cache
from app.utils.config import settings

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


if __name__ == '__main__':
    application = ApplicationBuilder().token(token=settings.TOKEN).build()

    application.add_handler(start_command_handler.start_handler)
    application.add_handler(new_message_handler.new_message_handler)
    application.add_handler(new_member_handler.new_member_handler)

    cache.cache = Redis(host=settings.REDIS_HOST,
                        port=settings.REDIS_PORT,
                        decode_responses=True)
    openai.api_key = settings.OPENAI_API_KEY

    application.run_polling()
