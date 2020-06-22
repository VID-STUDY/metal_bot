from telegram import ParseMode
from telegram.ext import MessageHandler

from core.resources import utils, images
from core.services import settings
from .utils import Filters


def faq(update, context):
    if 'has_action' in context.user_data:
        return
    faq_message = settings.get_settings().get('faq')
    faq_message = utils.replace_new_line(faq_message)
    image = images.get_faq_image()
    if image:
        chat_id = update.message.chat_id
        context.bot.send_photo(chat_id=chat_id, photo=image, caption=faq_message, parse_mode=ParseMode.HTML)
    else:
        update.message.reply_text(text=faq_message, parse_mode=ParseMode.HTML)


faq_handler = MessageHandler(Filters.FaqFilter(), faq)
