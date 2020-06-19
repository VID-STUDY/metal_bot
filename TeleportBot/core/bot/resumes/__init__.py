from . import create
from . import edit
from . import vacations
from core.bot.utils import Navigation

from telegram.ext import CallbackQueryHandler, MessageHandler, Filters, ConversationHandler

create_resume_conversation = ConversationHandler(
    entry_points=[CallbackQueryHandler(create.create, pattern='resumes:create')],
    states={
        create.TITLE: [MessageHandler(Filters.text, create.resume_title)],
        create.DESCRIPTION: [MessageHandler(Filters.text, create.resume_description)],
        create.CONTACTS: [MessageHandler(Filters.text, create.resume_contacts)],
        create.REGION: [CallbackQueryHandler(create.resume_region), MessageHandler(Filters.text, create.from_location_to_contacts)],
        create.CITY: [CallbackQueryHandler(create.resume_city), MessageHandler(Filters.text, create.from_location_to_contacts)],
        create.CATEGORIES: [CallbackQueryHandler(create.resume_categories), MessageHandler(Filters.text, create.from_categories_to_location)],
        create.TARIFFS: [CallbackQueryHandler(create.payments.tariffs)],
        create.PROVIDER: [CallbackQueryHandler(create.payments.providers)]
    },
    fallbacks=[MessageHandler(Filters.text, '')]
)
action_resume_conversation = ConversationHandler(
    entry_points=[CallbackQueryHandler(edit.resume, pattern=r'^resumes:\d+$')],
    states={
        edit.RESUME_ACTION: [CallbackQueryHandler(edit.resume_action)],
        edit.EDIT_ACTION: [CallbackQueryHandler(edit.edit_action)],
        edit.UPDATE_RESUME: [MessageHandler(Filters.text, edit.update_resume)]
    },
    fallbacks=[MessageHandler(Filters.text, '')]
)
resume_back_handler = CallbackQueryHandler(Navigation.to_account, pattern='resumes:back')

resume_vacations_conversation = ConversationHandler(
    entry_points=[CallbackQueryHandler(vacations.resumes_list, pattern='account:vacations')],
    states={
        vacations.LIST: [CallbackQueryHandler(vacations.vacations_for_resume)],
        vacations.VACATIONS: [CallbackQueryHandler(vacations.paginated_vacations)]
    },
    fallbacks=[MessageHandler(Filters.text, '')]
)
