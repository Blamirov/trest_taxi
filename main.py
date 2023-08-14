from loader import bot
import handlers
from telebot.custom_filters import StateFilter, IsDigitFilter
from utils.set_bot_commands import set_default_commands
from loguru import logger
from data_base_doc.local_sql import creation_db


if __name__ == '__main__':
    logger.add('logger.log', format='{time:YYYY-MM-DD HH:mm:ss} {level} {message}')
    creation_db()
    bot.add_custom_filter(StateFilter(bot))
    bot.add_custom_filter(IsDigitFilter())
    set_default_commands(bot)
    bot.infinity_polling()
