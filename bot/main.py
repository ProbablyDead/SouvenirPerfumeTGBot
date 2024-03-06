import asyncio
import logging

from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher 
from aiogram.enums import ParseMode

from config.token import BOT_TOKEN
from poll import router

import start

class TelegramBot:
    def __init__(self) -> None:
        logging.basicConfig(level=logging.INFO)

        self.bot = Bot(token=BOT_TOKEN,
                       default=DefaultBotProperties(parse_mode=ParseMode.HTML))

        self.dp = Dispatcher()
        self.dp.include_router(router)

    async def main(self):
        await self.dp.start_polling(self.bot)


if __name__ == "__main__":
    tg = TelegramBot()
    asyncio.run(tg.main())
