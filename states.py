"""States for FSM"""

from aiogram.fsm.state import State, StatesGroup


class MonthStates(StatesGroup):
    """States for months"""

    choosing_month = State()
