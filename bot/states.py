from aiogram.fsm.state import StatesGroup, State

class TripState(StatesGroup):
    city = State()
    excursion = State()
    point_index = State()
    