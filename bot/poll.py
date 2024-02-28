from aiogram import F
from aiogram import Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import types
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest
from database import db
from result_image import ResultImage
from io import BytesIO

router = Router()


class last_question(StatesGroup):
    view_quest = State()
    answered_quest = State()


def create_db_str(id: int):
    db[str(id)] = []


def update_db_str(callback):
    id = str(callback.from_user.id)
    ans = callback.data.split("_")[1]

    db[id].append(ans)


def get_db_str(id: int):
    return db.get(str(id), [])


async def start_polls(message: types.Message):
    create_db_str(message.from_user.id)

    await message.answer("""
    <b>Выберите утверждение, которое наиболее близко вам:</b>
    \t1. Я живу в удовольствие, никуда не тороплюсь
    \t2. Моя жизнь полна ярких красок, каждый день словно новая страница в жизни, я могу уехать куда хочу когда захочу
    \t3. Я ценю уют и комфорт, не гонюсь за деньгами и успехом, скорее, семья важнее всего для меня
    \t4. Я работаю для своего будущего, делаю успешную карьеру
    """, reply_markup=poll1())


async def update_poll(message: types.Message, text: str, keyboard=None):
    with suppress(TelegramBadRequest):
        await message.edit_text(
            f"{text}",
            reply_markup=keyboard
        )


@router.callback_query(F.data.startswith("var1_"))
async def callbacks_var1(callback: types.CallbackQuery):
    await update_poll(callback.message, """<b>Мой любимый цветок в парфюме: </b>
    \t1. Розы, пионы
    \t2. Лилии, иланг-иланг
    \t3. Жасмин, мята
    \t4. Не люблю цветы, скорее, что-то более ягодное
    """, poll2())

    await callback.answer()


@router.callback_query(F.data.startswith("var2_"))
async def callbacks_var2(callback: types.CallbackQuery):
    update_db_str(callback)

    await update_poll(callback.message, """<b>Какой десерт ты выберешь?</b>
    \t1. Булочка с корицей
    \t2. Чизкейк с соленой карамелью
    \t3. Лимонно-мятный сорбет
    \t4. Сигарету с кофе, пожалуйста!
    """, poll3())

    await callback.answer()


@router.callback_query(F.data.startswith("var3_"))
async def callbacks_var3(callback: types.CallbackQuery):
    update_db_str(callback)
    await update_poll(callback.message, """<b>Что тебе нравится в парфюмерии больше всего?</b>
    \t1. Стойкость и шлейфовость 
    \t2. Нежность и деликатность
    \t3. Свежесть, необычные ароматы 
    \t4. Тяжелые, древесные ароматы
    """, poll4())

    await callback.answer()


@router.callback_query(F.data.startswith("var4_"))
async def callbacks_var4(callback: types.CallbackQuery):
    update_db_str(callback)
    await update_poll(callback.message, """<b>Какое твоё любимое мороженое?</b>
    \t1. Фисташка
    \t2. Пломбир
    \t3. Шоколадное
    \t4. Фруктовый сорбет
    """, poll5())

    await callback.answer()


@router.callback_query(F.data.startswith("var5_"))
async def callbacks_var5(callback: types.CallbackQuery):
    update_db_str(callback)
    await update_poll(callback.message, """<b>Любимое время года?</b>
    \t1. Зима 
    \t2. Осень
    \t3. Лето
    \t4. Весна
    """, poll6())

    await callback.answer()


@router.callback_query(F.data.startswith("var6_"))
async def callbacks_var6(callback: types.CallbackQuery):
    await update_poll(callback.message, """<b>Где бы ты хотел находиться прямо сейчас?</b>
    \t1. Горы
    \t2. Море
    \t3. Город
    \t4. Деревня
    """, poll7())

    await callback.answer()


@router.callback_query(F.data.startswith("var7_"))
async def callbacks_var7(callback: types.CallbackQuery):
    update_db_str(callback)
    await update_poll(callback.message, """<b>Какую еду предпочитаешь?</b>
    \t1. Сладкую
    \t2. Соленую
    \t3. Острую
    \t4. Пряную
    """, poll8())

    await callback.answer()


@router.callback_query(F.data.startswith("var8_"))
async def callbacks_var8(callback: types.CallbackQuery):
    update_db_str(callback)
    await update_poll(callback.message, """<b>Кто ты по психотипу?</b>
    \t1. Холерик
    \t2. Сангвиник
    \t3. Флегматик
    \t4. Меланхолик""", poll9())

    await callback.answer()


@router.callback_query(F.data.startswith("var9_"))
async def callbacks_var9(callback: types.CallbackQuery):
    await update_poll(callback.message, """<b>Какие цвета тебе нравятся больше?</b>
    \t1. Яркие
    \t2. Темные
    \t3. Приглушенные
    \t4. Пастельные
    """, poll10())

    await callback.answer()


