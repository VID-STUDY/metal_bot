from telegram.ext import CallbackQueryHandler, ConversationHandler, CallbackContext, MessageHandler, Filters
from telegram import Update, CallbackQuery, ParseMode
from telegram.error import BadRequest

from core.resources import strings, keyboards, images
from core.services import users, categories
from core.bot.utils import Navigation, Filters as CustomFilters

from core.bot import about, account, faq, news, support, referral, start


LOCATION_REGION, LOCATION_CITY, CATEGORY, VACATIONS = range(4)


def _to_location_region(update: Update, context: CallbackContext, new_message=False):
    message = update.message
    language = context.user_data['user'].get('language')
    select_location_message = strings.get_string('location.regions', language)
    select_location_keyboard = keyboards.get_keyboard('location.regions', language)
    image = images.get_catalog_image(language)
    if new_message:
        photo_message = message.reply_photo(photo=image)
        text_message = message.reply_text(text=select_location_message, reply_markup=select_location_keyboard)
        if 'catalog_photo_id' in context.user_data:
            try:
                context.bot.delete_message(chat_id=update.message.chat_id,
                                           message_id=context.user_data['catalog_photo_id'])
            except BadRequest:
                pass
        if 'catalog_message_id' in context.user_data:
            try:
                context.bot.delete_message(chat_id=update.message.chat_id,
                                           message_id=context.user_data['catalog_message_id'])
            except BadRequest:
                pass
        context.user_data['catalog_photo_id'] = photo_message.message_id
        context.user_data['catalog_message_id'] = text_message.message_id
    else:
        update.callback_query.edit_message_text(text=select_location_message, reply_markup=select_location_keyboard)
    return LOCATION_REGION


def _to_parent_categories(query: CallbackQuery, context: CallbackContext):
    parent_categories = categories.get_parent_categories()
    parent_categories = sorted(parent_categories, key=lambda i: i['position'])
    language = context.user_data['user'].get('language')
    message = strings.get_string('catalog.categories', language)
    keyboard = keyboards.get_categories_keyboard(parent_categories, language, [])
    query.answer()
    message = query.edit_message_text(message, reply_markup=keyboard)
    context.user_data['categories_message_id'] = message.message_id
    return CATEGORY


def catalog(update: Update, context: CallbackContext):
    message = update.message
    context.user_data['user'] = users.user_exists(message.from_user.id)
    if context.user_data['user'].get('is_blocked'):
        blocked_message = strings.get_string('blocked', context.user_data['user'].get('language'))
        message.reply_text(text=blocked_message)
        return ConversationHandler.END
    context.user_data['catalog'] = {}
    return _to_location_region(update, context, new_message=True)


def catalog_location_region(update: Update, context: CallbackContext):
    language = context.user_data['user'].get('language')
    query = update.callback_query
    region = query.data.split(':')[1]
    context.user_data['catalog']['location'] = {}
    if region == 'back':
        context.bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
        if 'catalog_photo_id' in context.user_data:
            try:
                context.bot.delete_message(chat_id=query.message.chat_id,
                                           message_id=context.user_data['catalog_photo_id'])
            except BadRequest:
                pass
        del context.user_data['catalog']
        return ConversationHandler.END
    if region == 'all':
        context.user_data['catalog']['location']['code'] = region
        context.user_data['catalog']['location']['full_name'] = strings.get_string("location.regions.all", language)
        return _to_parent_categories(query, context)
    context.user_data['catalog']['location']['region'] = region
    region_name = strings.get_string('location.regions.' + region, language)
    keyboard = keyboards.get_cities_from_region(region, language)
    message = strings.get_string('location.select.city', language).format(region_name)
    query.edit_message_text(message, reply_markup=keyboard)
    return LOCATION_CITY

def catalog_location_city(update: Update, context: CallbackContext):
    language = context.user_data['user'].get('language')
    query = update.callback_query
    city = query.data.split(':')[1]
    if city == 'back':
        return _to_location_region(update, context)
    region = context.user_data['catalog']['location']['region']
    city_name = strings.get_city_from_region(region, city, language)
    region_name = strings.get_string('location.regions.' + region, language)
    full_name = region_name + ', ' + city_name
    context.user_data['catalog']['location'] = {}
    context.user_data['catalog']['location']['code'] = region + '.' + city
    context.user_data['catalog']['location']['full_name'] = full_name
    query.answer(text=full_name)
    return _to_parent_categories(query, context)


