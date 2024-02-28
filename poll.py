from aiogram import F
from aiogram import Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram import Bot, Dispatcher, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest

router = Router()

class last_question(StatesGroup):
    view_quest = State()
    answered_quest = State() 

dist = {}

def get_dist():
    return dist
    

async def start_polls(message: types.Message):
    await message.answer("Вопрос 1.", reply_markup=poll1())

async def update_poll(message: types.Message, text: str, keyboard=None):
    with suppress(TelegramBadRequest):
        await message.edit_text(
            f"{text}",
            reply_markup=keyboard
        )

@router.message(last_question.view_quest)
async def answer(message: types.Message, state: FSMContext):
    id = message.from_user.id
    dist[f"{id}" + "_5"] = f"{message.text}"
    await state.set_state(last_question.answered_quest)
    await message.answer(f"{message.text}")


@router.callback_query(F.data.startswith("var1_"))
async def callbacks_var1(callback: types.CallbackQuery):
    action = callback.data.split("_")[1]
    id = callback.from_user.id
    dist[f"{id}" + "_1"] = action
    await update_poll(callback.message, "Вопрос 2.", poll2())  

    await callback.answer()

@router.callback_query(F.data.startswith("var2_"))
async def callbacks_var2(callback: types.CallbackQuery):
    action = callback.data.split("_")[1]
    id = callback.from_user.id
    dist[f"{id}" + "_2"] = action
    await update_poll(callback.message, "Вопрос 3.", poll3())        

    await callback.answer()

@router.callback_query(F.data.startswith("var3_"))
async def callbacks_var3(callback: types.CallbackQuery):
    action = callback.data.split("_")[1]
    id = callback.from_user.id
    dist[f"{id}" + "_3"] = action
    await update_poll(callback.message, "Вопрос 4.", poll4())

    await callback.answer()

@router.callback_query(F.data.startswith("var4_"))
async def callbacks_var4(callback: types.CallbackQuery, state: FSMContext):
    action = callback.data.split("_")[1]
    await state.set_state(last_question.view_quest)
    id = callback.from_user.id
    dist[f"{id}" + "_4"] = action
    await update_poll(callback.message, "Открытый вопрос.")

    await callback.answer()

def poll1():
    buttons = [
        [
            types.InlineKeyboardButton(text="вариант 1", callback_data="var1_1"),
            types.InlineKeyboardButton(text="вариант 2", callback_data="var1_2")
        ],
        [
            types.InlineKeyboardButton(text="вариант 3", callback_data="var1_3"),
            types.InlineKeyboardButton(text="вариант 4", callback_data="var1_4")
        ]
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def poll2():
    buttons = [
        [
            types.InlineKeyboardButton(text="вариант 1", callback_data="var2_1"),
            types.InlineKeyboardButton(text="вариант 2", callback_data="var2_2")
        ],
        [
            types.InlineKeyboardButton(text="вариант 3", callback_data="var2_3"),
            types.InlineKeyboardButton(text="вариант 4", callback_data="var2_4")
        ]
    ]
    
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def poll3():
    buttons = [
        [
            types.InlineKeyboardButton(text="вариант 1", callback_data="var3_1"),
            types.InlineKeyboardButton(text="вариант 2", callback_data="var3_2")
        ],
        [
            types.InlineKeyboardButton(text="вариант 3", callback_data="var3_3"),
            types.InlineKeyboardButton(text="вариант 4", callback_data="var3_4")
        ]
    ]
    
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard

def poll4():
    buttons = [
        [
            types.InlineKeyboardButton(text="вариант 1", callback_data="var4_1"),
            types.InlineKeyboardButton(text="вариант 2", callback_data="var4_2")
        ],
        [
            types.InlineKeyboardButton(text="вариант 3", callback_data="var4_3"),
            types.InlineKeyboardButton(text="вариант 4", callback_data="var4_4")
        ]
    ]
    
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard