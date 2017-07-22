import flask, telebot, json, re
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

from bot.config import botcfg
from bot import util

LOG_CATEGORY = 'VSLBOT.MAIN'
TELEBOT_WH_PATH = '/%s' % botcfg['TELEBOT_WH_PATH']
INTRO_MSG = """Hi %s, I'm a bot from VietStartupLondon.
Here are the commands:
/start: Show this message
/about: Discover our community and fun projects
/events: Query upcoming and past events
/member: Subscribe to our upcoming events and news
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


@bot.message_handler(commands=['intro', 'start', 'help'])
def handle_aboutus(message):
    '''Introduce the organisation to the world'''
    fname = guess_fname(message)
    bot.send_message(message.chat.id, INTRO_MSG % fname)
    del sessions[message.chat.id]


@bot.message_handler(commands=['about', 'aboutus'])
def handle_aboutus(message):
    '''Introduce the organisation to the world'''
    fname = guess_fname(message)
    bot.send_message(message.chat.id, ABOUTUS_MSG % fname)


@bot.message_handler(commands=['event', 'events'])
def handle_events(message):
    '''List events by the organisation'''
    bot.send_chat_action(message.chat.id, 'typing')
    events = util.get_events()
    if not events:
        bot.send_message(message.chat.id, "Hey! We don't have events yet. Feel free to check again.")
    else:
        output = ""
        for event in events:
            output += "* %s\n%s\n%s\n----\n" % (
                event.name, event.time.strftime("%I:%M%p %a, %b %d %Y"),
                event.url)
        bot.send_message(message.chat.id, "Our events:\n%s" % output)


@bot.message_handler(commands=['member'])
def handle_registration(message):
    chat_id = message.chat.id
    if chat_id in sessions:
        return False
    sessions[chat_id] = util.User(message.chat.first_name, message.chat.last_name)
    fname = 'there'
    if message.chat.first_name:
        fname = message.chat.first_name
    msg = bot.reply_to(message, """Howdy %s, what's your full name?
""" % fname)
    bot.register_next_step_handler(msg, process_name_step)


@util.return_on_stop
def process_name_step(message):
    chat_id = message.chat.id
    try:
        user = sessions[chat_id]
        user.first_name, user.last_name = message.text.strip().split(' ')
        # Commit the change
        sessions[chat_id] = user
        msg = bot.reply_to(message, 'Your email address, please:')
        bot.register_next_step_handler(msg, process_email_step)
    except Exception as e:
        logger.error('process_name_step: [chat:%d] Could not get first and last names - %s' % (chat_id, e))
        msg = bot.reply_to(message, 'Please enter first & last names:')
        bot.register_next_step_handler(msg, process_name_step)


@util.return_on_stop
def process_email_step(message):
    chat_id = message.chat.id
    bot.send_chat_action(chat_id, 'typing')
    try:
        if chat_id not in sessions:
            return False
        email = message.text.strip().lower()
        if not util.check_email(email):
            raise Exception('Invalid email %s' % email)
        user = sessions[chat_id]
        # Check if the email is already registered
        if util.is_user_subscribed(email):
            bot.send_message(chat_id,
                "Thanks %s! Here's news: You are already registered with the email %s" % (
                user.first_name, email))
            # Session is done, clean up
            del sessions[chat_id]
            return True
        # If the email is not registered, proceed
        user.email = email
        # Commit the change
        sessions[chat_id] = user
        if not util.subscribe_user(user):
            bot.send_message(chat_id,
                "Hey %s, there's a problem and we could not register your email %s."
                    + " Please try again alter. We are really sorry for the inconvenience." % (
                        user.first_name, user.email))
        else:
            bot.send_message(chat_id, 'Nice to meet you, %s. We have recorded your email %s.' % (
                user.first_name, user.email))
        # Session is done, clean up
        del sessions[chat_id]
    except Exception as e:
        logger.error('process_email_step: [chat:%d] Could not obtain email - %s' % (chat_id, e))
        msg = bot.reply_to(message, "Ok, please enter your email:")
        bot.register_next_step_handler(msg, process_email_step)


@bot.message_handler(func=lambda message: True)
def handle_undefined(message):
    '''Undefined commands or messages go here'''
    chat_id = message.chat.id
    fname = guess_fname(message)
    logger.info('sessions = %s' % sessions)
    if chat_id in sessions:
        return False
    bot.reply_to(message, INTRO_MSG % fname)
