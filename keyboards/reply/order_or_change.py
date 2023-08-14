from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def start_ordering() -> ReplyKeyboardMarkup:
    markup_reply = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True, one_time_keyboard=True)
    order_button = KeyboardButton(text='Заказать такси')
    change_button = KeyboardButton(text='Внести изменения в заказ')

    markup_reply.add(change_button, order_button)
    return markup_reply

