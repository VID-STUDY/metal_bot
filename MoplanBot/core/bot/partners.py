from telegram import ParseMode
from telegram.ext import MessageHandler, CallbackQueryHandler
from telegram.error import BadRequest

from core.resources import utils, images, strings, keyboards
from core.services import settings, users
from .utils import Filters, Navigation

import os


def partners(update, context):
    context.user_data['user'] = users.user_exists(update.callback_query.from_user.id)
    if context.user_data['user'].get('is_blocked'):
        blocked_message = strings.get_string('blocked', context.user_data['user'].get('language'))
        update.callback_query.answer(text=blocked_message, show_alert=True)
        return
    bot_settings = settings.get_settings()
    language = context.user_data['user'].get('language')
    partners_keyboard = keyboards.get_keyboard('partners', language)
    if context.user_data['user'].get('language') == 'uz':
        ad_image_path = bot_settings.get('partners_ad_image_uz')
        partners_message = bot_settings.get('partners_uz')
    else:
        ad_image_path = bot_settings.get('partners_ad_image')
        partners_message = bot_settings.get('partners')
    if not partners_message:
        if context.user_data['user'].get('language') == 'uz':
            partners_message = bot_settings.get('partners_tariffs_uz')
        else:
            partners_message = bot_settings.get('partners_tariffs')
    partners_message = utils.replace_new_line(partners_message)
    if ad_image_path:
        if os.path.exists(ad_image_path):
            image = open(ad_image_path, 'rb')
        else:
            image = images.get_partners_image(context.user_data['user'].get('language'))
    else:
        image = images.get_partners_image(context.user_data['user'].get('language'))
    photo_message = None
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.callback_query.message.message_id)
    if image:
        chat_id = update.effective_message.chat_id
        photo_message = context.bot.send_photo(chat_id=chat_id, photo=image)
        message = context.bot.send_message(chat_id=chat_id, text=partners_message, parse_mode=ParseMode.HTML,
                                           reply_markup=partners_keyboard)
    else:
        message = update.effective_message.reply_text(text=partners_message, parse_mode=ParseMode.HTML,
                                            reply_markup=partners_keyboard)
    context.user_data['partners_message_id'] = message.message_id
    if photo_message:
        context.user_data['partners_photo_id'] = photo_message.message_id


def handle_tariffs(update, context):
    query = update.callback_query
    if 'user' not in context.user_data:
        context.user_data['user'] = users.user_exists(query.message.chat_id)
    if context.user_data['user'].get('language') == 'uz':
        tariffs_message = settings.get_settings().get('partners_tariffs_uz')
    else:
        tariffs_message = settings.get_settings().get('partners_tariffs')
    tariffs_message = utils.replace_new_line(tariffs_message)
    partners_keyboard = keyboards.get_keyboard('partners', context.user_data['user'].get('language'))
    try:
        query.edit_message_text(text=tariffs_message, parse_mode=ParseMode.HTML, reply_markup=partners_keyboard)
    except BadRequest:
        query.answer()
        pass


def partners_close(update, context):
    query = update.callback_query
    try:
        context.bot.delete_message(chat_id=query.message.chat_id,
                                   message_id=context.user_data['partners_message_id'])
    except BadRequest:
        pass
    try:
        context.bot.delete_message(chat_id=query.message.chat_id,
                                   message_id=context.user_data['partners_photo_id'])
    except BadRequest:
        pass
    Navigation.to_account(update, context, new_message=True)


partners_handler = CallbackQueryHandler(partners, pattern='account:partners')
tariffs_handler = CallbackQueryHandler(handle_tariffs, pattern='partners:tariffs')
close_handler = CallbackQueryHandler(partners_close, pattern='partners:close')
