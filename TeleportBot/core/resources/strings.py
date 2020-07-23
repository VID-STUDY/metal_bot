import os
import json
from . import utils

_basedir = os.path.abspath(os.path.dirname(__file__))

# Load strings from json
# Russian language
_strings_ru = json.loads(open(os.path.join(_basedir, 'strings_ru.json'), 'r', encoding='utf8').read())

# Uzbek language
_strings_uz = json.loads(open(os.path.join(_basedir, 'strings_uz.json'), 'r', encoding='utf8').read())


def get_string(key, language='ru') -> str:
    if language == 'ru':
        return _strings_ru.get(key, 'no_string')
    elif language == 'uz':
        return _strings_uz.get(key, 'no_string')
    else:
        raise Exception('Invalid language')


def get_user_info(user: dict) -> str:
    user_info = get_string('account.id', user.get('language')) + str(user.get('id'))
    user_info += '\n'
    days = utils.date_difference_now(user.get('created_at')).get('days')
    user_info += get_string('account.days', user.get('language')) + str(days)
    user_info += '\n'
    if user.get('balance_' + user.get('user_role')):
        balance = str(user.get('balance_' + user.get('user_role')))
    else:
        balance = str(0)
    user_info += get_string('account.balance', user.get('language')) + balance
    user_info += '\n'
    if user.get('user_role') == 'employer':
        user_role = get_string('account.select_role.employer', user.get('language'))
    else:
        user_role = get_string('account.select_role.contractor', user.get('language'))
    user_info += get_string('account.status', user.get('language')) + user_role

    return user_info


def get_city_from_region(region_number, city_number, language):
    return get_string('location.regions.' + region_number + '.cities', language)[int(city_number)]


def get_category_description(category: dict, language) -> str:
    if category.get(language + '_description'):
        return category.get(language + '_description')
    else:
        return get_string('resumes.create.categories.select', language)


def from_categories(added_category: dict, categories: list, added: bool, language: str) -> str:
    if added:
        message = get_string('resumes.categories.selected.added', language).format(
            added_category.get(language + '_title'))
    else:
        message = get_string('resumes.categories.selected.removed', language).format(
            added_category.get(language + '_title'))
    if language == 'uz':
        message += get_string('resumes.categories.selected', language).format(10, len(categories))
    else:
        message += get_string('resumes.categories.selected', language).format(len(categories), 10)
    for i in range(len(categories)):
        item_str = get_string('resumes.categories.selected.item', language).format(i + 1, categories[i].get(
            language + '_title'))
        message += item_str
    return message


def from_categories_message(added_category: dict, categories: list, added: bool, language: str) -> str:
    if added:
        message = get_string('resumes.categories.selected.added.message', language).format(
            added_category.get(language + '_title'), len(categories), 10)
    else:
        message = get_string('resumes.categories.selected.removed.message', language).format(
            added_category.get(language + '_title'), len(categories), 10)
    return message


def from_resume(resume: dict, language: str, for_vacation=False, user=None) -> str:
    if for_vacation:
        template = get_string('resumes.template.for_vacation', language)
    else:
        template = get_string('resumes.template', language)
    if resume.get('location') == 'all':
        location = get_string('location.regions.all', language)
    else:
        region, city = resume.get('location').split('.')
        region_name = get_string('location.regions.' + region, language)
        city_name = get_city_from_region(region, city, language)
        location = region_name + ', ' + city_name
    if for_vacation:
        result = template.format(date=utils.reformat_datetime(resume.get('created_at')), title=resume.get('title'),
                                 description=resume.get('description'), contacts=resume.get('contacts'),
                                 location=location)
        result += '\n\n<a href="tg://user?id={}">'.format(user.get('id')) + get_string('open_chat', language) + '</a>'
        return result
    else:
        categories_string = ''
        for category in resume['categories']:
            categories_string += category.get(language + '_title') + '\n'
        return template.format(date=utils.reformat_datetime(resume.get('created_at')), title=resume.get('title'),
                               description=resume.get('description'), contacts=resume.get('contacts'),
                               location=location, categories=categories_string)


