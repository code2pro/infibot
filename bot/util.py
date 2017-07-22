import logging, telebot, requests
from validate_email import validate_email
from functools import wraps
from datetime import datetime

from bot.storage import EphemeralStore
from bot.config import botcfg

LOG_CATEGORY = 'VSLBOT.UTIL'


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


logger = get_logger(LOG_CATEGORY)


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


class Event(object):
    def __init__(self, name, time, url):
        self.name = name
        self.time = time
        self.url = url

    def __repr__(self):
        return "Event(name=%s, time=%s, url='%s')" % (self.name, self.time, self.url)


def return_on_stop(f):
    '''Stop the current chatbot flow/session on /stop or /clear'''
    @wraps(f)
    def wrapper(message, *args, **kwds):
        if message.text.strip().lower() in ['/stop', '/clean']:
            return False
        return f(message, *args, **kwds)
    return wrapper


def get_bot():
    '''Return the Telegram bot with token is drawn from config'''
    return telebot.TeleBot(botcfg['TELEGRAM_TOKEN'])


def set_webhook():
    '''Set webhook URL if the current URL is outdated'''
    bot = get_bot()
    wh_info = bot.get_webhook_info()
    logger.info('set_webhook: Web Hook Info = %s' % wh_info)
    if wh_info.url != botcfg['TELEBOT_WEBHOOK_URL']:
        logger.info('set_webhook: Previous webhook URL was %s' % wh_info.url)
        bot.remove_webhook()
        bot.set_webhook(url=botcfg['TELEBOT_WEBHOOK_URL'])


def check_email(email):
    '''Validate email format'''
    return validate_email(email)


def get_session_storage():
    '''Return an ephemeral storage for sessions'''
    return UserSession(ns='sessions', prefix='u', expire=180)


def get_events():
    '''Returns Live, Started, Ended, and Completed events'''
    EVBRITE_PREFIX = botcfg['EVBRITE_PREFIX']
    EVBRITE_ANON_TOKEN = botcfg['EVBRITE_ANON_TOKEN']
    params = {
        'token': EVBRITE_ANON_TOKEN,
        'status': 'live,started,ended',
        'order_by': 'start_desc',
    }
    r = requests.get(EVBRITE_PREFIX, params=params)
    resp = r.json()
    logger.info("get_events: [status_code=%d,url=%s]" % (r.status_code, r.url))
    if r.status_code != 200:
        logger.error("get_events: Got error when querying URL '%s' [status_code=%d,error=%s,error_description=%s]" % (
            r.url, resp['status_code'], resp['error'], resp['error_description']
        ))
        return None
    events = resp['events']
    logger.info("get_events: JSON Events = %s" % events)
    ret_events = []
    for event in events:
        ev_name = event['name']['text']
        # Format: 2017-08-11T09:00:00
        ev_time = datetime.strptime(event['start']['local'], '%Y-%m-%dT%H:%M:%S')
        ev_url = event['vanity_url'] if 'vanity_url' in event else event['url']
        ret_event = Event(name=ev_name, time=ev_time, url=ev_url)
        ret_events.append(ret_event)
    return ret_events
