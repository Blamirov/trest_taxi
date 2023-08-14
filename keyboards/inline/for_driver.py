from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from loguru import logger

@logger.catch
def for_driver() -> InlineKeyboardMarkup:
    """
    функция для опроса нужны ли фотографии
    :return: InlineKeyboardMarkup
    """
    keyboard_comment = InlineKeyboardMarkup()
    key_yes = InlineKeyboardButton(text='Принимаю', callback_data='yes')
    key_no = InlineKeyboardButton(text='Отказ', callback_data='no')
    keyboard_comment.add(key_no, key_yes)
    return keyboard_comment

@logger.catch
def order_done() -> InlineKeyboardMarkup:
    """
    функция для опроса нужны ли фотографии
    :return: InlineKeyboardMarkup
    """
    keyboard_comment = InlineKeyboardMarkup()
    key_yes = InlineKeyboardButton(text='Заказ выполнен', callback_data='done')
    keyboard_comment.add(key_yes)
    return keyboard_comment

