import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from config import Config
from core.bot import start, account, resumes, vacations, payments
from core.resources import strings

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)
    error_message = strings.get_string('error', language='ru')
    if update.callback_query:
        update.callback_query.answer(text=error_message, show_alert=True)
    else:
        update.message.reply_text(text=error_message)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(Config.API_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    dp.add_handler(start.conversation_handler)
    dp.add_handler(account.account_handler)
    dp.add_handler(account.select_role_choice_handler)
    dp.add_handler(account.change_role_handler)
    dp.add_handler(account.user_resumes_handler)
    dp.add_handler(account.user_vacations_handler)
    dp.add_handler(resumes.resume_back_handler)
    dp.add_handler(resumes.create_resume_conversation)
    dp.add_handler(resumes.action_resume_conversation)
    dp.add_handler(vacations.create_vacation_conversation)
    dp.add_handler(vacations.action_vacation_conversation)
    dp.add_handler(vacations.vacation_back_handler)
    dp.add_handler(resumes.resume_vacations_conversation)
    dp.add_handler(payments.payments_conversation)
    dp.add_handler(payments.pre_checkout_handler)
    dp.add_handler(payments.successful_payment_handler)

    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    if Config.ENVIRONMENT == 'production':
        updater.start_webhook(listen='0.0.0.0',
                              port=8443,
                              url_path=Config.API_TOKEN)
        updater.bot.set_webhook(webhook_url=Config.APP_URL + '/' + Config.API_TOKEN)
    else:
        updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
