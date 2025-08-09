from app.handlers.router import router
import datetime
import asyncio
import logging


from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram import F

from app.keyboards import inline as inline_keyboards
from app.keyboards import answer as answer_keyboards
from app.requests.get_cat_error import get_cat_error_async as get_cat_error
from app.requests.get_cocktail import get_cocktail_async as get_cocktail
from app.requests.get_cocktail import get_ingredients_list
from app.requests.get_joke import get_random_joke_async as get_random_joke
from app.requests.get_number_fact import get_random_number_fact_async as get_random_number_fact
from app.requests.get_cat_gif import get_random_cat_gif_async as get_random_cat_gif
from app.requests.get_dog_gif import get_random_dog_gif_async as get_random_dog_gif
from app.requests.get_activity import get_random_activity_async as get_random_activity
from app.states.states import Pomodoro


from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await message.reply("Привет! 👋")
    await message.answer("Я много что умею 👇", reply_markup=inline_keyboards.main)
    # Устанавливаем начальное состояние пользователя как Idle (бездействие)
    await state.set_state(Pomodoro.Idle)

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.reply(text="Этот бот просто учебный проект! Он может выполнять несколько интересных функций, связанных с отдыхом и продуктивностью\n\n\nОстались вопросы?\nПиши ему: \\@dianabol\\_metandienon\\_enjoyer", reply_markup=inline_keyboards.home, parse_mode='MarkdownV2')


@router.message(Command("contacts"))
async def cmd_contacts(message: Message):
    # Важно: для MarkdownV2 нужно экранировать специальные символы (\)
    text = "Связь с разрабом:\n\n\n\\@dianabol\\_metandienon\\_enjoyer\n\n\n[GitHub](https://github.com/Segun228)"
    await message.reply(text=text, reply_markup=inline_keyboards.home, parse_mode='MarkdownV2')


@router.callback_query(F.data == "productivity")
async def productivity_callback(callback:CallbackQuery):
    await callback.message.answer(
        text="Отлично! Самое время приступить к работе. Выбери необходимую функцию",
        reply_markup=inline_keyboards.productivity
    )
    await callback.answer() # Добавлено: Отвечаем на коллбек


@router.callback_query(F.data == "contacts")
async def contacts_callback(callback:CallbackQuery):
    # Важно: для MarkdownV2 нужно экранировать специальные символы (\)
    text = "Связь с разрабом:\n\n\n\\@dianabol\\_metandienon\\_enjoyer\n\n\n[GitHub](https://github.com/Segun228)"
    await callback.message.reply(text=text, reply_markup=inline_keyboards.home, parse_mode='MarkdownV2')
    await callback.answer() # Добавлено: Отвечаем на коллбек


@router.callback_query(F.data == "main_menu")
async def main_menu_callback(callback:CallbackQuery):
    await callback.message.answer("Я много что умею 👇", reply_markup=inline_keyboards.main)
    await callback.answer() # Уже было: Отвечаем на коллбек


# -------------------------------------------------------------
# Обработчики API (все вызовы теперь с await и добавлены callback.answer())
# -------------------------------------------------------------
@router.callback_query(F.data == "joke")
async def callback_joke(callback:CallbackQuery):
    joke = await get_random_joke() # <--- Асинхронный вызов
    if joke is None:
        await callback.message.answer(text="Не до шуток сейчас, иди работай!")
    else:
        await callback.message.reply(text=f"{joke}", reply_markup=inline_keyboards.joke)
    await callback.answer() # Добавлено: Отвечаем на коллбек

@router.callback_query(F.data == "number")
async def callback_number(callback:CallbackQuery):
    fact = await get_random_number_fact() # <--- Асинхронный вызов
    if fact is None:
        await callback.message.answer(text="Не до циферок, иди работай!")
    else:
        await callback.message.reply(text=f"{fact}", reply_markup=inline_keyboards.number)
    await callback.answer() # Добавлено: Отвечаем на коллбек


