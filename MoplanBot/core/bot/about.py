from telegram import ParseMode, Update
from telegram.ext import MessageHandler, CallbackQueryHandler
from telegram.error import BadRequest

from core.resources import utils, strings, keyboards
from core.services import settings, users
from .utils import Filters, Navigation


def about(update: Update, context):
    context.user_data['user'] = users.user_exists(update.callback_query.from_user.id)
    if context.user_data['user'].get('is_blocked'):
        blocked_message = strings.get_string('blocked', context.user_data['user'].get('language'))
        update.callback_query.answer(text=blocked_message, show_alert=True)
        return
    if context.user_data['user'].get('language') == 'uz':
        about_message = settings.get_settings().get('about_uz')
    else:
        about_message = settings.get_settings().get('about')
    about_message = utils.replace_new_line(about_message)
    about_keyboard = keyboards.get_keyboard('about', language=context.user_data['user'].get('language'))
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.callback_query.message.message_id)
    update.effective_message.reply_text(text=about_message, parse_mode=ParseMode.HTML, reply_markup=about_keyboard)


def close(update, context):
    query = update.callback_query
    try:
        context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
    except BadRequest:
        pass
    Navigation.to_account(update, context, new_message=True)


about_handler = CallbackQueryHandler(about, pattern='account:about')
close_handler = CallbackQueryHandler(close, pattern='about:close')
