from telegram import ParseMode
from telegram.ext import MessageHandler, CallbackQueryHandler
from telegram.error import BadRequest

from core.resources import utils, images, strings, keyboards
from core.services import settings, users
from .utils import Filters


def news(update, context):
    context.user_data['user'] = users.user_exists(update.message.from_user.id)
    if context.user_data['user'].get('is_blocked'):
        blocked_message = strings.get_string('blocked', context.user_data['user'].get('language'))
        update.message.reply_text(blocked_message)
        return
    if context.user_data['user'].get('language') == 'uz':
        news_message = settings.get_settings().get('news_uz')
    else:
        news_message = settings.get_settings().get('news')
    news_message = utils.replace_new_line(news_message)
    news_keyboard = keyboards.get_keyboard('news', language=context.user_data['user'].get('language'))
    image = images.get_news_image()
    if image:
        chat_id = update.message.chat_id
        message = context.bot.send_photo(chat_id=chat_id, photo=image, caption=news_message, parse_mode=ParseMode.HTML,
                                         reply_markup=news_keyboard)
    else:
        message = update.message.reply_text(text=news_message, parse_mode=ParseMode.HTML,
                                            reply_markup=news_keyboard)
    if 'news_message_id' in context.user_data:
        try:
            context.bot.delete_message(chat_id=update.message.chat_id, message_id=context.user_data['news_message_id'])
        except BadRequest:
            pass
    context.user_data['news_message_id'] = message.message_id


def close(update, context):
    query = update.callback_query
    try:
        context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
    except BadRequest:
        pass


news_handler = MessageHandler(Filters.NewsFilter(), news)
close_handler = CallbackQueryHandler(close, pattern='news:close')
