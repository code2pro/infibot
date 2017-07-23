import os

botcfg = {}

EXPECTED_ENVS = [
    'TELEGRAM_TOKEN', 'TELEBOT_WEBHOOK_URL', 'TELEBOT_WH_PATH',
    'EVBRITE_ANON_TOKEN', 'EVBRITE_GROUP_ID',
    'MAILING_BACKEND',
]
SUPP_MAILING_BACKENDS = {
    'MAILCHIMP' : ['MAILCHIMP_API_KEY', 'MAILCHIMP_GROUPID'],
    'MAILER_LITE' : ['MAILER_LITE_API_KEY', 'MAILER_LITE_GROUPID'],
}

for var in EXPECTED_ENVS:
    if var in os.environ:
        botcfg[var] = os.environ[var]
    else:
        raise Exception('Missing env var %s' % var)

if botcfg['MAILING_BACKEND'] not in SUPP_MAILING_BACKENDS:
    raise Exception('Currently supporting only %s' % list(SUPP_MAILING_BACKENDS.keys()))

for var in SUPP_MAILING_BACKENDS[botcfg['MAILING_BACKEND']]:
    if var in os.environ:
        botcfg[var] = os.environ[var]
    else:
        raise Exception('Missing env var %s' % var)

for var in ['MAILER_LITE_GROUPID']:
    if var in botcfg:
        botcfg[var] = int(botcfg[var])

EVBRITE_GROUP_EVENTS_TMPL = 'https://www.eventbriteapi.com/v3/organizers/%s/events/'
botcfg['EVBRITE_PREFIX'] = EVBRITE_GROUP_EVENTS_TMPL % botcfg['EVBRITE_GROUP_ID']
