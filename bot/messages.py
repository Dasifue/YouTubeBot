from aiogram import types, Dispatcher
from .fsm import CreateMessageFSM, EditMessageFSM, FSMContext


from .utils import (
    messages_managing_markup,
    messages_list_markup,
    message_managing_markup   
)

from .database import (
    get_user_messages,
    insert_user,
    insert_message,
    get_message,
    delete_message as drop_message,
    change_message_text,
    ENGINE
)





async def messages_managing(call: types.CallbackQuery):
    markup = messages_managing_markup()
    text = "Here you can manage your messages"
    await call.message.answer(text, reply_markup=markup)


async def messages_list(call: types.CallbackQuery):
    user = call.message.chat.id
    messages = get_user_messages(engine=ENGINE, user_tg_id=user)
    if messages:
        markup = messages_list_markup(messages)
        text = "Here are your messages"
        await call.message.edit_text(text=text, reply_markup=markup)
    else:
        await call.message.answer("You didn't write any message")
        await messages_managing(call)



async def message_managing(call: types.CallbackQuery):
    message_id = call.data.replace("get_message_", "")
    message = get_message(engine=ENGINE, message_id=message_id)
    markup = message_managing_markup(message_id)

    await call.message.edit_text(text=message.text, reply_markup=markup)








async def pre_edit_message(call: types.CallbackQuery, state: FSMContext):
    await EditMessageFSM.message.set()
    message_id = call.data.replace("edit_message_", "")
    message = get_message(engine=ENGINE, message_id=message_id)

    async with state.proxy() as data:
        data["message"] = message.id
    await EditMessageFSM.next()

    
    await call.message.answer("Enter text")    


async def edit_message(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["text"] = message.text
        change_message_text(engine=ENGINE, data=data)
    await state.finish()
    await message.answer("Message has been changed")
    markup = messages_managing_markup()
    text = "Message manager"
    await message.answer(text, reply_markup=markup)









async def pre_create_message(call: types.CallbackQuery):
    text = "Cool! Now send message and we will answer soon."
    await CreateMessageFSM.text.set()
    await call.message.answer(text=text)


async def create_message(message: types.Message, state: FSMContext):
    user_data = {
        "tg_id": message.from_user.id,
        "username": message.from_user.username,
        "full_name": message.from_user.full_name,
    }

    message_data = {
        "user_tg_id": message.from_user.id,
        "text": message.text,
    }

    insert_user(engine=ENGINE, data=user_data)
    insert_message(engine=ENGINE, data=message_data)
    await message.answer("Good! I registerd your message.")
    await state.finish()
    markup = messages_managing_markup()
    text = "Message manager"
    await message.answer(text, reply_markup=markup)










async def delete_message(call: types.CallbackQuery, state: FSMContext):
    message_id = call.data.replace("delete_message_", "")
    drop_message(engine=ENGINE, message_id=message_id)
    await call.message.edit_text("Message deleted.")
    await state.finish()
    await messages_managing(call)




async def back_to_message_managing(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    markup = messages_managing_markup()
    text = "Here you can manage your messages"
    await call.message.edit_text(text, reply_markup=markup)





def register_handlers(dp: Dispatcher):
    #Manage and listing
    dp.register_callback_query_handler(messages_managing, lambda call: call.data=="messages")
    dp.register_callback_query_handler(messages_list, lambda call: call.data=="user_messages")
    dp.register_callback_query_handler(message_managing, lambda call: call.data.startswith("get_message_"))


    #Message creating
    dp.register_callback_query_handler(pre_create_message, lambda call: call.data=="create_message", state="*")
    dp.register_message_handler(create_message, content_types=types.ContentType.TEXT, state=CreateMessageFSM.text)


    #Message updating
    dp.register_callback_query_handler(pre_edit_message, lambda call: call.data.startswith("edit_message_"), state="*")
    dp.register_message_handler(edit_message, content_types=types.ContentType.TEXT, state=EditMessageFSM.text)

    #Message deleting
    dp.register_callback_query_handler(delete_message, lambda call: call.data.startswith("delete_message_"), state="*")


    #Message managing
    dp.register_callback_query_handler(back_to_message_managing, lambda call: call.data=="back_to_managing", state="*")

