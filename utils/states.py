from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    BEGIN = State()
    LANGUAGES = State()
    UNIVERSITIES = State()
    COURSES = State()
    