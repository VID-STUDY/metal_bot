from telegram import ParseMode
from telegram.ext import MessageHandler
from telegram.error import BadRequest

from core.resources import utils, strings
from core.services import settings, users
from .utils import Filters


def about(update, context):
    context.user_data['user'] = users.user_exists(update.message.from_user.id)
    if context.user_data['user'].get('is_blocked'):
        blocked_message = strings.get_string('blocked', context.user_data['user'].get('language'))
        update.message.reply_text(blocked_message)
        return
    about_message = settings.get_settings().get('about')
    about_message = utils.replace_new_line(about_message)
    message = update.message.reply_text(text=about_message, parse_mode=ParseMode.HTML)
    if 'about_message_id' in context.user_data:
        try:
            context.bot.delete_message(chat_id=update.message.chat_id, message_id=context.user_data['about_message_id'])
        except BadRequest:
            pass
    context.user_data['about_message_id'] = message.message_id


about_handler = MessageHandler(Filters.AboutFilter(), about)
