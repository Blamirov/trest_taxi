from loader import bot
from loguru import logger
from telebot.types import Message
from data_base_doc.local_sql import execute_read_query


@logger.catch
@bot.message_handler(commands=['active_order'])
def order(message: Message) -> None:
    """
    Функция отправляет водителю активные заказы, информацию берет из таблицы orders
    :param message: объект Message из телеграма (сообщение пользователя)
    """
    query = f'''SELECT * FROM orders'''
    data = execute_read_query(query)
    if data:
        for act_order in data:
            bot.send_message(message.from_user.id,
                             f'{act_order[0]}. Время - {act_order[2]}\nмаршрут: {act_order[3]} -> {act_order[4]}')
    else:
        bot.send_message(message.from_user.id, 'Нет активных заказов')


if __name__ == "__main__":
    pass
