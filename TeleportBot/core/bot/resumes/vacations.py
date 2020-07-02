from telegram import ParseMode
from telegram.ext import ConversationHandler

from core.services import users, resumes
from core.resources import strings, keyboards
from core.bot.utils import Navigation


LIST, VACATIONS = range(2)


def resumes_list(update, context):
    context.user_data['user'] = users.user_exists(update.callback_query.from_user.id)
    if context.user_data['user'].get('is_blocked'):
        blocked_message = strings.get_string('blocked', context.user_data['user'].get('language'))
        update.callback_query.answer(text=blocked_message, show_alert=True)
        return ConversationHandler.END
    context.user_data['has_action'] = True
    query = update.callback_query
    language = context.user_data['user'].get('language')
    user_id = context.user_data['user'].get('id')
    user_resumes = users.get_user_resumes(user_id)
    if len(user_resumes) == 0:
        empty_message = strings.get_string('resumes.empty_list', language)
        query.answer(text=empty_message, show_alert=True)
        del context.user_data['has_action']
        return ConversationHandler.END
    list_message = strings.get_string('resumes.vacations.select', language)
    list_keyboard = keyboards.get_resumes_keyboard(user_resumes, language, include_create_button=False)
    context.bot.delete_message(chat_id=user_id, message_id=query.message.message_id)
    context.bot.send_message(chat_id=user_id, text=list_message, reply_markup=list_keyboard, parse_mode=ParseMode.HTML)
    return LIST


def vacations_for_resume(update, context):
    context.user_data['user'] = users.user_exists(update.callback_query.from_user.id)
    if context.user_data['user'].get('is_blocked'):
        blocked_message = strings.get_string('blocked', context.user_data['user'].get('language'))
        update.callback_query.answer(text=blocked_message, show_alert=True)
        return ConversationHandler.END
    query = update.callback_query
    language = context.user_data['user'].get('language')
    resume_id = query.data.split(':')[1]
    if resume_id == 'back':
        Navigation.to_account(update, context)
        del context.user_data['has_action']
        return ConversationHandler.END
    vacations = resumes.get_vacations_for_resume(resume_id)
    if len(vacations) == 0:
        empty_message = strings.get_string('resumes.vacations.empty', language)
        query.answer(text=empty_message, show_alert=True)
        return LIST
    if type(vacations) is dict:
        vacations = list(vacations.values())
    context.user_data['found_vacations'] = vacations
    context.user_data['current_page'] = 1
    first_vacation = vacations[0]
    user = users.user_exists(first_vacation.get('user_id'))
    vacation_message = strings.from_vacation(first_vacation, language, for_resume=True, user=user)
    vacations_keyboard = keyboards.get_list_paginated_keyboard(vacations, language)
    query.edit_message_text(text=vacation_message, reply_markup=vacations_keyboard, parse_mode=ParseMode.HTML)
    return VACATIONS


def paginated_vacations(update, context):
    query = update.callback_query
    language = context.user_data['user'].get('language')
    page = query.data.split(':')[1]
    if page == 'back':
        user_id = context.user_data['user'].get('id')
        user_resumes = users.get_user_resumes(user_id)
        list_message = strings.get_string('resumes.vacations.select', language)
        list_keyboard = keyboards.get_resumes_keyboard(user_resumes, language, include_create_button=False)
        query.edit_message_text(text=list_message, reply_markup=list_keyboard)
        return LIST
    if int(page) == context.user_data['current_page']:
        return VACATIONS
    vacation = context.user_data['found_vacations'][int(page) - 1]
    user = users.user_exists(vacation.get('user_id'))
    vacation_message = strings.from_vacation(vacation, language, for_resume=True, user=user)
    vacations_keyboard = keyboards.get_list_paginated_keyboard(context.user_data['found_vacations'],
                                                               language, current_page=int(page))
    query.edit_message_text(text=vacation_message, reply_markup=vacations_keyboard, parse_mode=ParseMode.HTML)
    context.user_data['current_page'] = int(page)
    return VACATIONS
