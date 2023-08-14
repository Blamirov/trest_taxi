from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from loguru import logger

@logger.catch
def time_now() -> InlineKeyboardMarkup:
    """
    функция для опроса нужны ли фотографии
    :return: InlineKeyboardMarkup
    """
    keyboard_time_now = InlineKeyboardMarkup()
    key_now = InlineKeyboardButton(text='Ближайшее время', callback_data='now')
    key_time = InlineKeyboardButton(text='На точное время', callback_data='choose')
    keyboard_time_now.add(key_now, key_time)
    return keyboard_time_now
