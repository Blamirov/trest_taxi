from loader import bot
from states.users_states import DriverStates
from loguru import logger
from telebot.types import Message, CallbackQuery
from data_base_doc.local_sql import execute_query
from data_base_doc.local_sql import execute_read_query


@logger.catch
@bot.message_handler(commands=['idriver'])
def connection_to_passenger(message: Message) -> None:
    """ Функция устанавливает id водителя"""
    query_get = f'''SELECT * FROM driver'''
    data = execute_read_query(query_get)
    if data:
        query = f"""Update driver set driver_id = ?"""
        execute_query(query, [message.from_user.id])
    else:
        query = """INSERT INTO driver(driver_id)
                       VALUES(?)"""
        execute_query(query, [message.from_user.id])
    bot.send_message(message.from_user.id, "Отлично, все заказы будут поступать вам!")
