import os

botcfg = {}

EXPECTED_ENVS = [
    'TELEGRAM_TOKEN', 'TELEBOT_WEBHOOK_URL', 'TELEBOT_WH_PATH',
    'EVBRITE_ANON_TOKEN',
]

for var in EXPECTED_ENVS:
    if var in os.environ:
        botcfg[var] = os.environ[var]
    else:
        raise Exception('Missing env var %s' % var)
