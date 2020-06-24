from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from .strings import get_string
from typing import Union, Optional
from config import Config


def _create_keyboard(keyboard: list, one_time: bool = False) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=one_time)


_default_keyboard = _create_keyboard([['no_keyboard']])


def get_keyboard(key, language='ru') -> Union[ReplyKeyboardRemove, ReplyKeyboardMarkup, InlineKeyboardMarkup]:
    if key == 'remove':
        return ReplyKeyboardRemove()
    elif key == 'go_back':
        return _create_keyboard([[get_string('go_back', language)]])
    elif key == 'start.languages':
        return _create_keyboard([[get_string('languages.ru', language), get_string('languages.uz')]], one_time=True)
    elif key == 'menu':
        keyboard = [
            [get_string('menu.cabinet', language)],
            [get_string('menu.about', language), get_string('menu.support', language)],
            [get_string('menu.faq', language), get_string('menu.partners', language)],
            [get_string('menu.news', language), get_string('menu.referral', language)]
        ]
        return _create_keyboard(keyboard)
    elif key == 'account.select_role':
        keyboard = [
            [InlineKeyboardButton(get_string('account.select_role.contractor', language), callback_data='role'
                                                                                                        ':contractor')],
            [InlineKeyboardButton(get_string('account.select_role.employer', language), callback_data='role:employer')]
        ]
        return InlineKeyboardMarkup(keyboard)
    elif key == 'location.regions':
        keyboard = [[InlineKeyboardButton(get_string('location.regions.all'), callback_data='region:all')]]
        for i in range(13):
            keyboard.append([InlineKeyboardButton(get_string('location.regions.' + str(i)),
                                                  callback_data='region:' + str(i))])
        return InlineKeyboardMarkup(keyboard)
    elif key == 'resume':
        keyboard = [
            [InlineKeyboardButton(get_string('edit', language), callback_data='edit')],
            [InlineKeyboardButton(get_string('delete', language), callback_data='delete')],
            [InlineKeyboardButton(get_string('go_back', language), callback_data='back')]
        ]
        return InlineKeyboardMarkup(keyboard)
    elif key == 'resume.edit':
        keyboard = [
            [InlineKeyboardButton(get_string('title', language), callback_data='title')],
            [InlineKeyboardButton(get_string('description', language), callback_data='description')],
            [InlineKeyboardButton(get_string('contacts', language), callback_data='contacts')],
            [InlineKeyboardButton(get_string('go_back', language), callback_data='back')]
        ]
        return InlineKeyboardMarkup(keyboard)
    elif key == 'vacation':
        keyboard = [
            [InlineKeyboardButton(get_string('edit', language), callback_data='edit')],
            [InlineKeyboardButton(get_string('delete', language), callback_data='delete')],
            [InlineKeyboardButton(get_string('go_back', language), callback_data='back')]
        ]
        return InlineKeyboardMarkup(keyboard)
    elif key == 'vacation.edit':
        keyboard = [
            [InlineKeyboardButton(get_string('title', language), callback_data='title')],
            [InlineKeyboardButton(get_string('salary', language), callback_data='salary')],
            [InlineKeyboardButton(get_string('category', language), callback_data='category')],
            [InlineKeyboardButton(get_string('description', language), callback_data='description')],
            [InlineKeyboardButton(get_string('contacts', language), callback_data='contacts')],
            [InlineKeyboardButton(get_string('go_back', language), callback_data='back')]
        ]
        return InlineKeyboardMarkup(keyboard)
    elif key == 'referral':
        keyboard = [
            [InlineKeyboardButton(get_string('rules', language), callback_data='referral:rules'), InlineKeyboardButton(get_string('prize_place', language), callback_data='referral:prize')],
            [InlineKeyboardButton(get_string('rating', language), callback_data='referral:rating')]
        ]
        return InlineKeyboardMarkup(keyboard)
    elif key == 'payments.contractor':
        keyboard = [
            [InlineKeyboardButton(get_string('payments.tariff.contractor_tariff_1', language),
                                  callback_data='payments:contractor_tariff_1')],
            [InlineKeyboardButton(get_string('payments.tariff.contractor_tariff_2', language),
                                  callback_data='payments:contractor_tariff_2')],
            [InlineKeyboardButton(get_string('payments.tariff.contractor_tariff_3', language),
                                  callback_data='payments:contractor_tariff_3')],
            [InlineKeyboardButton(get_string('go_back', language), callback_data='payments:back')]
        ]
        return InlineKeyboardMarkup(keyboard)
    elif key == 'payments.employer':
        keyboard = [
            [InlineKeyboardButton(get_string('payments.tariff.employer_tariff_1', language),
                                  callback_data='payments:employer_tariff_1')],
            [InlineKeyboardButton(get_string('payments.tariff.employer_tariff_2', language),
                                  callback_data='payments:employer_tariff_2')],
            [InlineKeyboardButton(get_string('payments.tariff.employer_tariff_3', language),
                                  callback_data='payments:employer_tariff_3')],
            [InlineKeyboardButton(get_string('go_back', language), callback_data='payments:back')]
        ]
        return InlineKeyboardMarkup(keyboard)
    elif key == 'payments.providers':
        keyboard = [
            [InlineKeyboardButton(get_string('payments.click', language), callback_data='payments:click')],
            [InlineKeyboardButton(get_string('payments.payme', language), callback_data='payments:payme')],
            [InlineKeyboardButton(get_string('payments.yandex', language), callback_data='payments:yandex')],
            [InlineKeyboardButton(get_string('go_back', language), callback_data='payments:back')]
        ]
        return InlineKeyboardMarkup(keyboard)
    elif key == 'referral.rules' or key == 'referral.prize' or key == 'referral.rating':
        return InlineKeyboardMarkup([[InlineKeyboardButton(get_string('go_back', language),
                                                           callback_data='referral:back')]])
    elif key == 'support.cancel':
        return _create_keyboard([[get_string('cancel', language)]])


