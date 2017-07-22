import logging, telebot
from validate_email import validate_email
from functools import wraps

from bot.storage import EphemeralStore
from bot.config import botcfg

LOG_CATEGORY = 'VSLBOT.UTIL'

class User(object):
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name


class UserSession(EphemeralStore):
    def __init__(self, ns, prefix, expire=180, db=0):
        super(UserSession, self).__init__(ns, prefix, expire, db)

    def __setitem__(self, key, user):
        super().hmset(key, user.__dict__)

    def __getitem__(self, key):
        val = super().hgetall(key)
        if not val:
            return None
        # TODO: Fix the Bytes vs String issue
        user = User(val[b'first_name'].decode('utf-8'), val[b'last_name'].decode('utf-8'))
        return user


def get_bot():
    return telebot.TeleBot(botcfg['TELEGRAM_TOKEN'])


def set_webhook():
    logger = get_logger(LOG_CATEGORY)
    bot = get_bot()
    wh_info = bot.get_webhook_info()
    logger.info('set_webhook: Web Hook Info = %s' % wh_info)
    if wh_info.url != botcfg['TELEBOT_WEBHOOK_URL']:
        logger.info('set_webhook: Previous webhook URL was %s' % wh_info.url)
        bot.remove_webhook()
        bot.set_webhook(url=botcfg['TELEBOT_WEBHOOK_URL'])


def get_logger(log_category):
    '''Return logger with specified log category'''
    FORMAT = '%(asctime)s.%(msecs)03d:%(process)d:%(thread)d %(name)s %(levelname)s %(filename)s:%(lineno)d: %(message)s'
    DATE_FORMAT = '%Y-%m-%d_%H:%M:%S'
    formatter = logging.Formatter(fmt=FORMAT, datefmt=DATE_FORMAT)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger = logging.getLogger(log_category)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


def check_email(email):
    '''Validate email format'''
    return validate_email(email)


def get_session_storage():
    '''Return an ephemeral storage for sessions'''
    return UserSession(ns='sessions', prefix='u', expire=180)

def return_on_stop(f):
    @wraps(f)
    def wrapper(message, *args, **kwds):
        if message.text.strip().lower() in ['/stop', '/clean']:
            return False
        return f(message, *args, **kwds)
    return wrapper
