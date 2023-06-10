from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

import os
import bot
import database
load_dotenv(".env")

storage = MemoryStorage()
my_bot = Bot(os.getenv("BOT_TOKEN"))
dp = Dispatcher(my_bot, storage=storage)

USER = os.getenv("db_ADMIN")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
PASSWORD = os.getenv("PASSWORD")
DATABASE = os.getenv("DATABASE")

bot.bot_handlers(dp)
bot.fsm_handlers(dp)

engine = database.create_mysql_engine(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        database=DATABASE
    )    

if __name__ == "__main__":
    database.create_tables(engine)
    executor.start_polling(dp, skip_updates=True)
    
