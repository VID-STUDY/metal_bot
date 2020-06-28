from datetime import datetime
import re


def date_difference(older: datetime, newer: datetime):
    """
    Returns a difference between two dates
    :param older: Older date
    :param newer: Newer date
    :return: Dictionary with differences
    """
    difference = newer - older
    days = difference.days
    hours = difference.seconds / 3600
    minutes = difference.seconds % 3600 / 60
    seconds = difference.seconds % 3600 % 60

    return {
        'days': days,
        'hours': hours,
        'minutes': minutes,
        'seconds': seconds
    }


def date_difference_now(date_string: str):
    newer = datetime.now()
    older = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%fZ')

    return date_difference(older, newer)


def replace_new_line(string: str):
    return re.sub(r'<br\s*?/>', '\n', string)


def reformat_datetime(date_string: str):
    date = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%fZ')
    return date.strftime('%d.%m.%Y')
