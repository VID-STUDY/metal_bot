from telegram import ParseMode
from telegram.ext import ConversationHandler
from core.resources import strings, keyboards, images
from core.bot.utils import Navigation, Notifications
from core.services import categories, vacations, settings, users
from core.bot import payments

TARIFFS, PROVIDER, PRE_CHECKOUT, HISTORY, TITLE, PRICE, NAME, CONTACTS, REGION, CITY, CATEGORIES = range(11)


def to_parent_categories(query, context):
    parent_categories = categories.get_parent_categories()
    parent_categories = sorted(parent_categories, key=lambda i: i['position'])
    language = context.user_data['user'].get('language')
    message = strings.get_string('vacations.create.categories', language)
    keyboard = keyboards.get_parent_categories_keyboard(parent_categories, language)
    query.answer()
    message = query.edit_message_text(message, reply_markup=keyboard)
    context.user_data['categories_message_id'] = message.message_id
    return CATEGORIES


def from_location_to_contacts(update, context):
    language = context.user_data['user'].get('language')
    context.bot.delete_message(chat_id=update.callback_query.message.chat_id,
                               message_id=context.user_data['location_message_id'])
    message = strings.get_string('vacations.create.contacts', language)
    keyboard = keyboards.get_keyboard('go_back.inline', language)
    context.bot.send_message(chat_id=update.callback_query.message.chat_id,
                             text=message,
                             reply_markup=keyboard,
                             parse_mode=ParseMode.HTML)
    return CONTACTS


def from_categories_to_location(update, context):
    language = context.user_data['user'].get('language')
    context.bot.delete_message(chat_id=update.callback_query.from_user.id,
                               message_id=context.user_data['categories_message_id'])
    message = strings.get_string('location.regions', language)
    keyboard = keyboards.get_keyboard('location.regions', language)
    message = context.bot.send_message(chat_id=update.callback_query.from_user.id,
                                       text=message, reply_markup=keyboard)
    context.user_data['location_message_id'] = message.message_id
    return REGION


def create(update, context):
    context.user_data['user'] = users.user_exists(update.callback_query.from_user.id)
    if context.user_data['user'].get('is_blocked'):
        blocked_message = strings.get_string('blocked', context.user_data['user'].get('language'))
        update.callback_query.answer(text=blocked_message, show_alert=True)
        return ConversationHandler.END
    context.user_data['has_action'] = True
    query = update.callback_query
    context.user_data['vacation'] = {}
    context.user_data['vacation']['user_id'] = query.from_user.id
    language = context.user_data['user'].get('language')
    query.answer(text=strings.get_string('vacations.menu_has_gone', language), show_alert=True)
    message = strings.get_string('vacations.create.title', language)
    keyboard = keyboards.get_keyboard('go_back.inline', language)
    context.bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
    context.bot.send_message(chat_id=query.from_user.id, text=message, reply_markup=keyboard, parse_mode=ParseMode.HTML)
    return TITLE


def vacation_title(update, context):
    language = context.user_data['user'].get('language')
    if update.callback_query and update.callback_query.data == 'back':
        del context.user_data['vacation']
        context.bot.delete_message(update.effective_chat.id, update.effective_message.message_id)
        Navigation.to_account(update, context)
        del context.user_data['has_action']
        return ConversationHandler.END
    context.user_data['vacation']['title'] = update.message.text
    message = strings.get_string('vacations.create.price', language)
    keyboard = keyboards.get_keyboard('go_back.inline', language)
    update.message.reply_text(message, parse_mode=ParseMode.HTML, reply_markup=keyboard)
    return PRICE


def vacation_price(update, context):
    language = context.user_data['user'].get('language')
    if update.callback_query and update.callback_query.data == 'back':
        message = strings.get_string('vacations.create.title', language)
        keyboard = keyboards.get_keyboard('go_back.inline', language)
        update.сallback_query.edit_message_text(text=message, parse_mode=ParseMode.HTML, reply_markup=keyboard)
        return TITLE
    context.user_data['vacation']['price'] = update.message.text
    message = strings.get_string('vacations.create.name', language)
    keyboard = keyboards.get_keyboard('go_back.inline', language)
    update.message.reply_text(message, parse_mode=ParseMode.HTML, reply_markup=keyboard)
    return NAME


