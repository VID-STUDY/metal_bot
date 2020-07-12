from telegram import ParseMode
from telegram.ext import MessageHandler, CallbackQueryHandler
from telegram.error import BadRequest

from core.resources import utils, images, strings, keyboards
from core.services import settings, users
from .utils import Filters


def faq(update, context):
    context.user_data['user'] = users.user_exists(update.message.from_user.id)
    if context.user_data['user'].get('is_blocked'):
        blocked_message = strings.get_string('blocked', context.user_data['user'].get('language'))
        update.message.reply_text(blocked_message)
        return
    if context.user_data['user'].get('language') == 'uz':
        faq_message = settings.get_settings().get('faq_uz')
    else:
        faq_message = settings.get_settings().get('faq')
    faq_message = utils.replace_new_line(faq_message)
    faq_keyboard = keyboards.get_keyboard('faq', language=context.user_data['user'].get('language'))
    image = images.get_faq_image(context.user_data['user'].get('language'))
    if image:
        chat_id = update.message.chat_id
        message = context.bot.send_photo(chat_id=chat_id, photo=image, caption=faq_message, parse_mode=ParseMode.HTML,
                                         reply_markup=faq_keyboard)
    else:
        message = update.message.reply_text(text=faq_message, parse_mode=ParseMode.HTML, reply_markup=faq_keyboard)
    if 'faq_message_id' in context.user_data:
        try:
            context.bot.delete_message(chat_id=update.message.chat_id, message_id=context.user_data['faq_message_id'])
        except BadRequest:
            pass
    context.user_data['faq_message_id'] = message.message_id


def close(update, context):
    query = update.callback_query
    try:
        context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
    except BadRequest:
        pass


faq_handler = MessageHandler(Filters.FaqFilter(), faq)
close_handler = CallbackQueryHandler(close, pattern='faq:close')
