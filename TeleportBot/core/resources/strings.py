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
    if user.get('balance'):
        balance = str(user.get('balance'))
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


def from_resume(resume: dict, language: str) -> str:
    template = get_string('resumes.template', language)
    categories_string = ''
    for category in resume['categories']:
        categories_string += category.get(language + '_title') + '\n'
    if resume.get('location') == 'all':
        location = get_string('location.regions.all', language)
    else:
        region, city = resume.get('location').split('.')
        region_name = get_string('location.regions.' + region, language)
        city_name = get_city_from_region(region, city, language)
        location = region_name + ', ' + city_name
    return template.format(date=resume.get('created_at'), title=resume.get('title'),
                           description=resume.get('description'), contacts=resume.get('contacts'),
                           location=location, categories=categories_string)


def from_vacation(vacation: dict, language: str, for_resume=False) -> str:
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
        return template.format(date=vacation.get('created_at'), title=vacation.get('title'),
                               salary=vacation.get('salary'), category=vacation.get('category'),
                               description=vacation.get('description'), contacts=vacation.get('contacts'),
                               location=location)
    else:
        categories_string = ''
        for category in vacation['categories']:
            categories_string += category.get(language + '_title') + '\n'
        return template.format(date=vacation.get('created_at'), title=vacation.get('title'),
                               salary=vacation.get('salary'), category=vacation.get('category'),
                               description=vacation.get('description'), contacts=vacation.get('contacts'),
                               location=location, categories=categories_string)
