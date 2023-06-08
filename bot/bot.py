from aiogram import types, Dispatcher

from .utils import main_markup

async def welcome_message(message: types.Message):
    markup = main_markup()
    user = message.from_user.username
    text = f"""
    Hello, {user}!
    This is YouTubeDownloaderBot! As you can understand, my main mission is to help you download YouTube materials as video or audio.
    Send command - /help - to see tutorial
    """
    await message.answer(text=text, reply_markup=markup)

async def send_main_markup(message: types.Message):
    markup = main_markup()
    text = "YouTubeDownloader"
    await message.answer(text=text, reply_markup=markup)


async def send_instruction_by_message(message: types.Message):
    help_text = """
    Usage of this bot is simple:
    1) send me '/download' command
    2) chooce option (Start downloading if you want to get file)
    3) Go to YouTube and copy video link (video must be available and less than 10 minutes)
    4) After i send you message 'Send YouTube link' paste copied link
    5) If this link is correct I will give you a choise: video or audio. Tap on file format you want
    6) If you choosed audio - wait for minute and take file. But if you choosed video - you must choose resolution. Just wait for moment and let me send you another message
    7) Tap on resolution you want and waint for minute. After you cat take file.
    8) Start again
    """
    await message.reply(text=help_text)


async def send_instruction_by_call(call: types.CallbackQuery):
    help_text = """
    Usage of this bot is simple:
    1) send me '/download' command
    2) chooce option (Start downloading if you want to get file)
    3) Go to YouTube and copy video link (video must be available and less than 10 minutes)
    4) After i send you message 'Send YouTube link' paste copied link
    5) If this link is correct I will give you a choise: video or audio. Tap on file format you want
    6) If you choosed audio - wait for minute and take file. But if you choosed video - you must choose resolution. Just wait for moment and let me send you another message
    7) Tap on resolution you want and waint for minute. After you cat take file.
    8) Start again
    """
    await call.message.answer(text=help_text)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(welcome_message, commands=["start"])
    dp.register_callback_query_handler(send_instruction_by_call, lambda call: call.data=="help")
    dp.register_message_handler(send_instruction_by_message, commands=["help"])