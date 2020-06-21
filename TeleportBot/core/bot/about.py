from telegram import ParseMode
from telegram.ext import MessageHandler

from core.resources import utils
from core.services import settings
from .utils import Filters


def about(update, context):
    if 'has_action' in context.user_data:
        return
    about_message = settings.get_settings().get('about')
    about_message = utils.replace_new_line(about_message)
    update.message.reply_text(text=about_message, parse_mode=ParseMode.HTML)


about_handler = MessageHandler(Filters.AboutFilter(), about)
