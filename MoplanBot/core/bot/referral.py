from config import Config
from core.resources import strings, keyboards, images
from core.services import users, referral

from telegram.error import BadRequest
from telegram import ParseMode, CallbackQuery, Update
from telegram.ext import MessageHandler, ConversationHandler, CallbackQueryHandler
from telegram.utils import helpers
from .utils import Filters, Navigation


RULES, PRIZE_PLACES, RATING = range(3)


def to_referral_tender(update, context):
    user_id = update.callback_query.from_user.id
    query = update.callback_query
    language = context.user_data['user'].get('language')
    invited_users = referral.get_invited_users(user_id, context.user_data['referral_tender'].get('id'))
    link = helpers.create_deep_linked_url(context.bot.get_me().username, str(user_id))
    referral_message = strings.from_referral_tender(context.user_data['referral_tender'], language, len(invited_users),
                                                    link)
    referral_keyboard = keyboards.get_keyboard('referral', language)
    query.edit_message_caption(caption=referral_message, reply_markup=referral_keyboard, parse_mode=ParseMode.HTML)
    return ConversationHandler.END


def start(update: Update, context):
    user_id = update.effective_user.id
    if 'user' not in context.user_data:
        context.user_data['user'] = users.user_exists(user_id)
    if context.user_data['user'].get('is_blocked'):
        blocked_message = strings.get_string('blocked', context.user_data['user'].get('language'))
        update.callback_query.answer(text=blocked_message, show_alert=True)
        return
    check_channel(update, context)


def check_channel(update, context):

    def no_user_in_channel():
        if update.message:
            channel = context.bot.get_chat(chat_id=Config.TELEGRAM_CHANNEL_USERNAME)
            channel_message = strings.get_string('referral.channel', language).format(channelName=channel.title)
            channel_keyboard = keyboards.get_channel_keyboard(Config.TELEGRAM_CHANNEL_LINK, language)
            update.message.reply_text(text=channel_message, reply_markup=channel_keyboard, parse_mode=ParseMode.HTML)
        else:
            error_message = strings.get_string('referral.channel.empty', language)
            update.callback_query.answer(text=error_message, show_alert=True)

    user_id = update.effective_user.id
    language = context.user_data['user'].get('language')
    try:
        user = context.bot.get_chat_member(chat_id=Config.TELEGRAM_CHANNEL_USERNAME, user_id=user_id)
        if user.status == 'left':
            no_user_in_channel()
            return
    except BadRequest as error:
        if error.message == 'User not found':
            no_user_in_channel()
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
            latest_referral_tender = referral.get_latest_tender()
            if not latest_referral_tender:
                return
            latest_referral_tender_info = strings.from_latest_referral_tender(latest_referral_tender, language)
            context.bot.send_message(chat_id=user_id, text=latest_referral_tender_info, parse_mode=ParseMode.HTML)
            return
        context.user_data['referral_tender'] = referral_tender
        invited_users = referral.get_invited_users(user_id, referral_tender.get('id'))
        link = helpers.create_deep_linked_url(context.bot.get_me().username, str(user_id))
        referral_message = strings.from_referral_tender(referral_tender, language, len(invited_users), link)
        referral_keyboard = keyboards.get_keyboard('referral', language)
        image = images.get_referral_image(language)
        if update.callback_query:
            context.bot.delete_message(chat_id=user_id, message_id=update.callback_query.message.message_id)
        if image:
            message = context.bot.send_photo(chat_id=user_id, photo=image, caption=referral_message,
                                             reply_markup=referral_keyboard, parse_mode=ParseMode.HTML)
        else:
            if update.message:
                message = update.message.reply_text(text=referral_message, reply_markup=referral_keyboard, parse_mode=ParseMode.HTML)
            else:
                message = update.callback_query.edit_message_text(text=referral_message, reply_markup=referral_keyboard,
                                                                  parse_mode=ParseMode.HTML)
        if 'referral_message_id' in context.user_data:
            try:
                context.bot.delete_message(chat_id=user_id,
                                           message_id=context.user_data['referral_message_id'])
            except BadRequest:
                pass
        context.user_data['referral_message_id'] = message.message_id


def referral_rules(update, context):
    query = update.callback_query
    language = context.user_data['user'].get('language')
    rules_message = strings.from_referral_rules(context.user_data['referral_tender'], language)
    keyboard = keyboards.get_keyboard('referral.rules', language)
    query.edit_message_caption(caption=rules_message, reply_markup=keyboard, parse_mode=ParseMode.HTML)


def prize_places(update, context):
    query = update.callback_query
    language = context.user_data['user'].get('language')
    prize_message = strings.from_referral_prize_places(context.user_data['referral_tender'], language)
    keyboard = keyboards.get_keyboard('referral.prize', language)
    query.edit_message_caption(caption=prize_message, reply_markup=keyboard, parse_mode=ParseMode.HTML)


def rating(update, context):
    query = update.callback_query
    language = context.user_data['user'].get('language')
    referral_rating = referral.get_top_referrals(context.user_data['referral_tender'].get('id'))
    rating_message = strings.from_referral_rating(referral_rating, language)
    keyboard = keyboards.get_keyboard('referral.rating', language)
    query.edit_message_caption(caption=rating_message, reply_markup=keyboard)


def close(update, context):
    query = update.callback_query
    try:
        context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
    except BadRequest:
        pass
    Navigation.to_account()


referral_handler = CallbackQueryHandler(start, pattern='account:referral')
check_channel_handler = CallbackQueryHandler(check_channel, pattern='referral:check_channel')
rules_handler = CallbackQueryHandler(referral_rules, pattern='referral:rules')
prize_handler = CallbackQueryHandler(prize_places, pattern='referral:prize')
rating_handler = CallbackQueryHandler(rating, pattern='referral:rating')
back_handler = CallbackQueryHandler(to_referral_tender, pattern='referral:back')
close_handler = CallbackQueryHandler(close, pattern='referral:close')
