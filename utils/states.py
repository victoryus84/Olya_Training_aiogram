from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    BEGIN = State()
    LANGUAGE = State()
    UNIVERSITY = State()
    COURSE = State()
    CHOISE = State()