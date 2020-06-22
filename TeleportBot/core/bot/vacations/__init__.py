from . import create
from . import edit
from . import resumes

from core.bot.utils import Navigation

from telegram.ext import CallbackQueryHandler, MessageHandler, Filters, ConversationHandler, PreCheckoutQueryHandler


create_vacation_conversation = ConversationHandler(
    entry_points=[CallbackQueryHandler(create.create, pattern='my_vacations:create')],
    states={
        create.TITLE: [MessageHandler(Filters.text, create.vacation_title)],
        create.SALARY: [MessageHandler(Filters.text, create.vacation_salary)],
        create.CATEGORY: [MessageHandler(Filters.text, create.vacation_category)],
        create.DESCRIPTION: [MessageHandler(Filters.text, create.vacation_description)],
        create.CONTACTS: [MessageHandler(Filters.text, create.vacation_contacts)],
        create.REGION: [CallbackQueryHandler(create.vacation_region), MessageHandler(Filters.text, create.from_location_to_contacts)],
        create.CITY: [CallbackQueryHandler(create.vacation_city), MessageHandler(Filters.text, create.from_location_to_contacts)],
        create.CATEGORIES: [CallbackQueryHandler(create.vacation_categories), MessageHandler(Filters.text, create.from_categories_to_location)],
        create.TARIFFS: [CallbackQueryHandler(create.payments.tariffs)],
        create.PROVIDER: [CallbackQueryHandler(create.payments.providers)],
        create.PRE_CHECKOUT: [PreCheckoutQueryHandler(create.payments.pre_checkout_callback),
                              MessageHandler(Filters.text, create.payments.pre_checkout_callback)]
    },
    fallbacks=[MessageHandler(Filters.text, '')]
)

action_vacation_conversation = ConversationHandler(
    entry_points=[CallbackQueryHandler(edit.vacation, pattern=r'^my_vacations:\d+$')],
    states={
        edit.VACATION_ACTION: [CallbackQueryHandler(edit.vacation_action)],
        edit.EDIT_ACTION: [CallbackQueryHandler(edit.edit_action)],
        edit.UPDATE_VACATION: [MessageHandler(Filters.text, edit.update_vacation)]
    },
    fallbacks=[MessageHandler(Filters.text, '')]
)
vacation_back_handler = CallbackQueryHandler(Navigation.to_account, pattern='my_vacations:back')

vacation_resumes_handler = ConversationHandler(
    entry_points=[CallbackQueryHandler(resumes.vacations_list, pattern='account:responses')],
    states={
        resumes.LIST: [CallbackQueryHandler(resumes.resumes_for_vacation)],
        resumes.RESUMES: [CallbackQueryHandler(resumes.paginated_resumes)]
    },
    fallbacks=[MessageHandler(Filters.text, '')]
)
