from telegram import Update
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters
from core.resources import strings, keyboards
from core.services import users
from .utils import Navigation

LANGUAGES = 1


def referral_start(update, context):
    user = users.user_exists(update.message.from_user.id)
    if user:
        if user.get('is_blocked'):
            blocked_message = strings.get_string('blocked', user.get('language'))
            update.message.reply_text(blocked_message)
            return ConversationHandler.END
        Navigation.to_main_menu(update, user.get('language'), user_name=user.get('name'), welcome=True, context=context)
        help_message = strings.get_string('start.help', user.get('language'))
        update.message.reply_text(help_message)
        return ConversationHandler.END
    if context.args:
        context.user_data['referral_from_id'] = context.args[0]
    languages_message = strings.get_string('start.languages')
    keyboard = keyboards.get_keyboard('start.languages')

    update.message.reply_text(languages_message, reply_markup=keyboard)

    return LANGUAGES


def languages(update: Update, context):

    def error():
        languages_message = strings.get_string('start.languages')
        keyboard = keyboards.get_keyboard('start.languages')
        update.message.reply_text(languages_message, reply_markup=keyboard)

    text = update.message.text
    if strings.get_string('languages.ru') in text:
        language = 'ru'
    elif strings.get_string('languages.uz') in text:
        language = 'uz'
    else:
        error()
        return LANGUAGES
    user = update.message.from_user
    user_name = _get_user_name(user)
    users.create_user(user.id, user_name, user.username, language,
                      referral_from_id=context.user_data.get('referral_from_id', None))
    Navigation.to_main_menu(update, language, user_name=user_name, welcome=True, context=context)
    help_message = strings.get_string('start.help', language)
    update.message.reply_text(help_message)
    return ConversationHandler.END


def _get_user_name(user):
    user_name = user.first_name
    if user.last_name:
        user_name += (" " + user.last_name)
    return user_name


def cancel():
    pass


conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('start', referral_start, pass_args=True)],
    states={
        LANGUAGES: [MessageHandler(Filters.text, languages)]
    },
    fallbacks=[MessageHandler(Filters.text, '')]
)