def get_account_keyboard(user: dict) -> Optional[InlineKeyboardMarkup]:
    if user.get('user_role') == 'employer':
        keyboard = [
            [InlineKeyboardButton(get_string('account.change_role', user.get('language')),
                                  callback_data='account:role')],
            [InlineKeyboardButton(get_string('account.up_balance', user.get('language')),
                                  callback_data='account:balance')],
            [InlineKeyboardButton(get_string('account.responses', user.get('language')),
                                  callback_data='account:responses')],
            [InlineKeyboardButton(get_string('account.my_vacancies', user.get('language')),
                                  callback_data='account:my_vacations')]
        ]
    elif user.get('user_role') == 'contractor':
        keyboard = [
            [InlineKeyboardButton(get_string('account.change_role', user.get('language')),
                                  callback_data='account:role')],
            [InlineKeyboardButton(get_string('account.up_balance', user.get('language')),
                                  callback_data='account:balance')],
            [InlineKeyboardButton(get_string('account.vacancies', user.get('language')),
                                  callback_data='account:vacations')],
            [InlineKeyboardButton(get_string('account.resumes', user.get('language')),
                                  callback_data='account:resumes')]
        ]
    else:
        return None
    return InlineKeyboardMarkup(keyboard)


def get_resumes_keyboard(resumes: list, language: str, include_create_button: bool = True) -> InlineKeyboardMarkup:
    keyboard = []
    for resume in resumes:
        if include_create_button:
            data = 'resumes:' + str(resume.get('id'))
        else:
            data = 'vacations.resume:' + str(resume.get('id'))
        keyboard.append([InlineKeyboardButton(get_string('resumes.item', language).format(resume.get('title')),
                                              callback_data=data)])
    if include_create_button:
        keyboard.append([InlineKeyboardButton(get_string('resumes.create', language), callback_data='resumes:create')])
    keyboard.append([InlineKeyboardButton(get_string('go_back', language), callback_data='resumes:back')])
    return InlineKeyboardMarkup(keyboard)


