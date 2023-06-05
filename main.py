from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

import os
load_dotenv(".env")

storage = MemoryStorage()
my_bot = Bot(os.getenv("BOT_TOKEN"))
dp = Dispatcher(my_bot, storage=storage)

from bot import bot, fsm

bot.register_handlers(dp)
fsm.register_handlers(dp)


if __name__ == "__main__":
    executor.start_polling(skip_updates=True, dispatcher=dp)

