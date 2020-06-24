from core.resources import strings, keyboards, images
from telegram.ext import BaseFilter
from core.services import users
from telegram.error import BadRequest


class Navigation:
    @staticmethod
    def to_main_menu(update, language, message_text=None, user_name=None):
        if message_text:
            menu_message = message_text
        else:
            menu_message = strings.get_string('start.welcome', language).format(username=user_name)
        menu_keyboard = keyboards.get_keyboard('menu', language)
        update.message.reply_text(menu_message, reply_markup=menu_keyboard)

    @staticmethod
    def to_account(update, context, new_message=False):
        if update.message:
            user_id = update.message.from_user.id
        elif update.callback_query:
            user_id = update.callback_query.from_user.id
        if 'user' not in context.user_data:
            context.user_data['user'] = users.user_exists(user_id)
        user = context.user_data['user']
        account_message = strings.get_user_info(user)
        account_keyboard = keyboards.get_account_keyboard(user)
        image = images.get_account_image(context.user_data['user'].get('user_role'))
        if update.message:
            if image:
                message = context.bot.send_photo(chat_id=user_id, photo=image, caption=account_message,
                                                 reply_markup=account_keyboard)
            else:
                message = update.message.reply_text(text=account_message, reply_markup=account_keyboard)
        elif update.callback_query:
            if new_message:
                if image:
                    message = context.bot.send_photo(chat_id=user_id, photo=image, caption=account_message,
                                                     reply_markup=account_keyboard)
                else:
                    message = context.bot.send_message(chat_id=user_id, text=account_message, reply_markup=account_keyboard)
            else:
                if image:
                    context.bot.delete_message(chat_id=user_id, message_id=update.callback_query.message.message_id)
                    message = context.bot.send_photo(chat_id=user_id, photo=image, caption=account_message,
                                                     reply_markup=account_keyboard)
                else:
                    update.callback_query.edit_message_text(text=account_message, reply_markup=account_keyboard)
                    return
        else:
            return
        if 'account_message_id' in context.user_data:
            try:
                context.bot.delete_message(chat_id=user_id, message_id=context.user_data['account_message_id'])
            except BadRequest:
                pass
        context.user_data['account_message_id'] = message.message_id


class Filters:
    class AccountFilter(BaseFilter):
        def filter(self, message):
            return message.text and (strings.get_string('menu.cabinet', 'ru') in message.text or
                                     strings.get_string('menu.cabinet', 'uz') in message.text)

    class ReferralFilter(BaseFilter):
        def filter(self, message):
            return message.text and (strings.get_string('menu.referral', 'ru') in message.text or
                                     strings.get_string('menu.referral', 'uz') in message.text)

    class FaqFilter(BaseFilter):
        def filter(self, message):
            return message.text and (strings.get_string('menu.faq', 'ru') in message.text or
                                     strings.get_string('menu.faq', 'uz') in message.text)

    class AboutFilter(BaseFilter):
        def filter(self, message):
            return message.text and (strings.get_string('menu.about', 'ru') in message.text or
                                     strings.get_string('menu.about', 'uz') in message.text)

    class PartnersFilter(BaseFilter):
        def filter(self, message):
            return message.text and (strings.get_string('menu.partners', 'ru') in message.text or
                                     strings.get_string('menu.partners', 'uz') in message.text)

    class NewsFilter(BaseFilter):
        def filter(self, message):
            return message.text and (strings.get_string('menu.news', 'ru') in message.text or
                                     strings.get_string('menu.news', 'uz') in message.text)

    class SupportFilter(BaseFilter):
        def filter(self, message):
            return message.text and (strings.get_string('menu.support', 'ru') in message.text or
                                     strings.get_string('menu.support', 'uz') in message.text)