def catalog_categories(update: Update, context: CallbackContext):
    user = context.user_data['user']
    language = user.get('language')
    query = update.callback_query
    category_id = query.data.split(':')[1]
    if category_id == 'back':
        if 'current_category' not in context.user_data:
            return _to_location_region(update, context)
        current_category = context.user_data['current_category']
        if current_category.get('parent_id'):
            current_category = context.user_data['current_category']
            siblings_category = categories.get_siblings(current_category.get('id'))
            siblings_category = sorted(siblings_category, key=lambda i: i['position'])
            message = strings.get_category_description(current_category, language)
            keyboard = keyboards.get_categories_keyboard(siblings_category, language, [])
            query.answer()
            query.edit_message_text(text=message, reply_markup=keyboard)
            context.user_data['current_category'] = current_category.get('parent_category')
            return CATEGORIES
        else:
            del context.user_data['current_category']
            return _to_parent_categories(query, context)
    category = categories.get_category(category_id)
    children_categories = category.get('categories')
    if children_categories:
        context.user_data['current_category'] = category
        children_categories = sorted(children_categories, key=lambda i: i['position'])
        keyboard = keyboards.get_categories_keyboard(children_categories, language, [])
        message = strings.get_category_description(category, language)
        query.edit_message_text(message, reply_markup=keyboard)
        return CATEGORY
    vacations = category.get('vacations')
    if not vacations:
        empty_message = strings.get_string('catalog.empty', language)
        query.answer(text=empty_message, show_alert=True)
        return CATEGORY
    context.user_data['current_category'] = category
    location_code = context.user_data['catalog']['location']['code']
    if location_code != 'all':
        vacations = [vacation for vacation in vacations if vacation.get('location') == location_code or vacation.get('location') == 'all']
    vacations_message = strings.from_vacations_list_message(vacations, category, 
                                                            context.user_data['catalog']['location']['full_name'], 
                                                            len(vacations), language)
    catalog_keyboard = keyboards.get_keyboard('catalog', language)
    query.edit_message_text(vacations_message, reply_markup=catalog_keyboard, parse_mode=ParseMode.HTML)
    return VACATIONS


def catalog_vacations(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data.split(':')[1]
    user = context.user_data['user']
    language = user.get('language')
    if data == 'back':
        current_category = context.user_data['current_category']
        siblings_category = categories.get_siblings(current_category.get('id'))
        siblings_category = sorted(siblings_category, key=lambda i: i['position'])
        message = strings.get_category_description(current_category, language)
        keyboard = keyboards.get_categories_keyboard(siblings_category, language, [])
        query.answer()
        query.edit_message_text(text=message, reply_markup=keyboard)
        context.user_data['current_category'] = categories.get_category(current_category.get('parent_id'))
        return CATEGORY


def main_menu_handler(update, context):
    if CustomFilters.AboutFilter().filter(update.message):
        about.about(update, context)
    elif CustomFilters.FaqFilter().filter(update.message):
        faq.faq(update, context)
    elif CustomFilters.ReferralFilter().filter(update.message):
        referral.start(update, context)
    elif CustomFilters.CatalogFilter().filter(update.message):
        new_state = catalog(update, context)
        catalog_conversation.update_state(new_state, (update.effective_chat.id, update.effective_chat.id))
        return
    elif CustomFilters.AccountFilter().filter(update.message):
        account.start(update, context)
        if 'resume' in context.user_data:
            del context.user_data['resume']
        return ConversationHandler.END
    elif CustomFilters.SupportFilter().filter(update.message):
        support.support_conversation.handle_update(update, context.dispatcher, support.support_conversation.check_update(update), context)
        if 'resume' in context.user_data:
            del context.user_data['resume']
        return ConversationHandler.END
    elif CustomFilters.NewsFilter().filter(update.message):
        news.news(update, context)
    elif '/start' in update.message.text:
        start.referral_start(update, context)
        if 'resume' in context.user_data:
            del context.user_data['resume']
        return ConversationHandler.END
    else:
        context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)


catalog_conversation = ConversationHandler(
    entry_points=[MessageHandler(CustomFilters.CatalogFilter(), catalog)],
    states={
        LOCATION_REGION: [CallbackQueryHandler(catalog_location_region), MessageHandler(Filters.text, main_menu_handler)],
        LOCATION_CITY: [CallbackQueryHandler(catalog_location_city), MessageHandler(Filters.text, main_menu_handler)],
        CATEGORY: [CallbackQueryHandler(catalog_categories), MessageHandler(Filters.text, main_menu_handler)],
        VACATIONS: [CallbackQueryHandler(catalog_vacations), MessageHandler(Filters.text, main_menu_handler)]
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
