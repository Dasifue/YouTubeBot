from aiogram.types import (
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButton,
    Message
)

def messages_markup(messages_list):
    markup = InlineKeyboardMarkup(row_width=2)
    messages = [InlineKeyboardButton(message.text, callback_data=f"admin_get_message_{message.id}") for message in messages_list]
    markup.add(*messages)
    return markup



__all__ = [
    "messages_markup",
]