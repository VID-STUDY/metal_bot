from telegram import ParseMode
from telegram.ext import MessageHandler, CallbackQueryHandler
from telegram.error import BadRequest

from core.resources import utils, images, strings, keyboards
from core.services import settings, users
from .utils import Filters, Navigation


def news(update, context):
    context.user_data['user'] = users.user_exists(update.callback_query.from_user.id)
    if context.user_data['user'].get('is_blocked'):
        blocked_message = strings.get_string('blocked', context.user_data['user'].get('language'))
        update.callback_query.answer(text=blocked_message, show_alert=True)
        return
    if context.user_data['user'].get('language') == 'uz':
        news_message = settings.get_settings().get('news_uz')
    else:
        news_message = settings.get_settings().get('news')
    news_message = utils.replace_new_line(news_message)
    news_keyboard = keyboards.get_keyboard('news', language=context.user_data['user'].get('language'))
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.callback_query.message.message_id)
    image = images.get_news_image(context.user_data['user'].get('language'))
    if image:
        chat_id = update.effective_message.chat_id
        context.bot.send_photo(chat_id=chat_id, photo=image, caption=news_message, parse_mode=ParseMode.HTML,
                                         reply_markup=news_keyboard)
    else:
        update.effective_message.reply_text(text=news_message, parse_mode=ParseMode.HTML,
                                            reply_markup=news_keyboard)


def close(update, context):
    query = update.callback_query
    try:
        context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
    except BadRequest:
        pass
    Navigation.to_account(update, context, new_message=True)


news_handler = CallbackQueryHandler(news, pattern='account:news')
close_handler = CallbackQueryHandler(close, pattern='news:close')
