from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

import os
import bot
load_dotenv(".env")

storage = MemoryStorage()
my_bot = Bot(os.getenv("BOT_TOKEN"))
dp = Dispatcher(my_bot, storage=storage)


bot.bot_handlers(dp)
bot.fsm_handlers(dp)


if __name__ == "__main__":
    executor.start_polling(skip_updates=True, dispatcher=dp)

