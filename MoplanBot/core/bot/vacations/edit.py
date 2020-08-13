from telegram import ParseMode
from telegram.ext import ConversationHandler
from core.resources import strings, keyboards
from core.bot.utils import Navigation
from core.services import vacations, users


UPDATE_VACATION, VACATION_ACTION, EDIT_ACTION = range(3)


def vacation(update, context):
    context.user_data['user'] = users.user_exists(update.callback_query.from_user.id)
    if context.user_data['user'].get('is_blocked'):
        blocked_message = strings.get_string('blocked', context.user_data['user'].get('language'))
        update.callback_query.answer(text=blocked_message, show_alert=True)
        return ConversationHandler.END
    context.user_data['has_action'] = True
    language = context.user_data['user'].get('language')
    query = update.callback_query
    vacation_id = query.data.split(':')[1]
    vacation = vacations.get_vacation(vacation_id)
    context.user_data['editing_vacation'] = vacation
    vacation_message = strings.from_vacation(vacation, language)
    vacation_keyboard = keyboards.get_keyboard('vacation', language)
    query.edit_message_text(text=vacation_message, reply_markup=vacation_keyboard)
    return VACATION_ACTION


def vacation_action(update, context):
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
        user_vacations = users.get_user_vacations(user_id)
        keyboard = keyboards.get_vacations_keyboard(user_vacations, language)
        message = strings.get_string('vacations.list', language)
        query.edit_message_text(message, parse_mode=ParseMode.HTML, reply_markup=keyboard)
        del context.user_data['has_action']
        return ConversationHandler.END
    else:
        return VACATION_ACTION


def edit(update, context):
    query = update.callback_query
    language = context.user_data['user'].get('language')
    message = strings.get_string('vacations.edit', language).format(context.user_data['editing_vacation'].get('title'))
    edit_keyboard = keyboards.get_keyboard('vacation.edit', language)
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
        message = strings.get_string('vacations.edit.title', language)
    elif data == 'contacts':
        message = strings.get_string('vacations.edit.contacts', language)
    elif data == 'price':
        message = strings.get_string('vacations.edit.price', language)
    elif data == 'name':
        message = strings.get_string('vacations.edit.name', language)
    elif data == 'back':
        vacation_message = strings.from_vacation(context.user_data['editing_vacation'], language)
        vacation_keyboard = keyboards.get_keyboard('vacation', language)
        query.edit_message_text(text=vacation_message, reply_markup=vacation_keyboard)
        return VACATION_ACTION
    else:
        return EDIT_ACTION
    keyboard = keyboards.get_keyboard('go_back', language)
    context.user_data['editing_vacation_step'] = data
    context.bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
    sent_message = context.bot.send_message(chat_id=query.message.chat.id, text=message, reply_markup=keyboard,
                                            parse_mode=ParseMode.HTML)
    context.user_data['vacation_edit_message'] = sent_message.message_id
    return UPDATE_VACATION


def update_vacation(update, context):
    message = update.message

    def go_back():
        vacation_message = strings.get_string('vacations.edit', language).format(
            context.user_data['editing_vacation'].get('title'))
        edit_keyboard = keyboards.get_keyboard('vacation.edit', language)
        if 'vacation_edit_message' in context.user_data:
            context.bot.delete_message(chat_id=message.chat_id, message_id=context.user_data['vacation_edit_message'])
            del context.user_data['vacation_edit_message']
        context.bot.delete_message(chat_id=message.chat_id, message_id=message.message_id)
        message.reply_text(text=vacation_message, reply_markup=edit_keyboard, parse_mode=ParseMode.HTML)
        return EDIT_ACTION

    language = context.user_data['user'].get('language')
    if strings.get_string('go_back', language) in message.text:
        return go_back()
    payload = {context.user_data['editing_vacation_step']: message.text}
    context.user_data['editing_vacation'] = vacations.update_vacation(context.user_data['editing_vacation']['id'], payload)
    success_message = strings.get_string('success', language)
    menu_keyboard = keyboards.get_keyboard('menu', language)
    message.reply_text(text=success_message, reply_markup=menu_keyboard)
    return go_back()


def delete(update, context):
    query = update.callback_query
    language = context.user_data['user'].get('language')
    vacations.delete_vacation(context.user_data['editing_vacation'].get('id'))
    success = strings.get_string('success', language)
    query.answer(text=success)
    user_id = query.from_user.id
    user_vacations = users.get_user_vacations(user_id)
    keyboard = keyboards.get_vacations_keyboard(user_vacations, language)
    message = strings.get_string('vacations.list', language)
    query.edit_message_text(message, parse_mode=ParseMode.HTML, reply_markup=keyboard)
    del context.user_data['has_action']
    return ConversationHandler.END
