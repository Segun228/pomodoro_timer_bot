from app.handlers.router import router
import asyncio
import logging
from aiogram.types import Message, CallbackQuery, BufferedInputFile
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram import F
from aiogram.fsm.context import FSMContext
from app.keyboards import inline as inline_keyboards
from app.states.states import Pomodoro
from app.requests.get_cat_error import get_cat_error_async as get_cat_error
from app.requests.get_cocktail import get_cocktail_async as get_cocktail, get_ingredients_list
from app.requests.get_joke import get_random_joke_async as get_random_joke
from app.requests.get_number_fact import get_random_number_fact_async as get_random_number_fact
from app.requests.get_cat_gif import get_random_cat_gif_async as get_random_cat_gif
from app.requests.get_dog_gif import get_random_dog_gif_async as get_random_dog_gif
from app.requests.get_activity import get_random_activity_async as get_random_activity

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(Pomodoro.Idle)
    await message.reply("Привет! 👋")
    await message.answer("Я много что умею 👇", reply_markup=inline_keyboards.main)

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.reply(text="Этот бот — учебный проект! 📚 Он может выполнять несколько интересных функций, связанных с отдыхом и продуктивностью. Если остались вопросы, пиши ему: \\@dianabol\\_metandienon\\_enjoyer ❓", reply_markup=inline_keyboards.home, parse_mode='MarkdownV2')

@router.message(Command("contacts"))
async def cmd_contacts(message: Message):
    text = "Связь с разрабом: 📞\n\n\\@dianabol\\_metandienon\\_enjoyer 🤝\n\n[GitHub](https://github.com/Segun228)"
    await message.reply(text=text, reply_markup=inline_keyboards.home, parse_mode='MarkdownV2')

@router.callback_query(F.data == "productivity")
async def productivity_callback(callback:CallbackQuery, state: FSMContext):
    await state.set_state(Pomodoro.Idle)
    await callback.message.edit_text(
        text="Отлично! 💪 Самое время приступить к работе. Выбери необходимую функцию 👇",
        reply_markup=inline_keyboards.pomodoro_menu
    )
    await callback.answer()

@router.callback_query(F.data == "contacts")
async def contacts_callback(callback:CallbackQuery):
    text = "Связь с разрабом: 📞\n\n\\@dianabol\\_metandienon\\_enjoyer 🤝\n\n[GitHub](https://github.com/Segun228)"
    await callback.message.edit_text(text=text, reply_markup=inline_keyboards.home, parse_mode='MarkdownV2')
    await callback.answer()

@router.callback_query(F.data == "main_menu")
async def main_menu_callback(callback:CallbackQuery):
    await callback.message.edit_text("Я много что умею 👇", reply_markup=inline_keyboards.main)
    await callback.answer()

@router.callback_query(F.data == "joke")
async def callback_joke(callback:CallbackQuery):
    joke = await get_random_joke() 
    if joke is None:
        await callback.message.answer(text="Не до шуток сейчас, иди работай! 😠")
    else:
        await callback.message.reply(text=f"{joke} 😂", reply_markup=inline_keyboards.joke)
    await callback.answer()

@router.callback_query(F.data == "number")
async def callback_number(callback:CallbackQuery):
    fact = await get_random_number_fact()
    if fact is None:
        await callback.message.answer(text="Не до циферок, иди работай! 🔢")
    else:
        await callback.message.reply(text=f"{fact}", reply_markup=inline_keyboards.number)
    await callback.answer() 

@router.callback_query(F.data == "todo")
async def callback_todo(callback:CallbackQuery):
    activity = await get_random_activity()
    if activity is None:
        await callback.message.answer(text="Иди работай! 💼")
    else:
        await callback.message.reply(text=f"{activity} ✅", reply_markup=inline_keyboards.todo)
    await callback.answer() 

@router.callback_query(F.data == "cat")
async def callback_cat(callback:CallbackQuery):
    cat_gif_url = await get_random_cat_gif()
    if cat_gif_url is None:
        await callback.message.answer(text="Не до котиков, иди работай! 😼")
    else:
        await callback.bot.send_animation(
            chat_id=callback.message.chat.id,
            animation=cat_gif_url,
            caption="Сегодня ты такой котик! 🐈",
            reply_markup=inline_keyboards.cat
        )
    await callback.answer()

@router.callback_query(F.data == "dog")
async def callback_dog(callback:CallbackQuery):
    dog_gif_url = await get_random_dog_gif()
    if dog_gif_url is None:
        await callback.message.answer(text="Не до собакенов, иди работай! 🐶")
    else:
        await callback.bot.send_animation(
            chat_id=callback.message.chat.id,
            animation=dog_gif_url,
            caption="СОБАКЕН! 🐕",
            reply_markup=inline_keyboards.dog
        )
    await callback.answer()

