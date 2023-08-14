from loader import bot
from states.users_states import DriverStates
from loguru import logger
from telebot.types import Message, CallbackQuery
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from data_base_doc.local_sql import execute_read_query


@logger.catch
@bot.message_handler(commands=['connection_to_passenger'])
def connection_to_passenger(message: Message) -> None:
    """ Функция запрашивает у водителя сообщение для пользователя"""
    bot.send_message(message.from_user.id, 'Введите сообщение:')
    bot.set_state(message.from_user.id, DriverStates.send_message_to_pas)


@bot.message_handler(state=DriverStates.send_message_to_pas)
def order(message: Message) -> None:
    """

    :param message:
    :return:
    """
    query = f'''SELECT * FROM orders'''
    info = execute_read_query(query)
    if len(info) == 1:
        query_for_passenger_id = f'''SELECT tg_user_id FROM orders'''
        passenger_id = execute_read_query(query_for_passenger_id)[0][0]
        bot.send_message(passenger_id, f"Сообщение от водителя: {message.text}\n"
                                       f"для ответа напишите водителю на @{message.from_user.username}")
        bot.send_message(message.from_user.id, 'Сообщение отправлено')

    elif len(info) > 1:
        with bot.retrieve_data(message.from_user.id) as data:
            data['message'] = message.text
        keyboard_cancel = InlineKeyboardMarkup(row_width=1)
        key = [InlineKeyboardButton(text=f'{active_order[3]} -> {active_order[4]}, {active_order[2]}',
                                    callback_data=active_order[0]) for active_order in info]
        keyboard_cancel.add(*key)
        bot.send_message(message.from_user.id, 'Выберите заказ', reply_markup=keyboard_cancel)
    else:
        bot.send_message(message.from_user.id, 'Нет активных заказов')


@bot.callback_query_handler(state=DriverStates.send_message_to_pas, func=lambda call: True)
@logger.catch
def call_comment(call: CallbackQuery) -> None:
    bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.id, reply_markup=None)
    query_for_passenger_id = f'''SELECT tg_user_id FROM orders WHERE id = {call.data}'''
    passenger_id = execute_read_query(query_for_passenger_id)
    with bot.retrieve_data(call.from_user.id) as data:
        bot.send_message(passenger_id[0][0], f"Сообщение от водителя: {data['message']}\n"
                                             f"для ответа напишите водителю на @{call.from_user.username}")
    bot.send_message(call.from_user.id, 'Сообщение отправлено')
