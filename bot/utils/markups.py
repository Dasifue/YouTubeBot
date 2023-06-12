from aiogram.types import (
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    KeyboardButton,
    Message
)

stop_btn = InlineKeyboardButton("Cancel", callback_data="break_states")

def main_markup():
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = (
        InlineKeyboardButton("Start Downloading", callback_data="download"),
        InlineKeyboardButton("Help", callback_data="help"),
        InlineKeyboardButton("Messages", callback_data="messages"),
    )
    markup.add(*buttons)
    return markup


def types_markup():
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = (
        InlineKeyboardButton("video", callback_data="video"),
        InlineKeyboardButton("audio", callback_data="audio"),
    )
    markup.add(*buttons)
    markup.add(stop_btn)
    return markup


def resolutions_markup(resolutions):
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = list(map(lambda resolution: InlineKeyboardButton(resolution, callback_data=f"resolution-{resolution}"), resolutions))
    markup.add(*buttons)
    markup.add(stop_btn)
    return markup


def messages_managing_markup():
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton("Send message", callback_data="create_message"),
        InlineKeyboardButton("My messages", callback_data="user_messages"),
    ]
    markup.add(*buttons)
    return markup


def messages_list_markup(messages_list):
    markup = InlineKeyboardMarkup(row_width=1)
    buttons = [InlineKeyboardButton(message.text[:21], callback_data=f"get_message_{message.id}") for message in messages_list]
    markup.add(*buttons)
    return markup


def message_managing_markup(message_id):
    markup = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(text="Edit message", callback_data=f"edit_message_{message_id}"),
        InlineKeyboardButton(text="Delete message", callback_data=f"delete_message_{message_id}"),
    ]
    markup.add(*buttons)
    return markup


__all__ = [
    'main_markup',
    'types_markup',
    'resolutions_markup',
    'messages_managing_markup',
    'messages_list_markup',
    'message_managing_markup',
]

