from telegram import ParseMode
from telegram.ext import MessageHandler
from telegram.error import BadRequest

from core.resources import utils
from core.services import settings
from .utils import Filters


def partners(update, context):
    partners_message = settings.get_settings().get('partners')
    partners_message = utils.replace_new_line(partners_message)
    message = update.message.reply_text(text=partners_message, parse_mode=ParseMode.HTML)
    if 'partners_message_id' in context.user_data:
        try:
            context.bot.delete_message(chat_id=update.message.chat_id,
                                       message_id=context.user_data['partners_message_id'])
        except BadRequest:
            pass
    context.user_data['partners_message_id'] = message.message_id


partners_handler = MessageHandler(Filters.PartnersFilter(), partners)
