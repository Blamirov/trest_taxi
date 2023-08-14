from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from loguru import logger

@logger.catch
def change_order() -> InlineKeyboardMarkup:
    """
    функция для опроса нужны ли фотографии
    :return: InlineKeyboardMarkup
    """
    keyboard_change = InlineKeyboardMarkup(row_width=1)
    key_cancel = InlineKeyboardButton(text='Отменить заказ', callback_data='cancel')
    key_c_pickup = InlineKeyboardButton(text='Изменить точку сбора', callback_data='change_pickup')
    key_c_destination = InlineKeyboardButton(text='Изменить место назначения', callback_data='change_destination')
    key_c_time = InlineKeyboardButton(text='Изменить время', callback_data='change_time')
    keyboard_change.add(key_cancel, key_c_pickup, key_c_destination, key_c_time)
    return keyboard_change