def from_vacation(vacation: dict, language: str, for_resume=False, user=None) -> str:
    if for_resume:
        template = get_string('vacations.template.for_resume', language)
    else:
        template = get_string('vacations.template', language)
    if vacation.get('location') == 'all':
        location = get_string('location.regions.all', language)
    else:
        region, city = vacation.get('location').split('.')
        region_name = get_string('location.regions.' + region, language)
        city_name = get_city_from_region(region, city, language)
        location = region_name + ', ' + city_name
    if for_resume:
        result = template.format(date=utils.reformat_datetime(vacation.get('created_at')), title=vacation.get('title'),
                                 salary=vacation.get('salary'), category=vacation.get('category'),
                                 description=vacation.get('description'), contacts=vacation.get('contacts'),
                                 location=location)
        result += '\n\n<a href="tg://user?id={}">'.format(user.get('id')) + get_string('open_chat', language) + '</a>'
        return result
    else:
        categories_string = ''
        for category in vacation['categories']:
            categories_string += category.get(language + '_title') + '\n'
        return template.format(date=utils.reformat_datetime(vacation.get('created_at')), title=vacation.get('title'),
                               salary=vacation.get('salary'), category=vacation.get('category'),
                               description=vacation.get('description'), contacts=vacation.get('contacts'),
                               location=location, categories=categories_string)


def from_referral_tender(referral_tender: dict, language: str, invited_users_count, referral_link: str) -> str:
    tender = referral_tender
    template = get_string('referral.template', language)
    levels = tender.get('levels')
    levels_string = ''
    for i in range(len(levels)):
        level = levels[i]
        level_string = get_string('referral.level.item', language).format(i+1, get_string('referral.level.users', language)
                                                                          .format(level.get('users_from'),
                                                                                  level.get('users_to')))
        levels_string += (level_string + '\n')
    level_rewards_string = ''
    for i in range(len(levels)):
        level = levels[i]
        level_string = get_string('referral.level.item', language).format(i+1, level.get(language + '_reward'))
        level_rewards_string += (level_string + '\n')
    return template.format(referral_levels=levels_string, invited_count=invited_users_count,
                           referral_link=referral_link, levels_rewards=level_rewards_string)


def payments_string(settings: dict, user_role: str, language: str):
    template = get_string('payments.{}.template'.format(user_role), language)
    template += '\n\n'
    template += get_string('payments.{}.1item.template'.format(user_role), language)\
        .format(settings.get('{}_tariff_1'.format(user_role)))
    template += '\n'
    template += get_string('payments.{}.2item.template'.format(user_role), language) \
        .format(settings.get('{}_tariff_2'.format(user_role)))
    template += '\n'
    template += get_string('payments.{}.3item.template'.format(user_role), language) \
        .format(settings.get('{}_tariff_3'.format(user_role)))
    return template


def from_referral_rules(referral_tender: dict, language):
    template = get_string('referral.rules.template', language)
    return template.format(total_pot=referral_tender.get('total_pot'), date_from=referral_tender.get('date_from'),
                           date_to=referral_tender.get('date_to'))


def from_referral_prize_places(referral_tender: dict, language):
    template = get_string('referral.prize.template', language)
    return template.format(utils.replace_new_line(referral_tender.get(language + '_description')))


def from_referral_rating(referral_rating: dict, language: str) -> str:
    template = get_string('referral.rating.template', language)
    rating_string = ''
    i = 1
    for name in referral_rating:
        rating_string += (get_string('referral.rating.item.template', language).format(i, name, referral_rating[name]) + '\n')
        i += 1
    return template.format(rating_string)


def from_payment_history(history: list, language) -> str:
    message = get_string('payments.history.title', language)
    message += '\n\n'
    if len(history) == 0:
        message += get_string('payments.history.empty', language)
    else:
        for i in range(len(history)):
            item = get_string('payments.history.item', language).format(number=i+1, amount=history[i]['amount'],
                                                                        date=utils.reformat_datetime(history[i]['created_at']))
            item += '\n'
            message += item
    return message


def from_latest_referral_tender(latest_referral_tender_info, language) -> str:
    tender = latest_referral_tender_info['tender']
    top_referral = latest_referral_tender_info['topReferrals']
    header = get_string('referral.latest.template', language).format(date_from=tender.get('date_from'), date_to=tender.get('date_to'))
    prize = from_referral_prize_places(tender, language)
    top = from_referral_rating(top_referral, language)
    message = header + '\n\n' + prize + '\n\n' + top
    return message

