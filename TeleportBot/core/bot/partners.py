from telegram import ParseMode
from telegram.ext import MessageHandler
from telegram.error import BadRequest

from core.resources import utils, images, strings
from core.services import settings, users
from .utils import Filters


def partners(update, context):
    context.user_data['user'] = users.user_exists(update.message.from_user.id)
    if context.user_data['user'].get('is_blocked'):
        blocked_message = strings.get_string('blocked', context.user_data['user'].get('language'))
        update.message.reply_text(blocked_message)
        return
    if context.user_data['user'].get('language') == 'uz':
        partners_message = settings.get_settings().get('partners_uz')
    else:
        partners_message = settings.get_settings().get('partners')
    partners_message = utils.replace_new_line(partners_message)
    image = images.get_partners_image(context.user_data['user'].get('language'))
    photo_message = None
    if image:
        chat_id = update.message.chat_id
        image = images.get_partners_image(context.user_data['user'].get('language'))
        photo_message = context.bot.send_photo(chat_id=chat_id, photo=image)
        message = context.bot.send_message(chat_id=chat_id, text=partners_message, parse_mode=ParseMode.HTML)
    else:
        message = update.message.reply_text(text=partners_message, parse_mode=ParseMode.HTML)
    if 'partners_message_id' in context.user_data:
        try:
            context.bot.delete_message(chat_id=update.message.chat_id,
                                       message_id=context.user_data['partners_message_id'])
        except BadRequest:
            pass
    if 'partners_photo_id' in context.user_data:
        try:
            context.bot.delete_message(chat_id=update.message.chat_id,
                                       message_id=context.user_data['partners_photo_id'])
        except BadRequest:
            pass
    context.user_data['partners_message_id'] = message.message_id
    if photo_message:
        context.user_data['partners_photo_id'] = photo_message.message_id


partners_handler = MessageHandler(Filters.PartnersFilter(), partners)
