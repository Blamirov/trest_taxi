from loader import bot
from states.users_states import DriverStates
from loguru import logger
from telebot.types import Message, CallbackQuery
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from data_base_doc.local_sql import execute_read_query
from os import getenv
from dotenv import load_dotenv, find_dotenv
from data_base_doc.data_base import send_data_to_sheep

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

spreadsheet_id = getenv('Spreadsheet_id')


@logger.catch
@bot.message_handler(commands=['cancel_order'])
def order(message: Message) -> None:
    """
    Если несколько заказов, то функция отправляет кнопки для выбора нужного заказа.
    Если заказ один, то он сразу его удаляет.

    """
    query = f'''SELECT * FROM orders'''
    data = execute_read_query(query)
    if len(data) == 1:
        query_for_passenger_id = f'''SELECT tg_user_id FROM orders'''
        passenger_id = execute_read_query(query_for_passenger_id)
        bot.send_message(passenger_id[0][0], 'Ваш заказ был отменен')
        query = f'''DELETE FROM orders'''
        execute_read_query(query)
        bot.send_message(message.from_user.id, 'Заказ был успешно отменен')
        send_data_to_sheep(data=data, spreadsheet_id=spreadsheet_id, message=message, status='Отменен')


    elif len(data) > 1:
        bot.set_state(message.from_user.id, DriverStates.cancel_order_after_approved)
        keyboard_cancel = InlineKeyboardMarkup(row_width=1)
        key = [InlineKeyboardButton(text=f'{active_order[3]} -> {active_order[4]}, {active_order[2]}',
                                    callback_data=active_order[0]) for active_order in data]
        keyboard_cancel.add(*key)
        bot.send_message(message.from_user.id, 'Выберите заказ', reply_markup=keyboard_cancel)
    else:
        bot.send_message(message.from_user.id, 'Нет активных заказов')


@bot.callback_query_handler(state=DriverStates.cancel_order_after_approved, func=lambda call: True)
@logger.catch
def call_comment(call: CallbackQuery) -> None:

    """Функция удаляет выбранный заказ из таблицы orders и отправляет сообщение пользователю и водителю"""

    bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.id, reply_markup=None)
    query_for_passenger_id = f'''SELECT tg_user_id FROM orders WHERE id = {call.data}'''
    data = f'''SELECT * FROM orders WHERE id = {call.data}'''
    passenger_id = execute_read_query(query_for_passenger_id)
    bot.send_message(passenger_id[0][0], 'Ваш заказ был отменен')
    query = f'''DELETE FROM orders WHERE id = {call.data}'''
    execute_read_query(query)
    bot.send_message(call.from_user.id, 'Заказ был успешно отменен')
    send_data_to_sheep(data=data, spreadsheet_id=spreadsheet_id, message=call, status='Отменен')


if __name__ == '__main__':
    pass