def vacation_name(update, context):
    language = context.user_data['user'].get('language')
    if update.callback_query and update.callback_query.data == 'back':
        message = strings.get_string('vacations.create.price', language)
        keyboard = keyboards.get_keyboard('go_back.inline', language)
        update.сallback_query.edit_message_text(text=message, parse_mode=ParseMode.HTML, reply_markup=keyboard)
        return PRICE
    context.user_data['vacation']['name'] = update.message.text
    message = strings.get_string('vacations.create.contacts', language)
    keyboard = keyboards.get_keyboard('go_back.inline', language)
    update.message.reply_text(message, parse_mode=ParseMode.HTML, reply_markup=keyboard)
    return CONTACTS


def vacation_contacts(update, context):
    language = context.user_data['user'].get('language')
    if update.callback_query and update.callback_query.data == 'back':
        message = strings.get_string('vacations.create.name', language)
        keyboard = keyboards.get_keyboard('go_back.inline', language)
        update.сallback_query.edit_message_text(text=message, parse_mode=ParseMode.HTML, reply_markup=keyboard)
        return NAME
    phone_number = update.message.text
    if not phone_number.startswith('+'):
        phone_number = '+' + phone_number
    context.user_data['vacation']['contacts'] = phone_number
    message = strings.get_string('location.regions', language)
    keyboard = keyboards.get_keyboard('location.regions', language)
    remove_keyboard = keyboards.get_keyboard('remove')
    remove_message = strings.get_string('remove_keyboard', language)
    removed_message = context.bot.send_message(chat_id=update.message.chat_id, text=remove_message,
                                               reply_markup=remove_keyboard, disable_notification=True)
    context.bot.delete_message(chat_id=update.message.chat_id, message_id=removed_message.message_id)
    message = update.message.reply_text(message, reply_markup=keyboard)
    context.user_data['location_message_id'] = message.message_id
    context.user_data['location_step'] = 'region'
    return REGION


def vacation_region(update, context):
    language = context.user_data['user'].get('language')
    query = update.callback_query
    region = query.data.split(':')[1]
    if region == 'all':
        context.user_data['vacation']['location'] = {}
        context.user_data['vacation']['location']['full_name'] = strings.get_string("location.regions.all", language)
        context.user_data['vacation']['location']['code'] = 'all'
        return to_parent_categories(query, context)
    region_name = strings.get_string('location.regions.' + region, language)
    context.user_data['vacation']['location'] = {}
    context.user_data['vacation']['location']['region'] = region
    keyboard = keyboards.get_cities_from_region(region, language)
    message = strings.get_string('location.select.city', language).format(region_name)
    query.edit_message_text(message, reply_markup=keyboard)
    context.user_data['location_step'] = 'city'
    return CITY


def vacation_city(update, context):
    language = context.user_data['user'].get('language')
    query = update.callback_query
    city = query.data.split(':')[1]
    if city == 'back':
        message = strings.get_string('location.regions', language)
        keyboard = keyboards.get_keyboard('location.regions', language)
        query.answer()
        query.edit_message_text(text=message, reply_markup=keyboard)
        return REGION
    region = context.user_data['vacation']['location']['region']
    city_name = strings.get_city_from_region(region, city, language)
    region_name = strings.get_string('location.regions.' + region, language)
    full_name = region_name + ', ' + city_name
    context.user_data['vacation']['location']['full_name'] = full_name
    context.user_data['vacation']['location']['code'] = region + '.' + city
    query.answer(text=full_name)
    return to_parent_categories(query, context)


