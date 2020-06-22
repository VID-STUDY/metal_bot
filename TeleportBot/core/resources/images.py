import os


_basedir = os.path.abspath(os.path.dirname(__file__))
_images_dir = os.path.join(_basedir, 'images')


def _get_image(filename):
    path = os.path.join(_images_dir, filename)
    if os.path.exists(path):
        return open(path, 'rb')
    else:
        return None


def get_news_image():
    return _get_image('news.jpg')


def get_account_image(user_role):
    filename = 'account_' + user_role + '.jpg'
    return _get_image(filename)


def get_faq_image():
    return _get_image('faq.jpg')


def get_support_image():
    return _get_image('support.jpg')
