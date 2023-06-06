from aiogram import types, Dispatcher

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from .markups import (
    types_markup, 
    resolutions_markup,
    )

from .utils import (
    find_resolutions, 
    find_video, 
    download_video, 
    download_audio, 
    send_audio, 
    send_video,
    delete_file,
    wrong_url
    )

from .bot import send_main_markup

class FSM(StatesGroup):
    url = State()
    type = State()
    resolution = State()



async def fsm_start(call: types.CallbackQuery):
    await FSM.url.set()
    await call.message.answer("Send YouTube link")

async def fsm_start_again(message: types.Message):
    await FSM.url.set()
    await message.answer("Send YouTube link again")

async def set_url(message: types.Message, state: FSMContext):
    if wrong_url(url=message.text):
        await message.reply("Error: wrong link! Make shure that is's YouTube link!")
        await state.finish()
        await fsm_start_again(message)
    else:

        try:
            find_video(message.text)
        except Exception:
            await message.reply("Error! Make shure that video length is less than 10 minutes and available on YouTube!")
            await state.finish()
            await fsm_start_again(message)
        else:
            async with state.proxy() as data:
                data['url'] = message.text
            await FSM.next()
            markup = types_markup()
            await message.answer("Good, now choise option", reply_markup=markup)


async def set_type(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data['type'] = call.data
        url = data['url']
    await FSM.next()
    
    if call.data == "video":
        video = find_video(url)
        resolutions = find_resolutions(video)
        markup = resolutions_markup(resolutions)
        await call.message.edit_text("Choise resolution", reply_markup=markup)
    else:
        await call.message.edit_text("Wait for minute...")
        async with state.proxy() as data:
            data["resolution"] = None
            video = find_video(data["url"])
        file_path = download_audio(video)   
        await call.message.edit_text("Now sending...")
        await send_audio(call.message, file_path)   
        delete_file(file_path)
        await state.finish()
        await send_main_markup(call.message)


async def set_resolution(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("Wait for minute...")
    resolution = call.data.split("-")[1]
    async with state.proxy() as data:
        data["resolution"] = resolution      
        video = find_video(data["url"])
    file_path = download_video(video, resolution)  
    await call.message.edit_text("Now sending...")
    await send_video(call.message, file_path)
    delete_file(file_path)
    await state.finish()
    await send_main_markup(call.message)

async def break_states_by_call(call: types.CallbackQuery, state: FSMContext):
    state_now = await state.get_state()
    if state_now is not None:
        await state.finish()
        await send_main_markup(call.message)

async def break_states_by_message(message: types.CallbackQuery, state: FSMContext):
    state_now = await state.get_state()
    if state_now is not None:
        await state.finish()
        await send_main_markup(message)

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(break_states_by_message, commands=["cancel"], state="*")
    dp.register_callback_query_handler(break_states_by_call, lambda call: call.data=="break_states", state="*")
    dp.register_callback_query_handler(fsm_start, lambda call: call.data=="download", state=None)
    dp.register_message_handler(set_url, content_types=types.ContentType.TEXT, state=FSM.url)
    dp.register_callback_query_handler(set_type, lambda call: call.data in ("video", "audio"), state=FSM.type)
    dp.register_callback_query_handler(set_resolution, lambda call: call.data.startswith("resolution"), state=FSM.resolution)