from loader import bot
from states.users_states import UserStates
from loguru import logger
from telebot.types import Message



@logger.catch
@bot.message_handler(state=UserStates.none)
def bot_start(message: Message) -> None:
    bot.send_message(message.from_user.id,
                     f'  Здравствуйте {message.from_user.first_name},\n'
                     f'  Благодарим за использование такси от Треста "Арктикуголь"\n'
                     f'  Для заказа такси выберете в меню "заказать такси" и следуйте инструкциям'
                    )