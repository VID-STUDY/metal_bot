from telegram.ext import CallbackQueryHandler


def close(update, context):
    chat_id = update.callback_query.message.chat_id
    message_id = update.callback_query.message.message_id
    context.bot.delete_message(chat_id=chat_id, message_id=message_id)


close_handler = CallbackQueryHandler(close, pattern='notify:close')
