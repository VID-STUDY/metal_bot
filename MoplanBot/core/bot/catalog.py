from telegram.ext import CallbackQueryHandler, ConversationHandler, CallbackContext
from telegram import Update


LOCATION, CATEGORY, VACATION = range(3)


def catalog(update: Update, context: CallbackContext):
    query = update.callback_query
    context.user_data['user'] = users.user_exists(update.callback_query.from_user.id)
    if context.user_data['user'].get('is_blocked'):
        blocked_message = strings.get_string('blocked', context.user_data['user'].get('language'))
        update.callback_query.answer(text=blocked_message, show_alert=True)
        return ConversationHandler.END
