import os


_basedir = os.path.abspath(os.path.dirname(__file__))
_images_dir = os.path.join(_basedir, 'images')


def _get_image(filename):
    path = os.path.join(_images_dir, filename)
    if os.path.exists(path):
        return open(path, 'rb')
    else:
        return None


def get_news_image(language):
    return _get_image('news_' + language + '.jpg')


def get_account_image(user_role, language):
    filename = 'account_' + user_role + '_' + language + '.jpg'
    return _get_image(filename)


def get_faq_image(language):
    return _get_image('faq_' + language + '.jpg')


def get_support_image(language):
    return _get_image('support_' + language + '.jpg')


def get_referral_image(language):
    return _get_image('referral_' + language + '.jpg')


def get_welcome_image(language):
    return _get_image('welcome_' + language + '.jpg')


def get_partners_image(language):
    return _get_image('partners_' + language + '.jpg')


def get_help_panel_image():
    return _get_image('help_panel.jpg')


def get_catalog_image(language):
    return _get_image('catalog_' + language + '.jpg')
