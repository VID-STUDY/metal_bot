from telegram import ParseMode
from telegram.ext import MessageHandler

from core.resources import utils
from core.services import settings
from .utils import Filters


def faq(update, context):
    if 'has_action' in context.user_data:
        return
    faq_message = settings.get_settings().get('faq')
    faq_message = utils.replace_new_line(faq_message)
    update.message.reply_text(text=faq_message, parse_mode=ParseMode.HTML)


faq_handler = MessageHandler(Filters.FaqFilter(), faq)