@router.callback_query(F.data == "todo")
async def callback_todo(callback:CallbackQuery):
    activity = await get_random_activity() # <--- Асинхронный вызов
    if activity is None:
        await callback.message.answer(text="Иди работай!")
    else:
        await callback.message.reply(text=f"{activity}", reply_markup=inline_keyboards.todo)
    await callback.answer() # Добавлено: Отвечаем на коллбек


@router.callback_query(F.data == "cat")
async def callback_cat(callback:CallbackQuery):
    cat_gif_url = await get_random_cat_gif() # <--- Асинхронный вызов (исправлен синтаксис)
    if cat_gif_url is None:
        await callback.message.answer(text="Не до котиков, иди работай!")
    else:
        await callback.bot.send_animation(
            chat_id=callback.message.chat.id,
            animation=cat_gif_url, # Используем 'animation' для GIF
            caption=f"Сегодня ты такой котик!",
            reply_markup=inline_keyboards.cat
        )
    await callback.answer() # Уже было: Отвечаем на коллбек


@router.callback_query(F.data == "dog")
async def callback_dog(callback:CallbackQuery):
    dog_gif_url = await get_random_dog_gif() # <--- Асинхронный вызов
    if dog_gif_url is None:
        await callback.message.answer(text="Не до собакенов, иди работай!")
    else:
        await callback.bot.send_animation(
            chat_id=callback.message.chat.id,
            animation=dog_gif_url, # Используем 'animation' для GIF
            caption="СОБАКЕН!",
            reply_markup=inline_keyboards.dog
        )
    await callback.answer() # Уже было: Отвечаем на коллбек

@router.callback_query(F.data == "cocktail")
async def get_cocktail_callback(callback:CallbackQuery):
    cocktail_data = await get_cocktail() # <--- Асинхронный вызов
    # Безопасная проверка: убеждаемся, что cocktail_data не None и содержит список 'drinks'
    if cocktail_data is None or not cocktail_data.get("drinks"):
        await callback.message.answer(text="Харош бухать, иди работай!")
    else:
        # Получаем первый коктейль из списка 'drinks'
        cocktail_info = cocktail_data["drinks"][0] # Теперь безопасно, т.к. список уже проверен
        
        # Безопасный доступ к данным, используя .get() с запасным значением
        cocktail_name = cocktail_info.get("strDrink", "Неизвестно")
        preparation = cocktail_info.get("strInstructions", "Инструкции отсутствуют.")
        ingredients_list = get_ingredients_list(cocktail_info=cocktail_info) # Эта функция синхронная и это нормально

        caption = f"""
            Вот ваш коктейль, Сэр! 🎉

            **Название:** {cocktail_name}

            **Ингредиенты:**
            {ingredients_list}

            **Приготовление:**
            {preparation}
            """
        
        await callback.bot.send_photo(
            chat_id=callback.message.chat.id,
            photo=cocktail_info.get("strDrinkThumb"),
            caption=caption,
            parse_mode='Markdown',
            reply_markup=inline_keyboards.cocktail
        )
    await callback.answer() # Добавлено: Отвечаем на коллбек

@router.callback_query(F.data == "rest")
async def rest_callback(callback:CallbackQuery):
    await callback.message.answer(
        text="Прекрасно! Самое время немного расслабиться. Выбери нужную функцию",
        reply_markup=inline_keyboards.rest
    )
    await callback.answer() # Добавлено: Отвечаем на коллбек


@router.callback_query(F.data == "productivity")
async def productivity_menu(callback:CallbackQuery, state: FSMContext):
    # При входе в меню продуктивности устанавливаем состояние Idle,
    # чтобы можно было запустить Pomodoro
    await state.set_state(Pomodoro.Idle)
    await callback.message.answer(
        text="Прекрасно! Самое время немного поработать! Что будем делать?",
        reply_markup=inline_keyboards.pomodoro_menu
    )
    await callback.answer() # Добавлено: Отвечаем на коллбек


