from telegram import ParseMode
from telegram.ext import ConversationHandler
from core.resources import strings, keyboards
from core.bot.utils import Navigation, Notifications
from core.services import categories, resumes, settings
from core.bot import payments

TARIFFS, PROVIDER, PRE_CHECKOUT, TITLE, DESCRIPTION, CONTACTS, REGION, CITY, CATEGORIES = range(9)


def to_parent_categories(query, context):
    parent_categories = categories.get_parent_categories()
    language = context.user_data['user'].get('language')
    message = strings.get_string('resumes.create.categories', language)
    keyboard = keyboards.get_parent_categories_keyboard(parent_categories, language)
    query.answer()
    message = query.edit_message_text(message, reply_markup=keyboard)
    context.user_data['categories_message_id'] = message.message_id
    return CATEGORIES


def from_location_to_contacts(update, context):
    language = context.user_data['user'].get('language')
    if strings.get_string('go_back', language) in update.message.text:
        context.bot.delete_message(chat_id=update.message.chat.id, message_id=context.user_data['location_message_id'])
        message = strings.get_string('resumes.create.contacts', language)
        update.message.reply_text(message, parse_mode=ParseMode.HTML)
        return CONTACTS
    else:
        context.bot.delete_message(chat_id=update.message.chat.id, message_id=update.message.message_id)
        if context.user_data['location_step'] == 'region':
            return REGION
        elif context.user_data['location_step'] == 'city':
            return CITY


def from_categories_to_location(update, context):
    language = context.user_data['user'].get('language')
    if strings.get_string('go_back', language) in update.message.text:
        context.bot.delete_message(chat_id=update.message.chat.id, message_id=context.user_data['categories_message_id'])
        message = strings.get_string('location.regions', language)
        keyboard = keyboards.get_keyboard('location.regions', language)
        message = update.message.reply_text(text=message, reply_markup=keyboard)
        context.user_data['location_message_id'] = message.message_id
        return REGION
    else:
        context.bot.delete_message(chat_id=update.message.chat.id, message_id=update.message.message_id)
        return CATEGORIES


