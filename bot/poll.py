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
    \t1) Я живу в удовольствие, никуда не тороплюсь
    \t2) Моя жизнь полна ярких красок, каждый день словно новая страница в жизни, я могу уехать куда хочу когда захочу
    \t3) Я ценю уют и комфорт, не гонюсь за деньгами и успехом, скорее, семья важнее всего для меня
    \t4) Я работаю для своего будущего, делаю успешную карьеру
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
    \tРозы, пионы
    \tЛилии, иланг-иланг
    \tЖасмин, мята
    \tНе люблю цветы, скорее, что-то более ягодное
    """, poll2())

    await callback.answer()


@router.callback_query(F.data.startswith("var2_"))
async def callbacks_var2(callback: types.CallbackQuery):
    update_db_str(callback)

    await update_poll(callback.message, """<b>Какой десерт ты выберешь?</b>
    \tБулочка с корицей
    \tЧизкейк с соленой карамелью
    \tЛимонно-мятный сорбет
    \tСигарету с кофе, пожалуйста!
    """, poll3())

    await callback.answer()


@router.callback_query(F.data.startswith("var3_"))
async def callbacks_var3(callback: types.CallbackQuery):
    update_db_str(callback)
    await update_poll(callback.message, """<b>Что тебе нравится в парфюмерии больше всего?</b>
    \tСтойкость и шлейфовость 
    \tНежность и деликатность
    \tСвежесть, необычные ароматы 
    \tТяжелые, древесные ароматы
    """, poll4())

    await callback.answer()


@router.callback_query(F.data.startswith("var4_"))
async def callbacks_var4(callback: types.CallbackQuery):
    update_db_str(callback)
    await update_poll(callback.message, """<b>Какое твоё любимое мороженое?</b>
    \tФисташка
    \tПломбир
    \tШоколадное
    \tФруктовый сорбет
    """, poll5())

    await callback.answer()


@router.callback_query(F.data.startswith("var5_"))
async def callbacks_var5(callback: types.CallbackQuery):
    update_db_str(callback)
    await update_poll(callback.message, """<b>Любимое время года?</b>
    \tЗима 
    \tОсень
    \tЛето
    \tВесна
    """, poll6())

    await callback.answer()


@router.callback_query(F.data.startswith("var6_"))
async def callbacks_var6(callback: types.CallbackQuery):
    await update_poll(callback.message, """<b>Где бы ты хотел находиться прямо сейчас?</b>
    \tГоры
    \tМоре
    \tГород
    \tДеревня
    """, poll7())

    await callback.answer()


@router.callback_query(F.data.startswith("var7_"))
async def callbacks_var7(callback: types.CallbackQuery):
    update_db_str(callback)
    await update_poll(callback.message, """<b>Какую еду предпочитаешь?</b>
    \tСладкую
    \tСоленую
    \tОструю
    \tПряную
    """, poll8())

    await callback.answer()


@router.callback_query(F.data.startswith("var8_"))
async def callbacks_var8(callback: types.CallbackQuery):
    update_db_str(callback)
    await update_poll(callback.message, """<b>Кто ты по психотипу?</b>
    \tХолерик
    \tСангвиник
    \tФлегматик
    \tМеланхолик
    """, poll9())

    await callback.answer()


@router.callback_query(F.data.startswith("var9_"))
async def callbacks_var9(callback: types.CallbackQuery):
    await update_poll(callback.message, """<b>Какие цвета тебе нравятся больше?</b>
    \tЯркие
    \tТемные
    \tПриглушенные
    \tПастельные
    """, poll10())

    await callback.answer()


@router.callback_query(F.data.startswith("var10_"))
async def callbacks_var10(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(last_question.view_quest)
    await update_poll(callback.message, "<b>Как вы назовете свой аромат? (до 20 символов)</b>")

    await callback.answer()


@router.message(last_question.view_quest)
async def answer(message: types.Message, state: FSMContext):
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
                text="1)", callback_data="var1_"),
            types.InlineKeyboardButton(
                text="2)", callback_data="var1_")
        ],
        [
            types.InlineKeyboardButton(
                text="3)", callback_data="var1_"),
            types.InlineKeyboardButton(
                text="4)", callback_data="var1_")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def poll2():
    buttons = [
        [
            types.InlineKeyboardButton(
                text="Розы, пионы", callback_data="var2_rose"),
            types.InlineKeyboardButton(
                text="Лилии, иланг-иланг", callback_data="var2_lily")
        ],
        [
            types.InlineKeyboardButton(
                text="Жасмин, мята", callback_data="var2_jasmine"),
            types.InlineKeyboardButton(
                text="🍓", callback_data="var2_berry")
        ]
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def poll3():
    buttons = [
        [
            types.InlineKeyboardButton(
                text="Булочка с корицей", callback_data="var3_cinnamon"),
            types.InlineKeyboardButton(
                text="Чизкейк с соленой карамелью", callback_data="var3_caramel")
        ],
        [
            types.InlineKeyboardButton(
                text="Лимонно-мятный сорбет", callback_data="var3_lemon"),
            types.InlineKeyboardButton(
                text="Сигарету с кофе, пожалуйста!", callback_data="var3_cigarette")
        ]
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def poll4():
    buttons = [
        [
            types.InlineKeyboardButton(
                text="вариант 1", callback_data="var4_cognac"),
            types.InlineKeyboardButton(
                text="вариант 2", callback_data="var4_powder")
        ],
        [
            types.InlineKeyboardButton(
                text="вариант 3", callback_data="var4_citrus"),
            types.InlineKeyboardButton(
                text="вариант 4", callback_data="var4_tree")
        ]
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def poll5():
    buttons = [
        [
            types.InlineKeyboardButton(
                text="вариант 1", callback_data="var5_pistachios"),
            types.InlineKeyboardButton(
                text="вариант 2", callback_data="var5_vanilla")
        ],
        [
            types.InlineKeyboardButton(
                text="вариант 3", callback_data="var5_chocolate"),
            types.InlineKeyboardButton(
                text="вариант 4", callback_data="var5_mango")
        ]
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def poll6():
    buttons = [
        [
            types.InlineKeyboardButton(
                text="вариант 1", callback_data="var6_"),
            types.InlineKeyboardButton(
                text="вариант 2", callback_data="var6_")
        ],
        [
            types.InlineKeyboardButton(
                text="вариант 3", callback_data="var6_"),
            types.InlineKeyboardButton(
                text="вариант 4", callback_data="var6_")
        ]
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def poll7():
    buttons = [
        [
            types.InlineKeyboardButton(
                text="вариант 1", callback_data="var7_wind"),
            types.InlineKeyboardButton(
                text="вариант 2", callback_data="var7_breeze")
        ],
        [
            types.InlineKeyboardButton(
                text="вариант 3", callback_data="var7_bedsheets"),
            types.InlineKeyboardButton(
                text="вариант 4", callback_data="var7_meadow")
        ]
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def poll8():
    buttons = [
        [
            types.InlineKeyboardButton(
                text="вариант 1", callback_data="var8_sugar"),
            types.InlineKeyboardButton(
                text="вариант 2", callback_data="var8_sault")
        ],
        [
            types.InlineKeyboardButton(
                text="вариант 3", callback_data="var8_pepper"),
            types.InlineKeyboardButton(
                text="вариант 4", callback_data="var8_spices")
        ]
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def poll9():
    buttons = [
        [
            types.InlineKeyboardButton(
                text="вариант 1", callback_data="var9_"),
            types.InlineKeyboardButton(
                text="вариант 2", callback_data="var9_")
        ],
        [
            types.InlineKeyboardButton(
                text="вариант 3", callback_data="var9_"),
            types.InlineKeyboardButton(
                text="вариант 4", callback_data="var9_")
        ]
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def poll10():
    buttons = [
        [
            types.InlineKeyboardButton(
                text="вариант 1", callback_data="var10_"),
            types.InlineKeyboardButton(
                text="вариант 2", callback_data="var10_")
        ],
        [
            types.InlineKeyboardButton(
                text="вариант 3", callback_data="var10_"),
            types.InlineKeyboardButton(
                text="вариант 4", callback_data="var10_")
        ]
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
