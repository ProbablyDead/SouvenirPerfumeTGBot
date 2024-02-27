from aiogram import F
from aiogram import Router
from aiogram import Bot, Dispatcher, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest

router = Router()

async def start_polls(message: types.Message):
    await message.answer("Вопрос 1.", reply_markup=poll1())

async def update_poll(message: types.Message, text: str, keyboard):
    with suppress(TelegramBadRequest):
        await message.edit_text(
            f"{text}",
            reply_markup=keyboard
        )


@router.callback_query(F.data.startswith("var1_"))
async def callbacks_var1(callback: types.CallbackQuery):
    action = callback.data.split("_")[1]
    if action == "1":
        await update_poll(callback.message, "Вопрос 2.", poll2())
    elif action == "2":
        await update_poll(callback.message, "Вопрос 2.", poll2())
    elif action == "3":
        await update_poll(callback.message, "Вопрос 2.", poll2())
    elif action == "4":
        await update_poll(callback.message, "Вопрос 2.", poll2())        

    await callback.answer()

@router.callback_query(F.data.startswith("var2_"))
async def callbacks_var2(callback: types.CallbackQuery):
    action = callback.data.split("_")[1]
    if action == "1":
        await update_poll(callback.message, "Вопрос 3.", poll3())
    elif action == "2":
        await update_poll(callback.message, "Вопрос 3.", poll3())
    elif action == "3":
        await update_poll(callback.message, "Вопрос 3.", poll3())
    elif action == "4":
        await update_poll(callback.message, "Вопрос 3.", poll3())        

    await callback.answer()

@router.callback_query(F.data.startswith("var3_"))
async def callbacks_var3(callback: types.CallbackQuery):
    action = callback.data.split("_")[1]
    if action == "1":
        await update_poll(callback.message, "Вопрос 4.", poll4())
    elif action == "2":
        await update_poll(callback.message, "Вопрос 4.", poll4())
    elif action == "3":
        await update_poll(callback.message, "Вопрос 4.", poll4())
    elif action == "4":
        await update_poll(callback.message, "Вопрос 4.", poll4())

    await callback.answer()

@router.callback_query(F.data.startswith("var4_"))
async def callbacks_var4(callback: types.CallbackQuery):
    action = callback.data.split("_")[1]
    if action == "1":
        await update_poll(callback.message, "Вопрос 5.", poll5())
    elif action == "2":
        await update_poll(callback.message, "Вопрос 5.", poll5())
    elif action == "3":
        await update_poll(callback.message, "Вопрос 5.", poll5())
    elif action == "4":
        await update_poll(callback.message, "Вопрос 5.", poll5())

    await callback.answer()

@router.callback_query(F.data.startswith("var5_"))
async def callbacks_var5(callback: types.CallbackQuery):
    action = callback.data.split("_")[1]
    if action == "1":
        with suppress(TelegramBadRequest):
            await callback.message.edit_text(
                f"Ваши ответы записаны, вот ваш аромат:",
            )
    elif action == "2":
        with suppress(TelegramBadRequest):
            await callback.message.edit_text(
                f"Ваши ответы записаны, вот ваш аромат:",
            )   
    elif action == "3":
        with suppress(TelegramBadRequest):
            await callback.message.edit_text(
                f"Ваши ответы записаны, вот ваш аромат:",
            )
    elif action == "4":
        with suppress(TelegramBadRequest):
            await callback.message.edit_text(
                f"Ваши ответы записаны, вот ваш аромат:",
            )

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

def poll5():
    buttons = [
        [
            types.InlineKeyboardButton(text="вариант 1", callback_data="var5_1"),
            types.InlineKeyboardButton(text="вариант 2", callback_data="var5_2")
        ],
        [
            types.InlineKeyboardButton(text="вариант 3", callback_data="var5_3"),
            types.InlineKeyboardButton(text="вариант 4", callback_data="var5_4")
        ]
    ]

    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
