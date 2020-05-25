from telegram import Update
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, Filters
from core.resources import strings, keyboards
from core.services import users

LANGUAGES = 1


def start(update: Update, context):
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
    users.create_user(user.id, user_name, user.username, language)
    welcome_message = strings.get_string('start.welcome', language).format(username=user_name)
    menu_keyboard = keyboards.get_keyboard('menu', language)
    update.message.reply_text(welcome_message, reply_markup=menu_keyboard)
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
    entry_points=[CommandHandler('start', start)],
    states={
        LANGUAGES: [MessageHandler(Filters.text, languages)]
    },
    fallbacks=[MessageHandler(Filters.text, '')]
)
