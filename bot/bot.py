from aiogram import types, Dispatcher
import asyncio

from .markups import main_markup

async def welcome_message(message: types.Message):
    markup = main_markup()
    user = message.from_user.username
    text = f"""
    Hello, {user}!
    This is YouTubeDownloaderBot! As you can understand, my main mission is to help you download YouTube materials as video or audio.
    Send command - /help - to see tutorial
    """
    await message.answer(text=text, reply_markup=markup)


async def send_instruction(message: types.Message):
    await message.reply("Comming SOON")


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(welcome_message, commands=["start"])
    dp.register_message_handler(send_instruction, commands=["help"])