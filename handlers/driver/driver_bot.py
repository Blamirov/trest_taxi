from loader import bot
from states.users_states import UserStates, DriverStates
from loguru import logger
from telebot.types import Message, CallbackQuery
from data_base_doc.local_sql import insert_query_data


@bot.callback_query_handler(state=DriverStates.send_order, func=lambda call: True)
@logger.catch
def driver_answer(call: CallbackQuery) -> None:
    """"""
    bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.id, reply_markup=None)
    with bot.retrieve_data(call.from_user.id) as data:
        data['tg_driver_id'] = call.from_user.id
        if call.data == 'yes':
            bot.send_message(data['passenger_id'], f'Ваш заказ принят ожидайте такси, для связи с водителем - @'
                                                   f'{call.from_user.username}')
            bot.set_state(data['passenger_id'], UserStates.none)
            bot.send_message(call.from_user.id, f'Для того чтобы отметь заказ выполненным нажмите - /approved_order\n'
                                                f'Для просмотра активных заказов нажмите - /active_order\n'
                                                f'Для отмены заказа нажмите - /cancel_order\n'
                                                f'Для связи с клиентом нажмите - /connection_to_passenger'
                             )
            insert_query_data(data)

        else:
            bot.send_message(call.from_user.id, 'Введите причину отказа (заказчик увидит этот комментарий):')
            bot.set_state(data['passenger_id'], UserStates.none)
            bot.set_state(call.from_user.id, DriverStates.cancel_order)


@bot.message_handler(state=DriverStates.cancel_order)
def done_survey(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id) as data:
        bot.send_message(data['passenger_id'], f'Машина не найдена, комментарий водителя: {message.text}')
        bot.set_state(data['passenger_id'], UserStates.none)
