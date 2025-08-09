from aiogram.fsm.state import StatesGroup, State



class Pomodoro(StatesGroup):
    Idle = State()
    ShortBreak = State()
    LongBreak = State()
    Work = State()