def vacation_categories(update, context):
    user = context.user_data['user']
    language = user.get('language')
    query = update.callback_query
    category_id = query.data.split(':')[1]
    if category_id == 'back':
        current_category = context.user_data['current_category']
        if current_category.get('parent_id'):
            siblings_category = categories.get_siblings(current_category.get('id'))
            siblings_category = sorted(siblings_category, key=lambda i: i['position'])
            message = strings.get_category_description(current_category, language)
            keyboard = keyboards.get_categories_keyboard(siblings_category, language,
                                                         context.user_data['vacation']['categories'])
            query.answer()
            query.edit_message_text(text=message, reply_markup=keyboard)
            context.user_data['current_category'] = categories.get_category(current_category.get('parent_id'))
            return CATEGORIES
        else:
            return to_parent_categories(query, context)
    if category_id == 'save':
        context.user_data['user'] = users.user_exists(update.callback_query.from_user.id)
        if context.user_data['user'].get('is_blocked'):
            blocked_message = strings.get_string('blocked', context.user_data['user'].get('language'))
            update.callback_query.answer(text=blocked_message, show_alert=True)
            return ConversationHandler.END
        if user.get(user.get('user_role') + '_tariff') or user.get('free_actions_count') > 0:
            payment_settings = settings.get_settings()
            item_cost = payment_settings.get(user.get(user.get('user_role') + '_tariff'))
            user_balance = user.get('balance_' + user.get('user_role'))
            if user_balance is None:
                user_balance = 0
            if user_balance >= int(item_cost) or user.get('free_actions_count') > 0:
                result = vacations.create_vacation(context.user_data['vacation'])
                vacation = result.get('vacation')
                context.user_data['user'] = vacation.get('user')
                success_message = strings.get_string('vacations.create.success', language)
                help_message = strings.get_string('vacations.create.success.help', language)
                context.bot.delete_message(chat_id=query.message.chat.id, message_id=query.message.message_id)
                context.bot.send_message(chat_id=query.message.chat.id, text=success_message)
                menu_keyboard = keyboards.get_keyboard('menu', language)
                help_image = images.get_help_panel_image()
                if help_image:
                    context.bot.send_photo(chat_id=query.message.chat_id, photo=help_image, caption=help_message,
                                           parse_mode=ParseMode.HTML, reply_markup=menu_keyboard)
                else:
                    context.bot.send_message(chat_id=query.message.chat.id, text=help_message,
                                             parse_mode=ParseMode.HTML,
                                             reply_markup=menu_keyboard)
                Navigation.to_account(update, context, new_message=True)
                del context.user_data['vacation']
                del context.user_data['has_action']
                Notifications.notify_users_new_item(context.bot, result.get('notifyUsers'), 'vacations.notify.new')
                if result.get('notifyUsers'):
                    Notifications.notify_users_new_item(context.bot, [user], 'resumes.notify.new')
                return ConversationHandler.END
        empty_balance = strings.get_string('empty_balance', language)
        query.answer(text=empty_balance, show_alert=True)
        return payments.start(update, context)

    category = categories.get_category(category_id)
    children_categories = category.get('categories')
    if 'categories' not in context.user_data['vacation']:
        context.user_data['vacation']['categories'] = []
    if children_categories:
        children_categories = sorted(children_categories, key=lambda i: i['position'])
        keyboard = keyboards.get_categories_keyboard(children_categories, language,
                                                     context.user_data['vacation']['categories'])
        message = strings.get_category_description(category, language)
        query.edit_message_text(message, reply_markup=keyboard)
        context.user_data['current_category'] = category
        return CATEGORIES
    else:
        if any(d['id'] == category['id'] for d in context.user_data['vacation']['categories']):
            added = False
            context.user_data['vacation']['categories'][:] = [c for c in context.user_data['vacation']['categories'] if
                                                            c.get('id') != category.get('id')]
        else:
            if len(context.user_data['vacation']['categories']) == 10:
                limit_message = strings.get_string('categories.limit', language)
                query.answer(text=limit_message, show_alert=True)
                return CATEGORIES
            added = True
            context.user_data['vacation']['categories'].append(category)
        category_siblings = categories.get_siblings(category_id)
        category_siblings = sorted(category_siblings, key=lambda i: i['position'])
        keyboard = keyboards.get_categories_keyboard(category_siblings, language,
                                                     context.user_data['vacation']['categories'])
        message = strings.from_categories(category, context.user_data['vacation']['categories'], added, language)
        answer_message = strings.from_categories_message(category, context.user_data['vacation']['categories'], added,
                                                         language)
        query.answer(text=answer_message)
        query.edit_message_text(message, reply_markup=keyboard)
        return CATEGORIES
