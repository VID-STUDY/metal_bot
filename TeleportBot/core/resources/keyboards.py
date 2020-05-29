from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from .strings import get_string
from typing import Union, Optional


def _create_keyboard(keyboard: list, one_time: bool = False) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=one_time)


_default_keyboard = _create_keyboard([['no_keyboard']])


def get_keyboard(key, language='ru') -> Union[ReplyKeyboardRemove, ReplyKeyboardMarkup, InlineKeyboardMarkup]:
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
    elif key == 'account.select_role':
        keyboard = [
            [InlineKeyboardButton(get_string('account.select_role.contractor', language), callback_data='role'
                                                                                                        ':contractor')],
            [InlineKeyboardButton(get_string('account.select_role.employer', language), callback_data='role:employer')]
        ]
        return InlineKeyboardMarkup(keyboard)


def get_account_keyboard(user: dict) -> Optional[InlineKeyboardMarkup]:
    if user.get('user_role') == 'employer':
        keyboard = [
            [InlineKeyboardButton(get_string('account.change_role', user.get('language')),
                                  callback_data='account:role')],
            [InlineKeyboardButton(get_string('account.up_balance', user.get('language')),
                                  callback_data='account:balance')],
            [InlineKeyboardButton(get_string('account.responses', user.get('language')),
                                  callback_data='account:responses')],
            [InlineKeyboardButton(get_string('account.my_vacancies', user.get('language')),
                                  callback_data='account:my_vacancies')]
        ]
    elif user.get('user_role') == 'contractor':
        keyboard = [
            [InlineKeyboardButton(get_string('account.change_role', user.get('language')),
                                  callback_data='account:role')],
            [InlineKeyboardButton(get_string('account.up_balance', user.get('language')),
                                  callback_data='account:balance')],
            [InlineKeyboardButton(get_string('account.vacancies', user.get('language')),
                                  callback_data='account:vacancies')],
            [InlineKeyboardButton(get_string('account.resumes', user.get('language')),
                                  callback_data='account:resumes')]
        ]
    else:
        return None
    return InlineKeyboardMarkup(keyboard)
