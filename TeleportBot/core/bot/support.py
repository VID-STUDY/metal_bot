from telegram.ext import ConversationHandler, MessageHandler, CallbackQueryHandler, Filters as TelegramFilters
from telegram import ParseMode

from core.services import users
from core.resources import strings, keyboards, images
from .utils import Filters
from config import Config

from datetime import datetime
import pytz

SUPPORT = range(1)


def start(update, context):
    if 'has_action' in context.user_data:
        return
    context.user_data['has_action'] = True
    user_id = update.message.from_user.id
    if 'user' not in context.user_data:
        context.user_data['user'] = users.user_exists(user_id)
    language = context.user_data['user'].get('language')
    support_message = strings.get_string('support.welcome', language).format(name=context.user_data['user'].get('name'))
    support_keyboard = keyboards.get_keyboard('support.cancel', language)
    image = images.get_support_image()
    if image:
        chat_id = update.message.chat_id
        message = context.bot.send_photo(chat_id=chat_id, photo=image, caption=support_message,
                                         reply_markup=support_keyboard, parse_mode=ParseMode.HTML)
    else:
        message = update.message.reply_text(text=support_message, reply_markup=support_keyboard, parse_mode=ParseMode.HTML)
    context.user_data['support_message'] = message
    return SUPPORT


def support(update, context):
    language = context.user_data['user'].get('language')
    if update.callback_query and update.callback_query.data.split(':')[1] == 'cancel':
        canceled_message = strings.get_string('support.canceled', language)
        context.bot.delete_message(chat_id=update.callback_query.message.chat_id,
                                   message_id=update.callback_query.message.message_id)
        update.callback_query.answer(text=canceled_message, show_alert=True)
        del context.user_data['has_action']
        return ConversationHandler.END
    elif update.message:
        user_id = update.message.from_user.id
        question_text = update.message.text
        bot_info = context.bot.get_me()
        timezone = pytz.timezone('Asia/Tashkent')
        now_date = datetime.now(tz=timezone).strftime('%d %B %Y %H:%M:%S')
        support_message = strings.get_string('support.question.template', 'ru').format(bot_id=bot_info.id,
                                                                                       bot_name=bot_info.first_name,
                                                                                       user_id=user_id,
                                                                                       user_name=context.user_data[
                                                                                           'user'].get('name'),
                                                                                       date=now_date,
                                                                                       question=question_text)
        support_keyboard = keyboards.get_support_keyboard(link=(Config.APP_URL + '/users/' + str(user_id) + '/edit'))
        context.bot.send_message(chat_id=Config.TELEGRAM_SUPPORT_GROUP, text=support_message, parse_mode=ParseMode.HTML,
                                 reply_markup=support_keyboard)
        message = context.user_data['support_message']
        context.bot.delete_message(chat_id=message.chat_id, message_id=message.message_id)
        success_message = strings.get_string('support.success', language)
        update.message.reply_text(text=success_message)
        del context.user_data['has_action']
        return ConversationHandler.END
    else:
        return SUPPORT


support_conversation = ConversationHandler(
    entry_points=[MessageHandler(Filters.SupportFilter(), start)],
    states={
        SUPPORT: [MessageHandler(TelegramFilters.text, support), CallbackQueryHandler(support)]
    },
    fallbacks=[MessageHandler(TelegramFilters.text, '')]
)
