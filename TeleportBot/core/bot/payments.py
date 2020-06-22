from telegram.ext import ConversationHandler, CallbackQueryHandler, MessageHandler, Filters, PreCheckoutQueryHandler
from telegram import LabeledPrice, ParseMode

from core.resources import strings, keyboards
from .utils import Navigation
from config import Config
from core.services import users, settings, resumes, vacations

import secrets
import re


TARIFFS, PROVIDER, PRE_CHECKOUT = range(3)


def start(update, context):
    context.user_data['has_action'] = True
    query = update.callback_query
    language = context.user_data['user'].get('language')
    config = settings.get_settings()
    context.user_data['settings'] = config
    payment_message = strings.payments_string(config, context.user_data['user'].get('user_role'), language)
    payment_keyboard = keyboards.get_keyboard('payments.' + context.user_data['user'].get('user_role'), language)
    query.answer()
    query.edit_message_text(text=payment_message, reply_markup=payment_keyboard)
    return TARIFFS


def tariffs(update, context):
    query = update.callback_query
    language = context.user_data['user'].get('language')
    tariff = query.data.split(':')[1]
    if tariff == 'back':
        Navigation.to_account(update, context)
        del context.user_data['has_action']
        return ConversationHandler.END
    context.user_data['payments.tariff'] = tariff
    provider_message = strings.get_string('payments.providers', language)
    providers_keyboard = keyboards.get_keyboard('payments.providers', language)
    query.answer()
    query.edit_message_text(text=provider_message, reply_markup=providers_keyboard)
    return PROVIDER


def providers(update, context):
    query = update.callback_query
    chat_id = query.message.chat_id
    language = context.user_data['user'].get('language')
    provider = query.data.split(':')[1]
    if provider == 'back':
        payment_message = strings.payments_string(context.user_data['settings'], context.user_data['user'].get('user_role'), language)
        payment_keyboard = keyboards.get_keyboard('payments.' + context.user_data['user'].get('user_role'), language)
        query.edit_message_text(text=payment_message, reply_markup=payment_keyboard)
        return TARIFFS
    if provider == 'payme':
        provider_token = Config.TELEGRAM_PAYME_TOKEN
    elif provider == 'click':
        provider_token = Config.TELEGRAM_CLICK_TOKEN
    elif provider == 'yandex':
        provider_token = Config.TELEGRAM_YANDEX_TOKEN
    else:
        return PROVIDER
    payload = secrets.token_hex(12)
    context.user_data['payments.payload'] = payload
    title = strings.get_string('payments.tariff.' + context.user_data['payments.tariff'])
    description = strings.get_string('payments.description.' + context.user_data['user'].get('user_role'), language)
    start_parameter = 'tariff-payment'
    currency = 'UZS'
    tariff = context.user_data['payments.tariff']
    price = context.user_data['settings'].get(tariff) * int(re.search(r'\d+', tariff).group())
    context.user_data['payments.price'] = price
    prices = [LabeledPrice(strings.get_string('payments.tariff.' + context.user_data['payments.tariff']), price * 100)]
    query.answer()
    context.bot.delete_message(chat_id=chat_id, message_id=query.message.message_id)
    context.bot.send_invoice(chat_id, title, description, payload, provider_token, start_parameter, currency, prices)
    return PRE_CHECKOUT


def pre_checkout_callback(update, context):
    language = context.user_data['user'].get('language')
    if update.message:
        if strings.get_string('go_back', language) in update.message.text:
            Navigation.to_account(update, context, new_message=True)
            return ConversationHandler.END
        context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
        return PRE_CHECKOUT
    query = update.pre_checkout_query
    if query.invoice_payload == context.user_data['payments.payload']:
        query.answer(ok=True)
        return ConversationHandler.END
    else:
        query.answer(ok=False, error_message=strings.get_string('error', language))


def successful_payment_callback(update, context):
    language = context.user_data['user'].get('language')
    context.user_data['user'] = users.set_user_tariff(context.user_data['user'], context.user_data['payments.price'],
                                                      context.user_data['payments.tariff'])
    menu_keyboard = keyboards.get_keyboard('menu', language)
    update.message.reply_text(strings.get_string('success', language), reply_markup=menu_keyboard)
    if 'resume' in context.user_data:
        resumes.create_resume(context.user_data['resume'])
        help_message = strings.get_string('resumes.create.success.help', language)
        update.message.reply_text(help_message, parse_mode=ParseMode.HTML)
    if 'vacation' in context.user_data:
        vacations.create_vacation(context.user_data['vacation'])
        help_message = strings.get_string('vacations.create.success.help', language)
        update.message.reply_text(help_message, parse_mode=ParseMode.HTML)
    del context.user_data['has_action']
    Navigation.to_account(update, context)


payments_conversation = ConversationHandler(
    entry_points=[CallbackQueryHandler(start, pattern='account:balance')],
    states={
        TARIFFS: [CallbackQueryHandler(tariffs)],
        PROVIDER: [CallbackQueryHandler(providers)],
        PRE_CHECKOUT: [PreCheckoutQueryHandler(pre_checkout_callback),
                       MessageHandler(Filters.text, pre_checkout_callback)]
    },
    fallbacks=[MessageHandler(Filters.text, '')]
)

pre_checkout_handler = PreCheckoutQueryHandler(pre_checkout_callback)
successful_payment_handler = MessageHandler(Filters.successful_payment, successful_payment_callback)
