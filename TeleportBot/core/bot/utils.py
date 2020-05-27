from core.resources import strings, keyboards
from telegram.ext import BaseFilter


class Navigation:
    @staticmethod
    def to_main_menu(update, language, message_text=None, user_name=None):
        if message_text:
            menu_message = message_text
        else:
            menu_message = strings.get_string('start.welcome', language).format(username=user_name)
        menu_keyboard = keyboards.get_keyboard('menu', language)
        update.message.reply_text(menu_message, reply_markup=menu_keyboard)


class Filters:
    class AccountFilter(BaseFilter):
        def filter(self, message):
            return message.text and (strings.get_string('menu.cabinet', 'ru') in message.text or
                                     strings.get_string('menu.cabinet', 'uz') in message.text)
