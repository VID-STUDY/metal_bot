from telegram import Update, ParseMode
from telegram.ext import Filters, ConversationHandler, CallbackQueryHandler, MessageHandler
from core.resources import strings, keyboards
from .utils import Navigation


TITLE, DESCRIPTION, CONTACTS = range(3)


def create(update, context):
    query = update.callback_query
    context.user_data['resume'] = {}
    language = context.user_data['language']
    query.answer(text=strings.get_string('resumes.menu_has_gone', language), show_alert=True)
    message = strings.get_string('resumes.create.title', language)
    keyboard = keyboards.get_keyboard('go_back', language)
    context.bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
    context.bot.send_message(chat_id=query.from_user.id, text=message, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    return TITLE


def resume_title(update, context):
    language = context.user_data['language']
    if strings.get_string('go_back', language) in update.message.text:
        Navigation.to_main_menu(update, language)
        return ConversationHandler.END
    context.user_data['resume']['title'] = update.message.text
    message = strings.get_string('resumes.create.description', language)
    update.message.reply_text(message, parse_mode=ParseMode.HTML)
    return DESCRIPTION


def resume_description(update, context):
    language = context.user_data['language']
    if strings.get_string('go_back', language) in update.message.text:
        message = strings.get_string('resumes.create.title', language)
        update.message.reply_text(message)
        return TITLE
    context.user_data['resume']['description'] = update.message.text
    message = strings.get_string('resumes.create.contacts', language)
    update.message.reply_text(message, parse_mode=ParseMode.HTML)
    return CONTACTS


def resume_contacts(update, context):
    language = context.user_data['language']
    if strings.get_string('go_back', language) in update.message.text:
        message = strings.get_string('resumes.create.description', language)
        update.message.reply_text(message)
        return DESCRIPTION
    context.user_data['resume']['contacts'] = update.message.text
    message = strings.get_string('location.regions', language)
    keyboard = keyboards.get_keyboard('location.regions', language)
    update.message.reply_text(message, reply_markup=keyboard)
    return ConversationHandler.END


resume_create_handler = CallbackQueryHandler(create, pattern='my_resumes:create')
create_resume_conversation = ConversationHandler(
    entry_points=[resume_create_handler],
    states={
        TITLE: [MessageHandler(Filters.text, resume_title)],
        DESCRIPTION: [MessageHandler(Filters.text, resume_description)],
        CONTACTS: [MessageHandler(Filters.text, resume_contacts)]
    },
    fallbacks=[MessageHandler(Filters.text, '')]
)
