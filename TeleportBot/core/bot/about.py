from telegram import ParseMode
from telegram.ext import MessageHandler
from telegram.error import BadRequest

from core.resources import utils
from core.services import settings
from .utils import Filters


def about(update, context):
    if 'has_action' in context.user_data:
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
