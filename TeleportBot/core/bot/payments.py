from telegram.ext import ConversationHandler, CallbackQueryHandler, MessageHandler, Filters, PreCheckoutQueryHandler
from telegram import LabeledPrice, ParseMode

from core.resources import strings, keyboards
from .utils import Navigation, Notifications, Filters as CustomFilters
from config import Config
from core.services import users, settings, resumes, vacations, categories
from . import about, account, faq, news, support, referral, start as bot_start

import secrets
import re


TARIFFS, PROVIDER, PRE_CHECKOUT = range(3)


def start(update, context):
    context.user_data['user'] = users.user_exists(update.callback_query.from_user.id)
    if context.user_data['user'].get('is_blocked'):
        blocked_message = strings.get_string('blocked', context.user_data['user'].get('language'))
        update.callback_query.answer(text=blocked_message, show_alert=True)
        return ConversationHandler.END
    context.user_data['has_action'] = True
    query = update.callback_query
    language = context.user_data['user'].get('language')
    config = settings.get_settings()
    context.user_data['settings'] = config
    payment_message = strings.payments_string(config, context.user_data['user'].get('user_role'), language)
    payment_keyboard = keyboards.get_keyboard('payments.' + context.user_data['user'].get('user_role'), language)
    query.answer()
    context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)
    context.bot.send_message(chat_id=query.message.chat_id, text=payment_message,
                             reply_markup=payment_keyboard, parse_mode=ParseMode.HTML)
    return TARIFFS


def tariffs(update, context):
    query = update.callback_query
    language = context.user_data['user'].get('language')
    tariff = query.data.split(':')[1]
    if tariff == 'back':
        if 'resume' in context.user_data or 'vacation' in context.user_data:
            if 'resume' in context.user_data:
                from .resumes.create import to_parent_categories
                to_parent_categories(query, context)
                return 8
            if 'vacation' in context.user_data:
                from .vacations.create import to_parent_categories
                to_parent_categories(query, context)
                return 10
        else:
            Navigation.to_main_menu(update, language, context=context)
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
    go_back_keyboard = keyboards.get_keyboard('go_back.one_time', language)
    payment_message = strings.get_string('payments.message', language)
    keyboard_message = context.bot.send_message(chat_id=chat_id, text=payment_message, reply_markup=go_back_keyboard)
    invoice_message = context.bot.send_invoice(chat_id, title, description, payload, provider_token, start_parameter,
                                               currency, prices)
    context.user_data['invoice_message_id'] = invoice_message.message_id
    context.user_data['keyboard_message_id'] = keyboard_message.message_id
    return PRE_CHECKOUT


def pre_checkout_callback(update, context):
    language = context.user_data['user'].get('language')
    if update.message:
        if strings.get_string('go_back', language) in update.message.text:
            context.bot.delete_message(chat_id=update.message.chat_id, message_id=context.user_data['invoice_message_id'])
            context.bot.delete_message(chat_id=update.message.chat_id, message_id=context.user_data['keyboard_message_id'])
            provider_message = strings.get_string('payments.providers', language)
            providers_keyboard = keyboards.get_keyboard('payments.providers', language)
            context.bot.send_message(chat_id=update.message.chat_id, text=provider_message,
                                     reply_markup=providers_keyboard)
            return PROVIDER
        context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
        return PRE_CHECKOUT
    query = update.pre_checkout_query
    context.user_data['user'] = users.user_exists(update.query.from_user.id)
    if context.user_data['user'].get('is_blocked'):
        query.answer(ok=False, error_message=strings.get_string('blocked', language))
        del context.user_data['has_action']
        return ConversationHandler.END
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
    update.message.reply_text(strings.get_string('vacations.create.success', language), reply_markup=menu_keyboard)
    if context.user_data['user'].get('is_blocked'):
        blocked_message = strings.get_string('blocked', context.user_data['user'].get('language'))
        update.message.reply_text(blocked_message)
        return
    if 'resume' in context.user_data:
        result = resumes.create_resume(context.user_data['resume'])
        resume = result.get('resume')
        context.user_data['user'] = resume.get('user')
        help_message = strings.get_string('resumes.create.success.help', language)
        update.message.reply_text(help_message, parse_mode=ParseMode.HTML)
        notifiable_users = result.get('notifyUsers')
        Notifications.notify_users_new_item(context.bot, notifiable_users, 'resumes.notify.new')
        del context.user_data['resume']
    if 'vacation' in context.user_data:
        result = vacations.create_vacation(context.user_data['vacation'])
        vacation = result.get('vacation')
        context.user_data['user'] = vacation.get('user')
        help_message = strings.get_string('vacations.create.success.help', language)
        update.message.reply_text(help_message, parse_mode=ParseMode.HTML)
        Notifications.notify_users_new_item(context.bot, result.get('notifyUsers'), 'vacations.notify.new')
        del context.user_data['vacation']
    del context.user_data['has_action']
    Navigation.to_account(update, context)


def main_menu_handler(update, context):
    if CustomFilters.AboutFilter().filter(update.message):
        about.about(update, context)
    elif CustomFilters.FaqFilter().filter(update.message):
        faq.faq(update, context)
    elif CustomFilters.ReferralFilter().filter(update.message):
        referral.start(update, context)
    elif CustomFilters.AccountFilter().filter(update.message):
        account.start(update, context)
        return ConversationHandler.END
    elif CustomFilters.SupportFilter().filter(update.message):
        support.support_conversation.handle_update(update, context.dispatcher,
                                                   support.support_conversation.check_update(update), context)
        support.start(update, context)
        return ConversationHandler.END
    elif CustomFilters.NewsFilter().filter(update.message):
        news.news(update, context)
    elif '/start' in update.message.text:
        bot_start.referral_start(update, context)
        return ConversationHandler.END
    else:
        context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
        return
    return ConversationHandler.END


payments_conversation = ConversationHandler(
    entry_points=[CallbackQueryHandler(start, pattern='account:balance')],
    states={
        TARIFFS: [CallbackQueryHandler(tariffs), MessageHandler(Filters.text, main_menu_handler)],
        PROVIDER: [CallbackQueryHandler(providers), MessageHandler(Filters.text, main_menu_handler)],
        PRE_CHECKOUT: [PreCheckoutQueryHandler(pre_checkout_callback),
                       MessageHandler(Filters.text, pre_checkout_callback),
                       MessageHandler(Filters.text, main_menu_handler)]
    },
    fallbacks=[
        account.account_handler,
        referral.referral_handler,
        faq.faq_handler,
        about.about_handler,
        support.support_conversation,
        news.news_handler
    ]
)

pre_checkout_handler = PreCheckoutQueryHandler(pre_checkout_callback)
successful_payment_handler = MessageHandler(Filters.successful_payment, successful_payment_callback)
