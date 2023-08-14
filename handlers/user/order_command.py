from loader import bot
from states.users_states import UserStates, DriverStates
from loguru import logger
from keyboards.inline import need_comment, time_now, for_driver
from telebot.types import Message, CallbackQuery
import datetime
from data_base_doc.local_sql import execute_read_query


def done_order(message):
    query_get = f'''SELECT * FROM driver'''
    driver = execute_read_query(query_get)[0][0]
    with bot.retrieve_data(message.from_user.id) as data:
        if isinstance(message, CallbackQuery):
            user_comment = None
        else:
            user_comment = message.text
        bot.send_message(message.from_user.id, f'Ваш заказ:\n'
                                               f'{data["pickup_point"]} -> {data["destination_point"]}\n'
                                               f'Время отправления: {data["service_time"]}\n'
                                               f'Комментарий - {user_comment}\n\n'
                                               f'Идет поиск машины...\n'
                                               f'(Если ответа долго нет, отправьте любое сообщение)')
        bot.send_message(driver, f'Новый заказ!!!:\n'
                                    f'{data["pickup_point"]} -> {data["destination_point"]}\n'
                                    f'Время отправления: {data["service_time"]}\n'
                                    f'Комментарий - {user_comment}\n'
                                    f'Для связи - @{message.from_user.username}',
                         reply_markup=for_driver.for_driver())
        bot.set_state(driver, DriverStates.send_order)
        with bot.retrieve_data(driver) as data_driver:
            data_driver['pickup_point'] = data["pickup_point"]
            data_driver['service_time'] = data["service_time"]
            data_driver['destination_point'] = data["destination_point"]
            data_driver['passenger_id'] = message.from_user.id
            data_driver['comment'] = user_comment
            data_driver['name'] = f'{message.from_user.first_name} {message.from_user.last_name}'
            data_driver['username'] = f'@{message.from_user.username}'
            data_driver['order_time'] = datetime.datetime.now().strftime("%d/%m/%y %H:%M")


@logger.catch
@bot.message_handler(commands=['order'])
def order(message: Message) -> None:
    bot.set_state(message.from_user.id, UserStates.order_time, message.chat.id)
    bot.send_message(message.from_user.id, "Откуда вас забрать?")


@bot.message_handler(state=UserStates.order_time)
def time(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id) as data:
        data['pickup_point'] = message.text
    bot.send_message(message.from_user.id, "В какое время нужна машина?", reply_markup=time_now.time_now())
    bot.set_state(message.from_user.id, UserStates.need_order_time)


@bot.message_handler(state=UserStates.need_order_time)
def rep_time(message: Message) -> None:
    bot.send_message(message.from_user.id, "В какое время нужна машина? \nНажмите на кнопку",
                     reply_markup=time_now.time_now())


@bot.callback_query_handler(state=UserStates.need_order_time, func=lambda call: True)
@logger.catch
def call_time(call: CallbackQuery) -> None:
    """"""
    bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.id, reply_markup=None)
    bot.set_state(call.from_user.id, UserStates.done)
    if call.data == 'now':
        with bot.retrieve_data(call.from_user.id) as data:
            data['service_time'] = 'Ближайшее время'
            bot.set_state(call.from_user.id, UserStates.need_comment)
            bot.send_message(call.from_user.id, "Куда вас отвезти?")
    elif call.data == 'choose':
        bot.set_state(call.from_user.id, UserStates.destination_point)
        bot.send_message(call.from_user.id, "Введите время и дату:")


@bot.message_handler(state=UserStates.destination_point)
def destination(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id) as data:
        data['service_time'] = message.text
    bot.set_state(message.from_user.id, UserStates.need_comment, message.chat.id)
    bot.send_message(message.from_user.id, "Куда вас отвезти?")


@bot.message_handler(state=UserStates.need_comment)
def comment(message: Message) -> None:
    with bot.retrieve_data(message.from_user.id) as data:
        data['destination_point'] = message.text
    bot.set_state(message.from_user.id, UserStates.comment)
    bot.send_message(message.from_user.id, "Хотите добавить комментарий?", reply_markup=need_comment.comment())


@bot.message_handler(state=UserStates.comment)
def rep_comment(message: Message) -> None:
    bot.send_message(message.from_user.id, "Нужен комментарий? \nНажмите на кнопку да или нет",
                     reply_markup=need_comment.comment())


@bot.callback_query_handler(state=UserStates.comment, func=lambda call: True)
@logger.catch
def call_comment(call: CallbackQuery) -> None:
    """Функция для обработки ответа на вопрос нужны ли фотографии"""
    bot.edit_message_reply_markup(chat_id=call.from_user.id, message_id=call.message.id, reply_markup=None)
    bot.set_state(call.from_user.id, UserStates.done)
    if call.data == 'yes':
        bot.send_message(call.from_user.id, 'Введите комментарий:')
    else:
        done_order(message=call)

@bot.message_handler(state=UserStates.done)
def done_survey(message: Message) -> None:
    done_order(message)




if __name__ == "__main__":
    pass