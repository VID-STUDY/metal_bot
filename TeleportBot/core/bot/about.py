from telegram import ParseMode
from telegram.ext import MessageHandler, CallbackQueryHandler
from telegram.error import BadRequest

from core.resources import utils, strings, keyboards
from core.services import settings, users
from .utils import Filters


def about(update, context):
    context.user_data['user'] = users.user_exists(update.message.from_user.id)
    if context.user_data['user'].get('is_blocked'):
        blocked_message = strings.get_string('blocked', context.user_data['user'].get('language'))
        update.message.reply_text(blocked_message)
        return
    if context.user_data['user'].get('language') == 'uz':
        about_message = settings.get_settings().get('about_uz')
    else:
        about_message = settings.get_settings().get('about')
    about_message = utils.replace_new_line(about_message)
    about_keyboard = keyboards.get_keyboard('about', language=context.user_data['user'].get('language'))
    message = update.message.reply_text(text=about_message, parse_mode=ParseMode.HTML, reply_markup=about_keyboard)
    if 'about_message_id' in context.user_data:
        try:
            context.bot.delete_message(chat_id=update.message.chat_id, message_id=context.user_data['about_message_id'])
        except BadRequest:
            pass
    context.user_data['about_message_id'] = message.message_id


def close(update, context):
    query = update.callback_query
    try:
        context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
    except BadRequest:
        pass


about_handler = MessageHandler(Filters.AboutFilter(), about)
close_handler = CallbackQueryHandler(close, pattern='about:close')
