from telegram import Update, ParseMode
from telegram.ext import MessageHandler, CallbackQueryHandler, CallbackContext
from core.resources import strings, keyboards
from core.services import users
from .utils import Navigation, Filters


def select_role_choice(update: Update, context):
    query = update.callback_query
    role = query.data.split(':')[1]
    user = users.set_user_role(query.from_user.id, role)
    context.user_data['user'] = user
    if 'mode' in context.user_data and context.user_data['mode'] == 'catalog':
        if user.get('user_role') == 'employer':
            user_vacations(update, context)
        if user.get('user_role') == 'contractor':
            user_resumes(update, context)
        return
    Navigation.to_account(update, context)
    query.answer(text=strings.get_string('account.select_role.selected', context.user_data['user'].get('language')))


def start(update: Update, context):
    user = update.message.from_user
    user = users.user_exists(user.id)
    if not user:
        return
    context.user_data['user'] = user
    if user.get('is_blocked'):
        blocked_message = strings.get_string('blocked', user.get('language'))
        update.message.reply_text(blocked_message)
        return
    if user.get('user_role'):
        Navigation.to_account(update, context)
    else:
        select_role_message = strings.get_string('account.select_role', user.get('language'))
        select_role_keyboard = keyboards.get_keyboard('account.select_role', user.get('language'))
        update.message.reply_text(select_role_message, parse_mode=ParseMode.HTML, reply_markup=select_role_keyboard)


def change_role(update, context):
    context.user_data['user'] = users.user_exists(update.callback_query.from_user.id)
    if context.user_data['user'].get('is_blocked'):
        blocked_message = strings.get_string('blocked', context.user_data['user'].get('language'))
        update.callback_query.answer(text=blocked_message, show_alert=True)
        return
    query = update.callback_query
    query.answer()
    language = context.user_data['user'].get('language')
    select_role_message = strings.get_string('account.select_role', language)
    select_role_keyboard = keyboards.get_keyboard('account.select_role', language)
    if 'mode' in context.user_data and context.user_data['mode'] == 'catalog':
        query.edit_message_text(select_role_message, parse_mode=ParseMode.HTML, reply_markup=select_role_keyboard)
        return
    query.edit_message_caption(select_role_message, parse_mode=ParseMode.HTML, reply_markup=select_role_keyboard)


def change_language(update, context):
    context.user_data['user'] = users.user_exists(update.callback_query.from_user.id)
    if context.user_data['user'].get('is_blocked'):
        blocked_message = strings.get_string('blocked', context.user_data['user'].get('language'))
        update.callback_query.answer(text=blocked_message, show_alert=True)
        return
    query = update.callback_query
    query.answer()
    language = context.user_data['user'].get('language')
    change_language_message = strings.get_string('account.select_language', language)
    keyboard = keyboards.get_keyboard('account.language', language)
    query.edit_message_caption(change_language_message, reply_markup=keyboard)


def select_language(update, context):
    query = update.callback_query
    language = query.data.split(':')[1]
    if language == 'back':
        Navigation.to_account(update, context)
        return
    user = users.change_language(context.user_data['user'].get('id'), language)
    context.user_data['user'] = user
    success_message = strings.get_string('account.select_language.success', language)
    query.answer(text=success_message)
    Navigation.to_account(update, context)


def user_resumes(update, context):
    context.user_data['user'] = users.user_exists(update.callback_query.from_user.id)
    if context.user_data['user'].get('is_blocked'):
        blocked_message = strings.get_string('blocked', context.user_data['user'].get('language'))
        update.callback_query.answer(text=blocked_message, show_alert=True)
        return
    language = context.user_data['user'].get('language')
    query = update.callback_query
    query.answer()
    user_id = query.from_user.id
    resumes = users.get_user_resumes(user_id)
    keyboard = keyboards.get_resumes_keyboard(resumes, language)
    message = strings.get_string('resumes.list', language)
    context.bot.delete_message(chat_id=user_id, message_id=query.message.message_id)
    context.bot.send_message(chat_id=user_id, text=message, reply_markup=keyboard, parse_mode=ParseMode.HTML)


def user_vacations(update, context):
    context.user_data['user'] = users.user_exists(update.callback_query.from_user.id)
    if context.user_data['user'].get('is_blocked'):
        blocked_message = strings.get_string('blocked', context.user_data['user'].get('language'))
        update.callback_query.answer(text=blocked_message, show_alert=True)
        return
    language = context.user_data['user'].get('language')
    query = update.callback_query
    user_id = query.from_user.id
    vacations = users.get_user_vacations(user_id)
    keyboard = keyboards.get_vacations_keyboard(vacations, language)
    message = strings.get_string('vacations.list', language)
    context.bot.delete_message(chat_id=user_id, message_id=query.message.message_id)
    context.bot.send_message(chat_id=user_id, text=message, reply_markup=keyboard, parse_mode=ParseMode.HTML)


def account_settings(update: Update, context: CallbackContext):
    context.user_data['user'] = users.user_exists(update.callback_query.from_user.id)
    language = context.user_data['user'].get('language')
    query = update.callback_query
    settings_keyboard = keyboards.get_keyboard('account.settings', language)
    query.edit_message_reply_markup(settings_keyboard)


def account_settings_back(update: Update, context: CallbackContext):
    context.user_data['user'] = users.user_exists(update.callback_query.from_user.id)
    query = update.callback_query
    account_keyboard = keyboards.get_account_keyboard(context.user_data['user'])
    query.edit_message_reply_markup(account_keyboard)


account_handler = MessageHandler(Filters.AccountFilter(), start)
account_settings_handler = CallbackQueryHandler(account_settings, pattern='account:settings')
account_settings_back_handler = CallbackQueryHandler(account_settings_back, pattern='settings:back')
select_role_choice_handler = CallbackQueryHandler(select_role_choice, pattern='^role:.*')
change_role_handler = CallbackQueryHandler(change_role, pattern='account:role')
user_resumes_handler = CallbackQueryHandler(user_resumes, pattern='account:resumes')
user_vacations_handler = CallbackQueryHandler(user_vacations, pattern='account:my_vacations')
language_handler = CallbackQueryHandler(change_language, pattern='account:language')
select_language_handler = CallbackQueryHandler(select_language, pattern=r'^languages:.*')
