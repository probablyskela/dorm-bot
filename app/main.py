import logging
from redis.asyncio.client import Redis

from telegram.ext import ApplicationBuilder

from app.handlers import (new_member_handler, new_message_handler,
                          start_command_handler)
from app.utils.config import settings
from app.utils import cache

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


if __name__ == '__main__':
    application = ApplicationBuilder().token(token=settings.token).build()

    application.add_handler(start_command_handler.start_handler)
    application.add_handler(new_message_handler.new_message_handler)
    application.add_handler(new_member_handler.new_member_handler)

    cache.cache = Redis(host=settings.redis_host,
                        port=settings.redis_port,
                        decode_responses=True)

    application.run_polling()
