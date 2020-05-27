import os
import json
from . import utils


_basedir = os.path.abspath(os.path.dirname(__file__))

# Load strings from json
# Russian language
_strings_ru = json.loads(open(os.path.join(_basedir, 'strings_ru.json'), 'r', encoding='utf8').read())

# Uzbek language
_strings_uz = json.loads(open(os.path.join(_basedir, 'strings_uz.json'), 'r', encoding='utf8').read())


def get_string(key, language='ru') -> str:
    if language == 'ru':
        return _strings_ru.get(key, 'no_string')
    elif language == 'uz':
        return _strings_uz.get(key, 'no_string')
    else:
        raise Exception('Invalid language')


def get_user_info(user: dict) -> str:
    user_info = get_string('account.id', user.get('language')) + user.get('id')
    user_info += '\n'
    days = utils.date_difference_now(user.get('created_at')).get('days')
    user_info += get_string('account.days', user.get('language')) + days
    user_info += '\n'
    user_info += get_string('account.balance', user.get('language')) + user.get('balance')
    user_info += '\n'
    user_info += get_string('account.status', user.get('language')) + user.get('user_role')

    return user_info
