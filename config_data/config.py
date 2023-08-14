from os import getenv
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env')
else:
    load_dotenv()

BOT_TOKEN = getenv('BOT_TOKEN')
DEFAULT_COMMANDS = (
    ('order', "Заказать такси"),
    ('change', 'Внести изменения в заказ'),
    ('start', "Справка"),
    ('help', "Помощь"),
)

if __name__ == "__main__":
    pass