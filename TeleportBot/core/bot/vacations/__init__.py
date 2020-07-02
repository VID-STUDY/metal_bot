from . import create
from . import edit
from . import resumes

from core.bot import about, account, faq, news, support, referral

from core.bot.utils import Navigation, Filters as CustomFilters

from telegram.ext import CallbackQueryHandler, MessageHandler, Filters, ConversationHandler, PreCheckoutQueryHandler


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
        support.support_conversation.handle_update(update, context.dispatcher, support.support_conversation.check_update(update), context)
        return ConversationHandler.END
    elif CustomFilters.NewsFilter().filter(update.message):
        news.news(update, context)
    else:
        context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
        return
    return ConversationHandler.END


create_vacation_conversation = ConversationHandler(
    entry_points=[CallbackQueryHandler(create.create, pattern='my_vacations:create')],
    states={
        create.TITLE: [MessageHandler(Filters.text, create.vacation_title)],
        create.SALARY: [MessageHandler(Filters.text, create.vacation_salary)],
        create.CATEGORY: [MessageHandler(Filters.text, create.vacation_category)],
        create.DESCRIPTION: [MessageHandler(Filters.text, create.vacation_description)],
        create.CONTACTS: [MessageHandler(Filters.text, create.vacation_contacts)],
        create.REGION: [CallbackQueryHandler(create.from_location_to_contacts, pattern='region:back'),
                        CallbackQueryHandler(create.vacation_region)],
        create.CITY: [CallbackQueryHandler(create.vacation_city),
                      MessageHandler(Filters.text, create.from_location_to_contacts)],
        create.CATEGORIES: [CallbackQueryHandler(create.from_categories_to_location, pattern='category:to_location'),
                            CallbackQueryHandler(create.vacation_categories)],
        create.TARIFFS: [CallbackQueryHandler(create.payments.tariffs)],
        create.PROVIDER: [CallbackQueryHandler(create.payments.providers)],
        create.PRE_CHECKOUT: [PreCheckoutQueryHandler(create.payments.pre_checkout_callback),
                              MessageHandler(Filters.text, create.payments.pre_checkout_callback)]
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

action_vacation_conversation = ConversationHandler(
    entry_points=[CallbackQueryHandler(edit.vacation, pattern=r'^my_vacations:\d+$')],
    states={
        edit.VACATION_ACTION: [CallbackQueryHandler(edit.vacation_action), MessageHandler(Filters.text, main_menu_handler)],
        edit.EDIT_ACTION: [CallbackQueryHandler(edit.edit_action), MessageHandler(Filters.text, main_menu_handler)],
        edit.UPDATE_VACATION: [MessageHandler(Filters.text, edit.update_vacation)]
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
vacation_back_handler = CallbackQueryHandler(Navigation.to_account, pattern='my_vacations:back')

vacation_resumes_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(resumes.vacations_list, pattern='account:responses')],
    states={
        resumes.LIST: [CallbackQueryHandler(resumes.resumes_for_vacation), MessageHandler(Filters.text, main_menu_handler)],
        resumes.RESUMES: [CallbackQueryHandler(resumes.paginated_resumes), MessageHandler(Filters.text, main_menu_handler)]
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
