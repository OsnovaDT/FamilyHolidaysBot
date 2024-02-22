"""Constants of the project"""

from decouple import config
from mysql.connector import connect

TOKEN = config("TOKEN")

BOT_COMMANDS = [
    {
        "command": "start",
        "description": "Перезапуск бота (может помочь если что-то сломалось)",
    },
    {"command": "help", "description": "Помощь с командами"},
    {"command": "all_holidays", "description": "Все праздники"},
    {
        "command": "this_month_holidays",
        "description": "Праздники в этом месяце",
    },
    {
        "command": "next_month_holidays",
        "description": "Праздники в следующем месяце",
    },
]

HOLIDAYS_SQL_QUERY = """
SELECT date_of_holiday, title, is_birthday, whom_to_congratulate
FROM holidays
{where_condition}
ORDER BY MONTH(date_of_holiday), DAY(date_of_holiday);
"""

ALL_HOLIDAYS_SQL_QUERY = HOLIDAYS_SQL_QUERY.format(where_condition="")

THIS_MONTH_HOLIDAYS_SQL_QUERY = HOLIDAYS_SQL_QUERY.format(
    where_condition="WHERE MONTH(date_of_holiday) = MONTH(CURRENT_DATE())"
)

NEXT_MONTH_HOLIDAYS_SQL_QUERY = HOLIDAYS_SQL_QUERY.format(
    where_condition="WHERE MONTH(date_of_holiday) = MONTH(CURRENT_DATE()"
    " + INTERVAL 1 MONTH)"
)

SPECIFIED_MONTH_HOLIDAYS_SQL_QUERY = HOLIDAYS_SQL_QUERY.format(
    where_condition="WHERE MONTH(date_of_holiday) = {month}"
)

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

WINTER_MONTHS = ["Декабрь ❄️", "Январь ❄️", "Февраль ❄️"]
SPRING_MONTHS = ["Март 🌷", "Апрель 🌷", "Май 🌷"]
SUMMER_MONTHS = ["Июнь ☀️", "Июль ☀️", "Август ☀️"]
AUTUMN_MONTHS = ["Сентябрь ☔", "Октябрь ☔", "Ноябрь ☔"]

MONTHS_NUMBERS = {
    WINTER_MONTHS[0]: 12,
    WINTER_MONTHS[1]: 1,
    WINTER_MONTHS[2]: 2,
    SPRING_MONTHS[0]: 3,
    SPRING_MONTHS[1]: 4,
    SPRING_MONTHS[2]: 5,
    SUMMER_MONTHS[0]: 6,
    SUMMER_MONTHS[1]: 7,
    SUMMER_MONTHS[2]: 8,
    AUTUMN_MONTHS[0]: 9,
    AUTUMN_MONTHS[1]: 10,
    AUTUMN_MONTHS[2]: 11,
}

ALL_MONTHS = WINTER_MONTHS + SPRING_MONTHS + SUMMER_MONTHS + AUTUMN_MONTHS