@router.callback_query(F.data.startswith("var10_"))
async def callbacks_var10(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(last_question.view_quest)
    await update_poll(callback.message, "<b>Как вы назовете свой аромат? (до 20 символов)</b>")

    await callback.answer()


@router.message(last_question.view_quest)
async def answer(message: types.Message, state: FSMContext):
    if len(str(message.text)) > 20:
        await message.answer("Пожалуйста, укажите название длинной не более 20 символов")
        return

    result = get_db_str(message.from_user.id)
    result.append(message.text)

    bio = BytesIO()
    bio.name = 'result.jpeg'

    img = ResultImage.result_image(result)

    img.save(bio, "JPEG")
    bio.seek(0)

    await message.answer_photo(photo=types.BufferedInputFile(bio.getvalue(), "result.jpeg"),
                               caption="Спасибо за прохождение теста! Вот результат:")

    await state.set_state(last_question.answered_quest)


def poll1():
    buttons = [
        [
            types.InlineKeyboardButton(
                text="1", callback_data="var1_"),
            types.InlineKeyboardButton(
                text="2", callback_data="var1_")
        ],
        [
            types.InlineKeyboardButton(
                text="3", callback_data="var1_"),
            types.InlineKeyboardButton(
                text="4", callback_data="var1_")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def poll2():
    buttons = [
        [
            types.InlineKeyboardButton(
                text="1", callback_data="var2_rose"),
            types.InlineKeyboardButton(
                text="2", callback_data="var2_lily")
        ],
        [
            types.InlineKeyboardButton(
                text="3", callback_data="var2_jasmine"),
            types.InlineKeyboardButton(
                text="4", callback_data="var2_berry")
        ]
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def poll3():
    buttons = [
        [
            types.InlineKeyboardButton(
                text="1", callback_data="var3_cinnamon"),
            types.InlineKeyboardButton(
                text="2", callback_data="var3_caramel")
        ],
        [
            types.InlineKeyboardButton(
                text="3", callback_data="var3_lemon"),
            types.InlineKeyboardButton(
                text="4", callback_data="var3_cigarette")
        ]
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def poll4():
    buttons = [
        [
            types.InlineKeyboardButton(
                text="1", callback_data="var4_cognac"),
            types.InlineKeyboardButton(
                text="2", callback_data="var4_powder")
        ],
        [
            types.InlineKeyboardButton(
                text="3", callback_data="var4_citrus"),
            types.InlineKeyboardButton(
                text="4", callback_data="var4_tree")
        ]
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def poll5():
    buttons = [
        [
            types.InlineKeyboardButton(
                text="1", callback_data="var5_pistachios"),
            types.InlineKeyboardButton(
                text="2", callback_data="var5_vanilla")
        ],
        [
            types.InlineKeyboardButton(
                text="3", callback_data="var5_chocolate"),
            types.InlineKeyboardButton(
                text="4", callback_data="var5_mango")
        ]
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def poll6():
    buttons = [
        [
            types.InlineKeyboardButton(
                text="1", callback_data="var6_"),
            types.InlineKeyboardButton(
                text="2", callback_data="var6_")
        ],
        [
            types.InlineKeyboardButton(
                text="3", callback_data="var6_"),
            types.InlineKeyboardButton(
                text="4", callback_data="var6_")
        ]
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def poll7():
    buttons = [
        [
            types.InlineKeyboardButton(
                text="1", callback_data="var7_wind"),
            types.InlineKeyboardButton(
                text="2", callback_data="var7_breeze")
        ],
        [
            types.InlineKeyboardButton(
                text="3", callback_data="var7_bedsheets"),
            types.InlineKeyboardButton(
                text="4", callback_data="var7_meadow")
        ]
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def poll8():
    buttons = [
        [
            types.InlineKeyboardButton(
                text="1", callback_data="var8_sugar"),
            types.InlineKeyboardButton(
                text="2", callback_data="var8_sault")
        ],
        [
            types.InlineKeyboardButton(
                text="3", callback_data="var8_pepper"),
            types.InlineKeyboardButton(
                text="4", callback_data="var8_spices")
        ]
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def poll9():
    buttons = [
        [
            types.InlineKeyboardButton(
                text="1", callback_data="var9_"),
            types.InlineKeyboardButton(
                text="2", callback_data="var9_")
        ],
        [
            types.InlineKeyboardButton(
                text="3", callback_data="var9_"),
            types.InlineKeyboardButton(
                text="4", callback_data="var9_")
        ]
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def poll10():
    buttons = [
        [
            types.InlineKeyboardButton(
                text="1", callback_data="var10_"),
            types.InlineKeyboardButton(
                text="2", callback_data="var10_")
        ],
        [
            types.InlineKeyboardButton(
                text="3", callback_data="var10_"),
            types.InlineKeyboardButton(
                text="4", callback_data="var10_")
        ]
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
