from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from .strings import get_string
from typing import Union


def _create_keyboard(keyboard: list, one_time: bool = False) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=one_time)


_default_keyboard = _create_keyboard([['no_keyboard']])


def get_keyboard(key, language='ru') -> Union[ReplyKeyboardRemove, ReplyKeyboardMarkup]:
    if key == 'remove':
        return ReplyKeyboardRemove()
    elif key == 'start.languages':
        return _create_keyboard([[get_string('languages.ru', language), get_string('languages.uz')]], one_time=True)
    elif key == 'menu':
        keyboard = [
            [get_string('menu.cabinet', language)],
            [get_string('menu.about', language)],
            [get_string('menu.faq', language)],
            [get_string('menu.news', language)],
            [get_string('menu.support', language)],
            [get_string('menu.partners', language)]
        ]
        return _create_keyboard(keyboard)