@router.callback_query(F.data == "cocktail")
async def get_cocktail_callback(callback:CallbackQuery):
    cocktail_data = await get_cocktail()
    if cocktail_data is None or not cocktail_data.get("drinks"):
        await callback.message.answer(text="Харош бухать, иди работай! 🍻")
    else:
        cocktail_info = cocktail_data["drinks"][0]
        cocktail_name = cocktail_info.get("strDrink", "Неизвестно")
        preparation = cocktail_info.get("strInstructions", "Инструкции отсутствуют.")
        ingredients_list = get_ingredients_list(cocktail_info=cocktail_info)
        caption = f"Вот ваш коктейль, Сэр! 🎉\n\n**Название:** {cocktail_name}\n\n**Ингредиенты:**\n{ingredients_list}\n\n**Приготовление:**\n{preparation}"
        await callback.bot.send_photo(
            chat_id=callback.message.chat.id,
            photo=cocktail_info.get("strDrinkThumb"),
            caption=caption,
            parse_mode='Markdown',
            reply_markup=inline_keyboards.cocktail
        )
    await callback.answer()

@router.callback_query(F.data == "rest")
async def rest_callback(callback:CallbackQuery):
    await callback.message.edit_text(
        text="Прекрасно! 🏖️ Самое время немного расслабиться. Выбери нужную функцию 👇",
        reply_markup=inline_keyboards.rest
    )
    await callback.answer()

async def pomodoro_timer_worker(callback: CallbackQuery, state: FSMContext, duration: int):
    try:
        await asyncio.sleep(duration)
        current_state = await state.get_state()
        user_data = await state.get_data()
        counter = user_data.get('counter', 0)
        if current_state == Pomodoro.Work:
            counter += 1
            await state.update_data(counter=counter)
            if counter % 4 == 0:
                await state.set_state(Pomodoro.LongBreak)
                await callback.message.edit_text(f"Время длинного перерыва (20 минут)! ☕️", reply_markup=inline_keyboards.pomodoro_menu)
            else:
                await state.set_state(Pomodoro.ShortBreak)
                await callback.message.edit_text(f"Время короткого перерыва (5 минут)! 🍎", reply_markup=inline_keyboards.pomodoro_menu)
        elif current_state == Pomodoro.ShortBreak:
            await state.set_state(Pomodoro.Work)
            await callback.message.edit_text("Перерыв окончен! Возвращаемся к работе. 📚", reply_markup=inline_keyboards.pomodoro_menu)
        elif current_state == Pomodoro.LongBreak:
            await state.set_state(Pomodoro.Idle)
            await callback.message.edit_text("Длинный перерыв окончен! Вы можете начать новый цикл. 🎉", reply_markup=inline_keyboards.pomodoro_menu)
    except asyncio.CancelledError:
        logging.info("Таймер отменен")
    except Exception as e:
        logging.error(f"Ошибка в таймере: {e}")
    finally:
        user_data = await state.get_data()
        if user_data.get('task') is not None:
            await state.update_data(task=None)

@router.callback_query(F.data == "stop")
async def stop_pomodoro(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    task = user_data.get('task')
    if task:
        if not task.done():
            task.cancel()
        await state.update_data(task=None, counter=0)
        await state.set_state(Pomodoro.Idle)
        await callback.message.edit_text(
            text="Таймер остановлен. 🛑⏸️",
            reply_markup=inline_keyboards.pomodoro_menu
        )
    else:
        await callback.message.edit_text("Таймер не был запущен. 🤔", reply_markup=inline_keyboards.pomodoro_menu)
    await callback.answer()

@router.callback_query(F.data == "start", StateFilter(Pomodoro.Idle, Pomodoro.ShortBreak, Pomodoro.LongBreak))
async def start_pomodoro(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    existing_task = user_data.get('task')
    if existing_task and not existing_task.done():
        existing_task.cancel()
        await state.update_data(task=None)
    duration = 0
    current_state = await state.get_state()
    if current_state == Pomodoro.ShortBreak:
        duration = 5 * 60
    elif current_state == Pomodoro.LongBreak:
        duration = 20 * 60
    else:
        duration = 25 * 60
        await state.set_state(Pomodoro.Work)
    task = asyncio.create_task(pomodoro_timer_worker(callback, state, duration))
    await state.update_data(task=task)
    if current_state == Pomodoro.Idle:
        await callback.message.edit_text(f"Таймер запущен: работа на {duration // 60} минут! ⌚", reply_markup=inline_keyboards.stop)
    elif current_state == Pomodoro.ShortBreak:
        await callback.message.edit_text(f"Таймер запущен: короткий перерыв на {duration // 60} минут! ☕️", reply_markup=inline_keyboards.stop)
    elif current_state == Pomodoro.LongBreak:
        await callback.message.edit_text(f"Таймер запущен: длинный перерыв на {duration // 60} минут! 🛋️", reply_markup=inline_keyboards.stop)
    await callback.answer()

@router.message()
async def all_other_messages(message: Message):
    await message.answer("Неизвестная команда 🧐")
    photo_data = await get_cat_error()
    if photo_data:
        photo_to_send = BufferedInputFile(photo_data, filename="cat_error.jpg")
        await message.bot.send_photo(chat_id=message.chat.id, photo=photo_to_send)