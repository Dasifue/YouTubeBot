from aiogram import types, Dispatcher

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from .markups import types_markup, resolutions_markup
from .utils import find_resolutions, find_video

class FSM(StatesGroup):
    ulr = State()
    type = State()
    resolution = State()



async def fsm_start(call: types.CallbackQuery):
    await FSM.ulr.set()
    await call.message.answer("Send YouTube link")


async def set_url(message: types.Message, state: FSMContext):
    try:
        find_video(message.text)
    except Exception:
        await message.reply("Error! Make shure that video length less than 10 minutes or available on YouTube! \nStart again")
        await state.finish()
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
        async with state.proxy() as data:
            data["resolution"] = None
            await call.message.answer(str(data))
        await state.finish()


async def set_resolution(call: types.CallbackQuery, state: FSMContext):
    resolution = call.data.split("-")[1]
    async with state.proxy() as data:
        data["resolution"] = resolution        
        await call.message.answer(str(data))
    await state.finish()


def register_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(fsm_start, lambda call: call.data=="download", state=None)
    dp.register_message_handler(set_url, content_types=types.ContentType.TEXT, state=FSM.ulr)
    dp.register_callback_query_handler(set_type, lambda call: call.data in ("video", "audio"), state=FSM.type)
    dp.register_callback_query_handler(set_resolution, lambda call: call.data.startswith("resolution"), state=FSM.resolution)