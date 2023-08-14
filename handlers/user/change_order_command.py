from loader import bot
from states.users_states import UserStates
from loguru import logger
from keyboards.inline import change_order_button
from telebot.types import Message, CallbackQuery
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from data_base_doc.local_sql import execute_read_query, execute_query


@logger.catch
@bot.message_handler(commands=['change'])
def change_order(message: Message) -> None:
    """

    :param message:
    :return:
    """

    query = f'''SELECT * FROM orders WHERE tg_user_id = {message.from_user.id}'''
    data = execute_read_query(query)
    if len(data) == 1:
        order_num = data[0][0]
        bot.send_message(message.from_user.id, 'Что нужно изменить:', reply_markup=change_order_button.change_order())
        bot.set_state(message.from_user.id, UserStates.user_changing)
        with bot.retrieve_data(message.from_user.id) as data:
            data['num_cancel_order'] = order_num
    elif len(data) > 1:
        keyboard_change = InlineKeyboardMarkup(row_width=1)
        key = [InlineKeyboardButton(text=f'{active_order[3]} -> {active_order[4]}, {active_order[2]}',
                                    callback_data=active_order[0]) for active_order in data]
        keyboard_change.add(*key)
        bot.send_message(message.from_user.id, 'Выберите заказ', reply_markup=keyboard_change)
        bot.set_state(message.from_user.id, UserStates.user_choose_order)
    else:
        bot.send_message(message.from_user.id, 'Нет активных заказов')


@bot.callback_query_handler(state=UserStates.user_choose_order, func=lambda call: True)
@logger.catch
def call_choose_order(call: CallbackQuery) -> None:
    bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.id, reply_markup=None)
    with bot.retrieve_data(call.from_user.id) as data:
        data['num_cancel_order'] = call.data
        bot.send_message(call.from_user.id, 'Что нужно изменить:', reply_markup=change_order_button.change_order())
        bot.set_state(call.from_user.id, UserStates.user_changing)


@bot.callback_query_handler(state=UserStates.user_changing, func=lambda call: True)
@logger.catch
def call_change_order(call: CallbackQuery) -> None:
    with bot.retrieve_data(call.from_user.id) as data:
        query_for_passenger_id = f'''SELECT tg_driver_id FROM orders WHERE id = {data['num_cancel_order']}'''
        driver_id = execute_read_query(query_for_passenger_id)[0][0]
        if call.data == 'cancel':
            bot.send_message(driver_id, 'Отмена заказа')
            query = f'''DELETE FROM orders WHERE id = {data['num_cancel_order']}'''
            execute_read_query(query)
            bot.send_message(call.from_user.id, 'Заказ отменен')
        elif call.data == 'change_pickup':
            bot.send_message(call.from_user.id, 'Введите новый адрес')
            data['change'] = 'pickup'
            bot.send_message(driver_id, 'У заказа изменение адреса!')
        elif call.data == 'change_destination':
            bot.send_message(call.from_user.id, 'Введите новый адрес')
            data['change'] = 'destination'
            bot.send_message(driver_id, 'У заказа изменение адреса!')
        elif call.data == 'change_time':
            bot.send_message(call.from_user.id, 'Введите новое время')
            data['change'] = 'time'
            bot.send_message(driver_id, 'У заказа изменение времени!')
        else:
            bot.send_message(call.from_user.id, 'Ошибка ввода ')

    bot.set_state(call.from_user.id, UserStates.approved_changing)


@bot.message_handler(state=UserStates.approved_changing)
def approved_changing(message: Message):
    with bot.retrieve_data(message.from_user.id) as data:
        query = f"""Update orders set {data['change']} = ? where id = ?"""
        execute_query(query, [message.text, data['num_cancel_order']])

    bot.send_message(message.from_user.id, 'Обновления внесены')
    bot.set_state(message.from_user.id, UserStates.none)


if __name__ == "__main__":
    pass
