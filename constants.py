"""Constants of the project"""

from decouple import config
from mysql.connector import connect

TOKEN = config("TOKEN")

BOT_COMMANDS = [
    {"command": "start", "description": "Запуск бота"},
    {"command": "help", "description": "Подсказки"},
    {"command": "all_holidays", "description": "Все праздники"},
]

ALL_HOLIDAYS_SQL_QUERY = """
SELECT date_of_holiday, title, is_birthday, whom_to_congratulate
FROM holidays
ORDER BY MONTH(date_of_holiday), DAY(date_of_holiday);
"""

DB_CONNECT = connect(
    host=config("DB_HOST"),
    user=config("DB_USER"),
    password=config("DB_PASSWORD"),
    database=config("DB_NAME"),
)

ERROR_MESSAGE = (
    "Я ошибся. Я могу один раз ошибиться?\n"
    "Я великий грешник и у всех прошу прощения 🙏"
)
