import asyncio
import logging

from aiogram.client.default import DefaultBotProperties
from poll import router as pr
from aiogram import Router
from poll import start_polls
from aiogram import Bot, Dispatcher, types
from aiogram import F
from aiogram.filters import Command
from aiogram.enums import ParseMode
from config.token import BOT_TOKEN

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN,
          default=DefaultBotProperties(parse_mode=ParseMode.HTML))

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
    await start_polls(message)


@router.message(F.text.lower() == "заказать аромат")  # Переделать
async def get_contacts(message: types.Message):
    await message.reply("Конечно!\nДля заказа напиши @obnulai и прикрепи желаемый результат теста")


if __name__ == "__main__":
    asyncio.run(main())
