from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


main = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📈 Продуктивность", callback_data="productivity")],
        [InlineKeyboardButton(text="😌 Отдых", callback_data="rest")],
        [InlineKeyboardButton(text="📞 Контакты", callback_data="contacts")]
    ]
)


home = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")],
    ]
)


productivity = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="⏳ Pomodoro timer", callback_data="start")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")],
    ]
)


rest = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🍹 Рецепт коктейля", callback_data="cocktail")],
        [InlineKeyboardButton(text="😂 Случайная шутка", callback_data="joke")],
        [InlineKeyboardButton(text="🔢 Интересное число", callback_data="number")],
        [InlineKeyboardButton(text="🐱 Какой ты котик?", callback_data="cat")],
        [InlineKeyboardButton(text="🐶 Собакен", callback_data="dog")],
        [InlineKeyboardButton(text="🎯 Что бы поделать?", callback_data="todo")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")],
    ]
)


cocktail = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🍹 Еще коктейль!", callback_data="cocktail")],
        [InlineKeyboardButton(text="🎉 К развлечениям!", callback_data="rest")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")],
    ]
)


joke = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="😂 Еще шутку!", callback_data="joke")],
        [InlineKeyboardButton(text="🎉 К развлечениям!", callback_data="rest")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")],
    ]
)


number = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔢 Еще факт!", callback_data="number")],
        [InlineKeyboardButton(text="🎉 К развлечениям!", callback_data="rest")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")],
    ]
) 


cat = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🐱 Давай еще!", callback_data="cat")],
        [InlineKeyboardButton(text="🎉 К развлечениям!", callback_data="rest")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")],
    ]
) 


dog = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🐶 Давай еще!", callback_data="dog")],
        [InlineKeyboardButton(text="🎉 К развлечениям!", callback_data="rest")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")],
    ]
)


todo = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🎯 Хочу что-то другое!", callback_data="todo")],
        [InlineKeyboardButton(text="🎉 К развлечениям!", callback_data="rest")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")],
    ]
)


pomodoro_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="▶️ Стартовать таймер!", callback_data="start")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")],
    ]
)


stop_menu = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="▶️ Стартовать таймер!", callback_data="start")],
        [InlineKeyboardButton(text="📈 Продуктивность", callback_data="pomodoro_menu")],
        [InlineKeyboardButton(text="🏠 Главное меню", callback_data="main_menu")],
    ]
)

stop = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="⏹ Остановить", callback_data="stop")],
    ]
)