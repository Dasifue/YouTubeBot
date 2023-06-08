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
        InlineKeyboardButton("Send me message", callback_data="message"),
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

__all__ = [
    'main_markup',
    'types_markup',
    'resolutions_markup'
]

