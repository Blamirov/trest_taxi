from telebot.types import Message
from loader import bot
from loguru import logger


@logger.catch
@bot.message_handler(commands=['help'])
def bot_start(message: Message) -> None:
    bot.send_message(message.from_user.id,
                     f'При технической неисправности бота, а также по вопросам улучшения бота, связаться с @blamirov\n'
                     f'Для связи с ресепшеном позвоните по номеру - '
                     )
