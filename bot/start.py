from aiogram import F, types
from aiogram.filters import Command

from poll import router, start_test

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


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Приветствуем вас в нашем замечательном боте!", reply_markup=reply_keyboard())


@router.message(F.text.lower() == "пройти тест")
async def start_poll(message: types.Message):
    await start_test(message)


@router.message(F.text.lower() == "заказать аромат")  # Переделать
async def get_contacts(message: types.Message):
    await message.reply("Конечно!\nДля заказа напиши @obnulai и прикрепи желаемый результат теста")

