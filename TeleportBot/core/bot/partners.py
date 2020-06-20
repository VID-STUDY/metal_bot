from telegram import ParseMode
from telegram.ext import MessageHandler

from core.resources import utils
from core.services import settings
from .utils import Filters


def partners(update, context):
    partners_message = settings.get_settings().get('partners')
    partners_message = utils.replace_new_line(partners_message)
    update.message.reply_text(text=partners_message, parse_mode=ParseMode.HTML)


partners_handler = MessageHandler(Filters.PartnersFilter(), partners)
