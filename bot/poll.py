from aiogram import F
from aiogram import Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import types
from aiogram.exceptions import TelegramBadRequest

from contextlib import suppress
from io import BytesIO

from tele_test import QUESTION_COUNT, test
from database import Database
from result_image import ResultImage


router = Router()
database = Database()

def reply_keyboard():
    kb = [
        [
            types.KeyboardButton(text="Пройти тест"),
            types.KeyboardButton(text="Заказать аромат")
        ],
    ]
    return types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder="Выберите действие",
    )

class last_question(StatesGroup):
    view_quest = State()


async def start_test(message: types.Message):
    database.create_db_str(message.from_user.id, message.from_user.username)

    await set_question(0, message=message, first=True)


def form_buttons(q_num: int, ingredients: list[str]):
    button = lambda i : types.InlineKeyboardButton(text=str(i),
                                                   callback_data=f"answer_{q_num}_{ingredients[i-1] if ingredients else ''}")

    back_button = [ types.InlineKeyboardButton(text="Назад ↩", callback_data=f"answer_{q_num}_!") ]

    buttons = [ [button(i), button(i+1)] for i in range(1, 5, 2) ]

    if q_num:
        buttons.append(back_button)

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


async def set_question(num: int, message: types.Message, state = None, first: bool = False):
    q = test[num]
    text = f"{num+1}/{QUESTION_COUNT}\n\n<b>{q['title']}</b>"

    if "options" in q:
        options = q["options"]

        for i in range(len(options)):
            text += f'\n\t {i+1}. {options[i]}'

    ingredients = q["ingredients"]

    if q["type"] == "open":
        await state.set_state(last_question.view_quest)
        await message.edit_text(text)
        return

    buttons = form_buttons(num, ingredients)

    if not first:
        with suppress(TelegramBadRequest):
            await message.edit_text(text, reply_markup=buttons)
    else:
        await message.answer(text, reply_markup=buttons)
        

@router.callback_query(F.data.startswith("answer"))
async def test_routing(callback: types.CallbackQuery, state: FSMContext):
    _, num, ingredient = callback.data.split("_")
    num = int(num)

    if ingredient == '!':
        await state.clear()
        await set_question(num - 1, callback.message, state=state)
        return

    if ingredient:
        database.update_db_question_array(callback.from_user.id, num, ingredient)

    await set_question(num + 1, callback.message, state=state)


@router.message(last_question.view_quest)
async def answer(message: types.Message, state: FSMContext):
    if len(str(message.text)) > 20:
        await message.answer("Пожалуйста, укажите название длинной не более 20 символов")
        return

    result = list(filter(None, database.get_db_question_array_after_complete(message.from_user.id)))
    result.append(message.text)

    bio = BytesIO()
    bio.name = 'result.jpeg'

    img = ResultImage.result_image(result)

    img.save(bio, "JPEG")
    bio.seek(0)

    await message.answer_photo(photo=types.BufferedInputFile(bio.getvalue(), "result.jpeg"),
                               caption="Спасибо за прохождение теста! Заказать аромат вы можете по цене 1200 рублей, переслав данное сообщение @oooobnulai", reply_markup=reply_keyboard())

    await state.clear()

