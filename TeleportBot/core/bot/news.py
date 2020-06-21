from telegram import ParseMode
from telegram.ext import MessageHandler

from core.resources import utils
from core.services import settings
from .utils import Filters


def news(update, context):
    if 'has_action' in context.user_data:
        return
    news_message = settings.get_settings().get('news')
    news_message = utils.replace_new_line(news_message)
    update.message.reply_text(text=news_message, parse_mode=ParseMode.HTML)


news_handler = MessageHandler(Filters.NewsFilter(), news)
