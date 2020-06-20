from config import Config
from core.resources import strings, keyboards
from core.services import users, referral

from telegram.error import BadRequest
from telegram import ParseMode
from telegram.ext import MessageHandler
from telegram.utils import helpers
from .utils import Filters


def start(update, context):
    message = update.message
    user_id = message.from_user.id
    if 'user' not in context.user_data:
        context.user_data['user'] = users.user_exists(user_id)
    check_channel(update, context)


def check_channel(update, context):
    if update.message:
        user_id = update.message.from_user.id
    else:
        user_id = update.callback_query.from_user.id
    language = context.user_data['user'].get('language')
    try:
        context.bot.get_chat_member(chat_id=Config.TELEGRAM_CHANNEL_USERNAME, user_id=user_id)
    except BadRequest as error:
        if error.message == 'User not found':
            if update.message:
                channel = context.bot.get_chat(chat_id=Config.TELEGRAM_CHANNEL_USERNAME)
                channel_message = strings.get_string('referral.channel', language).format(channelName=channel.title)
                channel_keyboard = keyboards.get_channel_keyboard(Config.TELEGRAM_CHANNEL_LINK, language)
                update.message.reply_text(text=channel_message, reply_markup=channel_keyboard, parse_mode=ParseMode.HTML)
            else:
                error_message = strings.get_string('referral.channel.empty', language)
                update.callback_query.answer(text=error_message, show_alert=True)
        else:
            raise error
    else:
        referral_tender = referral.get_current_referral_tender()
        if not referral_tender:
            not_exist_message = strings.get_string('referral.not_exist', language)
            if update.message:
                update.message.reply_text(text=not_exist_message)
            else:
                update.callback_query.answer(text=not_exist_message, show_alert=True)
                context.bot.delete_message(chat_id=update.callback_query.message.chat.id,
                                           message_id=update.callback_query.message.message_id)
            return
        invited_users = referral.get_invited_users(user_id, referral_tender.get('id'))
        link = helpers.create_deep_linked_url(context.bot.get_me().username, str(user_id))
        referral_message = strings.from_referral_tender(referral_tender, language, len(invited_users), link)
        referral_keyboard = keyboards.get_keyboard('referral', language)
        if update.message:
            update.message.reply_text(text=referral_message, reply_markup=referral_keyboard, parse_mode=ParseMode.HTML)
        else:
            update.callback_query.edit_message_text(text=referral_message, reply_markup=referral_keyboard,
                                                    parse_mode=ParseMode.HTML)


referral_handler = MessageHandler(Filters.ReferralFilter(), start)
