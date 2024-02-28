import asyncio
import logging
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from poll import router as pr
from aiogram import Router
from poll import start_polls, get_dist
from aiogram import Bot, Dispatcher, types
from aiogram import F
from aiogram.filters import Command
from aiogram.enums import ParseMode
from data.config import BOT_TOKEN
from aiogram.utils.keyboard import InlineKeyboardBuilder

logging.basicConfig(level=logging.INFO)

dist = get_dist()

bot = Bot(token = BOT_TOKEN, parse_mode = ParseMode.HTML)

dp = Dispatcher()
router = Router()
dp.include_router(router)
dp.include_router(pr)

async def main():
    await dp.start_polling(bot)

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="Пройти тест"),
            types.KeyboardButton(text="Заказать аромат")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите действие"
    )
    await message.answer("Приветствуем вас в нашем замечательном боте!", reply_markup=keyboard)

@router.message(F.text.lower() == "пройти тест")
async def start_poll(message: types.Message):
    id = message.from_user.id
    dist[f"{id}" + "_0"] = "joined"                                 #не терять
    await message.answer(f"{dist[f"{id}" + "_0"]}")
    await start_polls(message)
    
@router.message(F.text.lower() == "заказать аромат")                #Переделать
async def get_list(message: types.Message):
    id = message.from_user.id
    for key in dist:
        await message.answer(f"{key}" + ": " + f"{dist[key]}")


if __name__ == "__main__":
    asyncio.run(main())
