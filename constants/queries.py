"""Queries to DB"""

_DAILY_NOTIFICATIONS_TABLE = "daily_notifications"

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

TODAYS_HOLIDAYS_SQL_QUERY = HOLIDAYS_SQL_QUERY.format(
    where_condition=(
        "WHERE DAY(date_of_holiday) = DAY(CURRENT_DATE()) "
        "AND MONTH(date_of_holiday) = MONTH(CURRENT_DATE())"
    )
)

IS_EXISTS_DAILY_NOTIFICATIONS_QUERY = (
    f"SELECT EXISTS(SELECT * FROM {_DAILY_NOTIFICATIONS_TABLE} "
    "WHERE chat_id='{chat_id}')"
)

GET_DAILY_NOTIFICATIONS_CHATS_IDS_QUERY = (
    f"SELECT chat_id FROM {_DAILY_NOTIFICATIONS_TABLE}"
)

ADD_DAILY_NOTIFICATIONS_QUERY = (
    f"INSERT IGNORE INTO {_DAILY_NOTIFICATIONS_TABLE}(chat_id) "
    "VALUES('{chat_id}')"
)

DELETE_DAILY_NOTIFICATIONS_QUERY = (
    f"DELETE FROM {_DAILY_NOTIFICATIONS_TABLE} " "WHERE chat_id='{chat_id}'"
)
