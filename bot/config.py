import os

botcfg = {}

EXPECTED_ENVS = [
    'TELEGRAM_TOKEN', 'TELEBOT_WEBHOOK_URL', 'TELEBOT_WH_PATH',
    'EVBRITE_ANON_TOKEN', 'EVBRITE_GROUP_ID',
    'MAILER_LITE_API_KEY', 'MAILER_LITE_GROUPID',
]

for var in EXPECTED_ENVS:
    if var in os.environ:
        botcfg[var] = os.environ[var]
    else:
        raise Exception('Missing env var %s' % var)

EVBRITE_GROUP_EVENTS_TMPL = 'https://www.eventbriteapi.com/v3/organizers/%s/events/'
botcfg['EVBRITE_PREFIX'] = EVBRITE_GROUP_EVENTS_TMPL % botcfg['EVBRITE_GROUP_ID']

MAILER_LITE_API_PREFIX = "https://api.mailerlite.com/api/v2"
MAILER_LITE_GROUP_SUB_TMPL = "/groups/%s/subscribers"
MAILER_LITE_USER_GROUPS_TMPL = "/subscribers/%s/groups"
botcfg['MAILER_LITE_USER_GROUPS_TMPL'] = MAILER_LITE_API_PREFIX + MAILER_LITE_USER_GROUPS_TMPL
botcfg['MAILER_LITE_GROUP_SUB_TMPL'] = MAILER_LITE_API_PREFIX + MAILER_LITE_GROUP_SUB_TMPL
botcfg['MAILER_LITE_GROUPID'] = int(botcfg['MAILER_LITE_GROUPID'])
