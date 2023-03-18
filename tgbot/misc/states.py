from aiogram.dispatcher.filters.state import StatesGroup, State


class GetPhone(StatesGroup):
    phone_number = State()