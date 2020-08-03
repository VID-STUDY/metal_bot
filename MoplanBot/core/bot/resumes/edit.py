from telegram import ParseMode
from telegram.ext import ConversationHandler
from core.resources import strings, keyboards
from core.bot.utils import Navigation
from core.services import resumes, users


UPDATE_RESUME, RESUME_ACTION, EDIT_ACTION = range(3)


def resume(update, context):
    context.user_data['user'] = users.user_exists(update.callback_query.from_user.id)
    if context.user_data['user'].get('is_blocked'):
        blocked_message = strings.get_string('blocked', context.user_data['user'].get('language'))
        update.callback_query.answer(text=blocked_message, show_alert=True)
        return ConversationHandler.END
    context.user_data['has_action'] = True
    language = context.user_data['user'].get('language')
    query = update.callback_query
    resume_id = query.data.split(':')[1]
    resume = resumes.get_resume(resume_id)
    context.user_data['editing_resume'] = resume
    resume_message = strings.from_resume(resume, language)
    resume_keyboard = keyboards.get_keyboard('resume', language)
    query.edit_message_text(text=resume_message, reply_markup=resume_keyboard)
    return RESUME_ACTION


def resume_action(update, context):
    context.user_data['user'] = users.user_exists(update.callback_query.from_user.id)
    if context.user_data['user'].get('is_blocked'):
        blocked_message = strings.get_string('blocked', context.user_data['user'].get('language'))
        update.callback_query.answer(text=blocked_message, show_alert=True)
        return ConversationHandler.END
    language = context.user_data['user'].get('language')
    query = update.callback_query
    data = query.data
    if data == 'edit':
        return edit(update, context)
    elif data == 'delete':
        return delete(update, context)
    elif data == 'back':
        user_id = query.from_user.id
        user_resumes = users.get_user_resumes(user_id)
        keyboard = keyboards.get_resumes_keyboard(user_resumes, language)
        message = strings.get_string('resumes.list', language)
        query.edit_message_text(message, parse_mode=ParseMode.HTML, reply_markup=keyboard)
        del context.user_data['has_action']
        return ConversationHandler.END
    else:
        return RESUME_ACTION


def edit(update, context):
    query = update.callback_query
    language = context.user_data['user'].get('language')
    message = strings.get_string('resumes.edit', language).format(context.user_data['editing_resume'].get('title'))
    edit_keyboard = keyboards.get_keyboard('resume.edit', language)
    query.edit_message_text(text=message, reply_markup=edit_keyboard, parse_mode=ParseMode.HTML)
    return EDIT_ACTION


def edit_action(update, context):
    context.user_data['user'] = users.user_exists(update.callback_query.from_user.id)
    if context.user_data['user'].get('is_blocked'):
        blocked_message = strings.get_string('blocked', context.user_data['user'].get('language'))
        update.callback_query.answer(text=blocked_message, show_alert=True)
        return ConversationHandler.END
    query = update.callback_query
    data = query.data
    language = context.user_data['user'].get('language')
    if data == 'title':
        message = strings.get_string('resumes.edit.title', language)
    elif data == 'price':
        message = strings.get_string('resumes.edit.price', language)
    elif data == 'name':
        message = strings.get_string('resumes.edit.name', language)
    elif data == 'contacts':
        message = strings.get_string('resumes.edit.contacts', language)
    elif data == 'back':
        resume_message = strings.from_resume(context.user_data['editing_resume'], language)
        resume_keyboard = keyboards.get_keyboard('resume', language)
        query.edit_message_text(text=resume_message, reply_markup=resume_keyboard)
        return RESUME_ACTION
    else:
        return EDIT_ACTION
    keyboard = keyboards.get_keyboard('go_back', language)
    context.user_data['editing_resume_step'] = data
    context.bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
    context.bot.send_message(chat_id=query.message.chat.id, text=message, reply_markup=keyboard,
                             parse_mode=ParseMode.HTML)
    return UPDATE_RESUME


def update_resume(update, context):
    message = update.message
    language = context.user_data['user'].get('language')

    def go_back():
        resume_message = strings.get_string('resumes.edit', language).format(
            context.user_data['editing_resume'].get('title'))
        Navigation.to_main_menu(update, language, user_name=context.user_data['user'].get('name'))
        edit_keyboard = keyboards.get_keyboard('resume.edit', language)
        message.reply_text(text=resume_message, reply_markup=edit_keyboard, parse_mode=ParseMode.HTML)
        return EDIT_ACTION

    if strings.get_string('go_back', language) in message.text:
        return go_back()
    payload = {context.user_data['editing_resume_step']: message.text}
    context.user_data['editing_resume'] = resumes.update_resume(context.user_data['editing_resume']['id'], payload)
    success_message = strings.get_string('success', language)
    menu_keyboard = keyboards.get_keyboard('menu', language)
    message.reply_text(text=success_message, reply_markup=menu_keyboard)
    return go_back()


def delete(update, context):
    query = update.callback_query
    language = context.user_data['user'].get('language')
    resumes.delete_resume(context.user_data['editing_resume'].get('id'))
    success = strings.get_string('success', language)
    query.answer(text=success)
    user_id = query.from_user.id
    user_resumes = users.get_user_resumes(user_id)
    keyboard = keyboards.get_resumes_keyboard(user_resumes, language)
    message = strings.get_string('resumes.list', language)
    query.edit_message_text(message, parse_mode=ParseMode.HTML, reply_markup=keyboard)
    del context.user_data['has_action']
    return ConversationHandler.END
