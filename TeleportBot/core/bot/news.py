from telegram import ParseMode
from telegram.ext import MessageHandler
from telegram.error import BadRequest

from core.resources import utils, images
from core.services import settings
from .utils import Filters


def news(update, context):
    if 'has_action' in context.user_data:
        return
    news_message = settings.get_settings().get('news')
    news_message = utils.replace_new_line(news_message)
    image = images.get_news_image()
    if image:
        chat_id = update.message.chat_id
        message = context.bot.send_photo(chat_id=chat_id, photo=image, caption=news_message, parse_mode=ParseMode.HTML)
    else:
        message = update.message.reply_text(text=news_message, parse_mode=ParseMode.HTML)
    if 'news_message_id' in context.user_data:
        try:
            context.bot.delete_message(chat_id=update.message.chat_id, message_id=context.user_data['news_message_id'])
        except BadRequest:
            pass
    context.user_data['news_message_id'] = message.message_id


news_handler = MessageHandler(Filters.NewsFilter(), news)