def create(update, context):
    context.user_data['has_action'] = True
    query = update.callback_query
    context.user_data['resume'] = {}
    context.user_data['resume']['user_id'] = query.from_user.id
    language = context.user_data['user'].get('language')
    query.answer(text=strings.get_string('resumes.menu_has_gone', language), show_alert=True)
    message = strings.get_string('resumes.create.title', language)
    keyboard = keyboards.get_keyboard('go_back', language)
    context.bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
    context.bot.send_message(chat_id=query.from_user.id, text=message, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    return TITLE


def resume_title(update, context):
    language = context.user_data['user'].get('language')
    if strings.get_string('go_back', language) in update.message.text:
        Navigation.to_main_menu(update, language, user_name=context.user_data['user'].get('name'))
        Navigation.to_account(update, context)
        del context.user_data['has_action']
        return ConversationHandler.END
    context.user_data['resume']['title'] = update.message.text
    message = strings.get_string('resumes.create.description', language)
    update.message.reply_text(message, parse_mode=ParseMode.HTML)
    return DESCRIPTION


def resume_description(update, context):
    language = context.user_data['user'].get('language')
    if strings.get_string('go_back', language) in update.message.text:
        message = strings.get_string('resumes.create.title', language)
        update.message.reply_text(message, parse_mode=ParseMode.HTML)
        return TITLE
    context.user_data['resume']['description'] = update.message.text
    message = strings.get_string('resumes.create.contacts', language)
    update.message.reply_text(message, parse_mode=ParseMode.HTML)
    return CONTACTS


def resume_contacts(update, context):
    language = context.user_data['user'].get('language')
    if strings.get_string('go_back', language) in update.message.text:
        message = strings.get_string('vacation.create.description', language)
        update.message.reply_text(message, parse_mode=ParseMode.HTML)
        return DESCRIPTION
    context.user_data['resume']['contacts'] = update.message.text
    message = strings.get_string('location.regions', language)
    keyboard = keyboards.get_keyboard('location.regions', language)
    message = update.message.reply_text(message, reply_markup=keyboard)
    context.user_data['location_message_id'] = message.message_id
    context.user_data['location_step'] = 'region'
    return REGION


def resume_region(update, context):
    language = context.user_data['user'].get('language')
    query = update.callback_query
    region = query.data.split(':')[1]
    if region == 'all':
        context.user_data['resume']['location'] = {}
        context.user_data['resume']['location']['full_name'] = strings.get_string("location.regions.all", language)
        context.user_data['resume']['location']['code'] = 'all'
        return to_parent_categories(query, context)
    region_name = strings.get_string('location.regions.' + region, language)
    context.user_data['resume']['location'] = {}
    context.user_data['resume']['location']['region'] = region
    keyboard = keyboards.get_cities_from_region(region, language)
    message = strings.get_string('location.select.city', language).format(region_name)
    query.edit_message_text(message, reply_markup=keyboard)
    context.user_data['location_step'] = 'city'
    return CITY


def resume_city(update, context):
    language = context.user_data['user'].get('language')
    query = update.callback_query
    city = query.data.split(':')[1]
    if city == 'back':
        message = strings.get_string('location.regions', language)
        keyboard = keyboards.get_keyboard('location.regions', language)
        query.answer()
        query.edit_message_text(text=message, reply_markup=keyboard)
        return REGION
    region = context.user_data['resume']['location']['region']
    city_name = strings.get_city_from_region(region, city, language)
    region_name = strings.get_string('location.regions.' + region, language)
    full_name = region_name + ', ' + city_name
    context.user_data['resume']['location']['code'] = region + '.' + city
    context.user_data['resume']['location']['full_name'] = full_name
    query.answer(text=full_name)
    return to_parent_categories(query, context)


def resume_categories(update, context):
    user = context.user_data['user']
    language = user.get('language')
    query = update.callback_query
    category_id = query.data.split(':')[1]
    if category_id == 'back':
        current_category = context.user_data['current_category']
        if current_category.get('parent_id'):
            siblings_category = categories.get_siblings(current_category.get('id'))
            message = strings.get_category_description(current_category, language)
            keyboard = keyboards.get_categories_keyboard(siblings_category, language,
                                                         context.user_data['resume']['categories'])
            query.answer()
            query.edit_message_text(text=message, reply_markup=keyboard)
            context.user_data['current_category'] = categories.get_category(current_category.get('parent_id'))
            return CATEGORIES
        else:
            return to_parent_categories(query, context)
    if category_id == 'save':
        if user.get(user.get('user_role')+'_tariff') or user.get('free_actions_count') > 0:
            payment_settings = settings.get_settings()
            item_cost = payment_settings.get(user.get(user.get('user_role')+'_tariff'))
            if int(user.get('balance_' + user.get('user_role'))) >= int(item_cost) or user.get('free_actions_count') > 0:
                result = resumes.create_resume(context.user_data['resume'])
                resume = result.get('resume')
                context.user_data['user'] = resume.get('user')
                success_message = strings.get_string('resumes.create.success', language)
                help_message = strings.get_string('resumes.create.success.help', language)
                context.bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
                context.bot.send_message(chat_id=query.message.chat.id, text=success_message)
                menu_keyboard = keyboards.get_keyboard('menu', language)
                context.bot.send_message(chat_id=query.message.chat.id, text=help_message, parse_mode=ParseMode.HTML,
                                         reply_markup=menu_keyboard)
                Navigation.to_account(update, context, new_message=True)
                del context.user_data['resume']
                del context.user_data['has_action']
                notifiable_users = result.get('notifyUsers')
                Notifications.notify_users_new_item(context.bot, notifiable_users, 'resumes.notify.new')
                return ConversationHandler.END
        empty_balance = strings.get_string('empty_balance', language)
        query.answer(text=empty_balance, show_alert=True)
        return payments.start(update, context)

    category = categories.get_category(category_id)
    children_categories = category.get('categories')
    if 'categories' not in context.user_data['resume']:
        context.user_data['resume']['categories'] = []
    if children_categories:
        keyboard = keyboards.get_categories_keyboard(children_categories, language,
                                                     context.user_data['resume']['categories'])
        message = strings.get_category_description(category, language)
        query.edit_message_text(message, reply_markup=keyboard)
        context.user_data['current_category'] = category
        return CATEGORIES
    else:
        if any(d['id'] == category['id'] for d in context.user_data['resume']['categories']):
            added = False
            context.user_data['resume']['categories'][:] = [c for c in context.user_data['resume']['categories'] if
                                                            c.get('id') != category.get('id')]
        else:
            if len(context.user_data['resume']['categories']) == 10:
                limit_message = strings.get_string('categories.limit', language)
                query.answer(text=limit_message, show_alert=True)
                return CATEGORIES
            added = True
            context.user_data['resume']['categories'].append(category)
        category_siblings = categories.get_siblings(category_id)
        keyboard = keyboards.get_categories_keyboard(category_siblings, language,
                                                     context.user_data['resume']['categories'])
        message = strings.from_categories(category, context.user_data['resume']['categories'], added, language)
        answer_message = strings.from_categories_message(category, context.user_data['resume']['categories'], added,
                                                         language)
        query.answer(text=answer_message)
        query.edit_message_text(message, reply_markup=keyboard)
        return CATEGORIES
