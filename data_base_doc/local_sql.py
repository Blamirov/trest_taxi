from loguru import logger
import sqlite3 as sq


@logger.catch()
def creation_db() -> None:
    """Функция для создания базы данных если ее еще нет на компьютере."""
    with sq.connect("orders.db") as con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT ,
        tg_user_id INTEGER NOT NULL,
        time TEXT NOT NULL,
        pickup TEXT NOT NULL,
        destination TEXT NOT NULL,
        tg_driver_id INTEGER NOT NULL,
        username TEXT,
        order_time DATA,
        comment TEXT,
        name TEXT 
        )
        """)
        cur.execute("""CREATE TABLE IF NOT EXISTS driver (
                driver_id INTEGER NOT NULL
                )
                """)
        con.commit()
        logger.info('База данных подключена')


@logger.catch
def execute_query(insert_query: str, query_data: list) -> None:
    """
         Функция передает запрос на внесение данных в таблицу
         :param insert_query: запрос по форме SQL
         :param query_data: необходимая информация
    """
    try:
        with sq.connect("orders.db") as connection:
            cursor = connection.cursor()
            cursor.execute(insert_query, query_data)
            connection.commit()
    except BaseException as e1:
        logger.error(e1)


@logger.catch
def execute_read_query(query: str) -> (None, str):
    """
        Функция для получения данных из таблицы
        :param query: запрос по форме SQL
    """
    try:
        with sq.connect("orders.db") as connection:
            cursor_rq = connection.cursor()
            cursor_rq.execute(query)
            result = cursor_rq.fetchall()
            return result
    except BaseException as e2:
        logger.error(e2)


@logger.catch
def insert_query_data(data) -> None:
    """
    Функция для внесения данных в sql таблицу
    :param data - объект data который получается из телеграма
    """
    values = [data['passenger_id'], data['service_time'], data['pickup_point'],
              data['destination_point'], data['tg_driver_id'], data['username'], data['order_time'], data['comment'],
              data['name']]
    query = """INSERT INTO orders(tg_user_id, time, pickup, destination, 
                tg_driver_id, username, order_time, comment, name)
                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    execute_query(query, values)


if __name__ == '__main__':
    pass
