from telegram import Update, ParseMode, CallbackQuery
from telegram.ext import CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from core.resources import strings, keyboards
from core.services import users
from .utils import Navigation, Filters

SELECT_ROLE = 1


def select_role_choice(update: Update, context):
    query = update.callback_query
    role = query.data.split(':')[1]
    user = users.set_user_role(query.from_user.id, role)
    account_info = strings.get_user_info(user)
    account_keyboard = keyboards.get_account_keyboard(user)
    query.edit_message_text(account_info, reply_markup=account_keyboard)
    query.answer(text=strings.get_string('account.select_role.selected', context.user_data.get('language')))


def start(update: Update, context):
    user = update.message.from_user
    user = users.user_exists(user.id)
    if not user:
        return
    context.user_data['language'] = user.get('language')
    if user.get('user_role'):
        account_message = strings.get_user_info(user)
        account_keyboard = keyboards.get_account_keyboard(user)
        update.message.reply_text(account_message, reply_markup=account_keyboard)
    else:
        select_role_message = strings.get_string('account.select_role', user.get('language'))
        select_role_keyboard = keyboards.get_keyboard('account.select_role', user.get('language'))
        update.message.reply_text(select_role_message, parse_mode=ParseMode.HTML, reply_markup=select_role_keyboard)
        return SELECT_ROLE


def change_role(update, context):
    query = update.callback_query
    query.answer()
    select_role_message = strings.get_string('account.select_role', context.user_data.get('language'))
    select_role_keyboard = keyboards.get_keyboard('account.select_role', context.user_data.get('language'))
    query.edit_message_text(select_role_message, parse_mode=ParseMode.HTML, reply_markup=select_role_keyboard)


account_handler = MessageHandler(Filters.AccountFilter(), start)
select_role_choice_handler = CallbackQueryHandler(select_role_choice, pattern='^role:.*')
change_role_handler = CallbackQueryHandler(change_role, pattern='account:role')