# -------------------------------------------------------------
# Логика Pomodoro-таймера
# -------------------------------------------------------------
async def pomodoro_timer_worker(callback: CallbackQuery, state: FSMContext, duration: int):
    try:
        await callback.message.answer(f"Таймер запущен на {duration // 60} минут!")
        await asyncio.sleep(duration)
        
        # Получаем текущее состояние и счетчик после сна
        current_state = await state.get_state()
        user_data = await state.get_data()
        counter = user_data.get('counter', 0)

        # Логика переходов после завершения таймера
        if current_state == Pomodoro.Work:
            counter += 1
            await state.update_data(counter=counter) # Сохраняем обновленный счетчик
            
            if counter % 4 == 0:
                await state.set_state(Pomodoro.LongBreak)
                await callback.message.answer("Время длинного перерыва (15-30 минут)!")
            else:
                await state.set_state(Pomodoro.ShortBreak)
                await callback.message.answer("Время короткого перерыва (5 минут)!")
        
        elif current_state == Pomodoro.ShortBreak: # Если был короткий перерыв, возвращаемся к работе
            await state.set_state(Pomodoro.Work)
            await callback.message.answer("Перерыв окончен! Возвращаемся к работе.")
        
        elif current_state == Pomodoro.LongBreak: # После длинного перерыва возвращаемся в Idle, завершая цикл
            await state.set_state(Pomodoro.Idle)
            await callback.message.answer("Длинный перерыв окончен! Вы можете начать новый цикл.")
            
    except asyncio.CancelledError:
        # Это исключение сработает, если таймер был отменен извне (кнопкой "стоп")
        logging.info("Таймер отменен")
        await callback.message.answer("Таймер был остановлен.")
    except Exception as e:
        # Логируем любые другие неожиданные ошибки
        logging.error(f"Ошибка в таймере: {e}")
    finally:
        # Гарантируем, что задача таймера будет удалена из состояния,
        # чтобы избежать утечек и проблем с повторным запуском.
        # Проверяем, что задача не None, прежде чем пытаться обновить.
        user_data = await state.get_data()
        if user_data.get('task') is not None:
            await state.update_data(task=None)


@router.callback_query(F.data == "start", F.state.in_({Pomodoro.Idle, Pomodoro.ShortBreak, Pomodoro.LongBreak}))
async def start_pomodoro(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    
    # ... (код для отмены существующей задачи)

    duration = 0
    current_state = await state.get_state()

    # <--- ВОТ ЗДЕСЬ ОШИБКА!
    if current_state == Pomodoro.ShortBreak:
        duration = 5 * 60
        await state.set_state(Pomodoro.Work) # Ошибка: перерыв запускается, но состояние меняется на Work
    elif current_state == Pomodoro.LongBreak:
        duration = 20 * 60
        await state.set_state(Pomodoro.Work) # Ошибка: длинный перерыв запускается, но состояние меняется на Work
    else: # Pomodoro.Idle
        duration = 25 * 60
        await state.set_state(Pomodoro.Work) # Это правильно, для начала работы

    task = asyncio.create_task(pomodoro_timer_worker(callback, state, duration))
    await state.update_data(task=task)
    
    await callback.message.answer(f"Таймер запущен на {duration // 60} минут!")
    await callback.answer()


# -------------------------------------------------------------
# Обработчик всех остальных сообщений (должен быть в самом конце файла)
# -------------------------------------------------------------
@router.message()
async def all_other_messages(message: Message):
    await message.answer("Неизвестная команда 🧐")
    # message.bot всегда не None в обработчиках, проверять не нужно
    photo_data = await get_cat_error() # <--- Асинхронный вызов
    if photo_data: # Проверка на "truthy" значение
        photo_to_send = BufferedInputFile(photo_data, filename="cat_error.jpg")
        await message.bot.send_photo(chat_id=message.chat.id, photo= photo_to_send)