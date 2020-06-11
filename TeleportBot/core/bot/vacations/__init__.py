from . import create
from . import edit

from core.bot.utils import Navigation

from telegram.ext import CallbackQueryHandler, MessageHandler, Filters, ConversationHandler


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
        create.CATEGORIES: [CallbackQueryHandler(create.vacation_categories), MessageHandler(Filters.text, create.from_categories_to_location)]
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
