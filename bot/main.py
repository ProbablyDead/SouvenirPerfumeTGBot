import asyncio
import logging

from dotenv import load_dotenv
import os

from aiogram.client.default import DefaultBotProperties
from aiogram import Bot, Dispatcher 
from aiogram.enums import ParseMode

from poll import router

from google_api import Google_worker

import start

SPREADSHEET_ID = None

class TelegramBot:
    def __init__(self) -> None:
        # load env 
        load_dotenv()

        BOT_TOKEN = os.getenv('BOT_TOKEN')

        if BOT_TOKEN == None:
            print("Cannot locate env var BOT_TOKEN")
            exit(1);


        logging.basicConfig(level=logging.INFO)

        self.bot = Bot(token=BOT_TOKEN,
                       default=DefaultBotProperties(parse_mode=ParseMode.HTML))

        self.dp = Dispatcher()
        self.dp.include_router(router)

    async def main(self):
        await self.dp.start_polling(self.bot)


if __name__ == "__main__":
    asyncio.run(TelegramBot().main())
