import os

botcfg = {}

EXPECTED_ENVS = [
    'TELEGRAM_TOKEN', 'TELEBOT_WEBHOOK_URL', 'TELEBOT_WH_PATH',
    'EVBRITE_ANON_TOKEN', 'EVBRITE_GROUP_ID',
]

for var in EXPECTED_ENVS:
    if var in os.environ:
        botcfg[var] = os.environ[var]
    else:
        raise Exception('Missing env var %s' % var)

EVBRITE_GROUP_EVENTS_TMPL = 'https://www.eventbriteapi.com/v3/organizers/%s/events/'
botcfg['EVBRITE_PREFIX'] = EVBRITE_GROUP_EVENTS_TMPL % botcfg['EVBRITE_GROUP_ID']
