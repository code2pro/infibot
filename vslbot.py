import flask, telebot, json, re
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

from bot.config import botcfg
from bot import util

LOG_CATEGORY = 'VSLBOT.MAIN'
TELEBOT_WH_PATH = '/%s' % botcfg['TELEBOT_WH_PATH']
INTRO_MSG = """Hi %s, I'm a bot from VietStartupLondon.
Here are the commands:
/about: Discover our community and fun projects
/events: Query upcoming and past events
"""
ABOUTUS_MSG = """
Hello %s, we are VietStartupLondon, a vibrant community of young Viet professionals in London.
We are passionate about entrepreneurship, techonology and working towards connecting Vietnamese start-ups across the globe.

Explore our activities, events and mussings:
1. Facebook Group: https://www.facebook.com/groups/284739328332602/
2. Medium: https://medium.com/vietstartup-london
3. Open Projects: https://trello.com/b/ODvtUhBf/vietstartup
4. For Developers: https://github.com/VietStartupLondon
5. Website: http://www.vietstartup.co.uk/
"""

logger = util.get_logger(LOG_CATEGORY)
sessions = util.get_session_storage()
bot = util.get_bot()
app = flask.Flask(__name__)


@app.route("/")
def index():
    return ''


@app.route(TELEBOT_WH_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)


def guess_fname(message):
    '''Guess first name from available data'''
    if message.chat.first_name:
        return message.chat.first_name
    else:
        return "there"


@bot.message_handler(commands=['about', 'intro', 'aboutus'])
def handle_aboutus(message):
    '''Introduce the organisation to the world'''
    fname = guess_fname(message)
    bot.send_message(message.chat.id, ABOUTUS_MSG % fname)


@bot.message_handler(commands=['event', 'events'])
def handle_events(message):
    '''List events by the organisation'''
    events = util.get_events()
    logger.info("handle_events: Events = %s" % events)
    bot.send_message(message.chat.id, "Events: %s" % events)


@bot.message_handler(func=lambda message: True)
def handle_undefined(message):
    '''Undefined commands or messages go here'''
    chat_id = message.chat.id
    fname = guess_fname(message)
    logger.info('sessions = %s' % sessions)
    if chat_id in sessions:
        return False
    bot.reply_to(message, INTRO_MSG % fname)
