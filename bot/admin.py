from aiogram import types, Dispatcher

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


from dotenv import load_dotenv
from os import getenv
load_dotenv(".env")

from .database import ENGINE, check_admin_exists, insert_admin, insert_user, get_messages_in_queue, get_message, change_message_status
from .utils import messages_markup, send_answer
from .database.models import MessageStatus

class CreateAdminFSM(StatesGroup):
    password = State()
    email = State()


class MessageAnswer(StatesGroup):
    message = State()
    answer = State()

async def start_admin(message: types.Message):
    await CreateAdminFSM.password.set()
    await message.answer("Enter Admin Password")


async def check_password(message: types.Message, state: FSMContext):
    admin_password = getenv("ADMIN_PASSWORD")
    if message.text == admin_password:
        user = message.from_user.id
        if check_admin_exists(engine=ENGINE, user_tg_id=user):
            await message.answer("Admin already exists!")
        else:
            async with state.proxy() as data:
                data["user_tg_id"] = user
            await CreateAdminFSM.next()
            await message.answer("Send your email")
    else:
        await state.finish()
        await message.answer("Wrong Password!")


async def register_email(message: types.Message, state: FSMContext):
    email = message.text
    
    def email_is_valid(email):
        from email_validator import validate_email, EmailNotValidError
        try:
            validate_email(email=email)
        except EmailNotValidError:
            return False
        else:
            return True
    
    if email_is_valid(email):
        async with state.proxy() as data:
            data["email"] = email
            insert_user(engine=ENGINE, data={
                    "tg_id":message.from_user.id,
                    "username":message.from_user.username,
                    "full_name":message.from_user.full_name
                }
            )
            insert_admin(engine=ENGINE, data=data)
            await message.answer("admin registered")
    else:
        await state.finish()
        await message.answer("Email is not valid!")


    
async def show_messages(message: types.Message):
    user = message.from_user.id
    if check_admin_exists(engine=ENGINE, user_tg_id=user):
        messages = get_messages_in_queue(engine=ENGINE)
        if len(messages):
            markup = messages_markup(messages_list=messages)
            await message.answer("Messages list", reply_markup=markup)
        else:
            await message.answer("There is no messages yet")


async def message_managing(call: types.CallbackQuery, state: FSMContext):
    await MessageAnswer.message.set()
    message_id = call.data.replace("admin_get_message_", "")
    message = get_message(engine=ENGINE, message_id=message_id)
    change_message_status(engine=ENGINE, message_id=message.id, status=MessageStatus.Readed)

    async with state.proxy() as data:
        data["message_id"] = message_id

    await MessageAnswer.next()
    await call.message.answer("Give answer:")


async def message_answer(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["answer"] = message.text
        await send_answer(data)
        message_ = get_message(engine=ENGINE, message_id=data["message_id"])
        change_message_status(engine=ENGINE, message_id=message_.id, status=MessageStatus.Answered)

    await state.finish()
    await message.answer("Answer sended.")

    




def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_admin, commands=["admin"])
    dp.register_message_handler(check_password, content_types=types.ContentType.TEXT, state=CreateAdminFSM.password)
    dp.register_message_handler(register_email, content_types=types.ContentTypes.TEXT, state=CreateAdminFSM.email)

    dp.register_message_handler(show_messages, commands=["messages"])
    dp.register_callback_query_handler(message_managing, lambda call: call.data.startswith("admin_get_message_"), state="*")
    dp.register_message_handler(message_answer, content_types=types.ContentTypes.TEXT, state=MessageAnswer.answer)