def get_vacations_keyboard(vacations: list, language: str, include_create_button=True) -> InlineKeyboardMarkup:
    keyboard = []
    for vacation in vacations:
        if include_create_button:
            data = 'my_vacations:' + str(vacation.get('id'))
        else:
            data = "vacations:" + str(vacation.get('id'))
        keyboard.append([InlineKeyboardButton(get_string('vacations.item', language).format(vacation.get('title')),
                                              callback_data=data)])
    if include_create_button:
        keyboard.append([InlineKeyboardButton(get_string('vacations.create', language), callback_data='my_vacations:create')])
    keyboard.append([InlineKeyboardButton(get_string('go_back', language), callback_data='my_vacations:back')])
    return InlineKeyboardMarkup(keyboard)


def get_categories_keyboard(categories: list, language: str, selected_categories: list) -> InlineKeyboardMarkup:
    keyboard = []
    for category in categories:
        if not any(d['id'] == category['id'] for d in selected_categories):
            keyboard.append([InlineKeyboardButton(get_string('resumes.categories.item', language).format(category[language+'_title']), callback_data='categories:' + str(category['id']))])
        else:
            keyboard.append([InlineKeyboardButton(get_string('resumes.categories.item.selected', language).format(category[language+'_title']), callback_data='categories:' + str(category['id']))])
    keyboard.append([InlineKeyboardButton(get_string('go_back', language), callback_data='categories:back')])
    if selected_categories:
        keyboard.append([InlineKeyboardButton(get_string('save', language), callback_data='categories:save')])
    return InlineKeyboardMarkup(keyboard)


def get_parent_categories_keyboard(categories: list, language: str) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(categories[0][language + '_title'], callback_data='category:' + str(categories[0]['id'])),
         InlineKeyboardButton(categories[1][language + '_title'], callback_data='category:' + str(categories[1]['id']))]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_cities_from_region(region_number: str, language: str) -> InlineKeyboardMarkup:
    def divide_chunks(l: list, n: int):
        for i in range(0, len(l), n):
            yield l[i:i + n]

    keyboard = []
    cities = get_string('location.regions.{}.cities'.format(region_number), language)
    i = 0
    chunked_cities = divide_chunks(cities, 3)
    for row in chunked_cities:
        city_row = []
        for city in row:
            city_row.append(InlineKeyboardButton(city, callback_data='city:' + str(i)))
            i += 1
        keyboard.append(city_row)
    keyboard.append([InlineKeyboardButton(get_string('go_back', language), callback_data='city:back')])
    return InlineKeyboardMarkup(keyboard)


def get_list_paginated_keyboard(entities: list, language: str, user: dict, current_page=1) -> InlineKeyboardMarkup:
    keyboard = [[InlineKeyboardButton(get_string('open_chat', language), url='tg://user?id=' + str(user.get('id')))]]
    links = []
    for i in range(len(entities)):
        if i+1 == current_page:
            text = '-'+str(i+1)+'-'
        else:
            text = str(i+1)
        links.append(InlineKeyboardButton(text, callback_data='page:' + str(i + 1)))
    keyboard.append(links)
    keyboard.append([InlineKeyboardButton(get_string('go_back', language), callback_data='page:back')])
    return InlineKeyboardMarkup(keyboard)


def get_channel_keyboard(invite_link: str, language: str) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(get_string('referral.channel.subscribe', language=language), url=invite_link)],
        [InlineKeyboardButton(get_string('referral.channel.check', language), callback_data='referral:check_channel')]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_support_keyboard(link) -> InlineKeyboardMarkup:
    keyboard = [[InlineKeyboardButton("Перейти на страницу пользователя", url=link)]]
    return InlineKeyboardMarkup(keyboard)
