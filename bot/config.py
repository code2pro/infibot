import os

botcfg = {}

for var in [
    'TELEGRAM_TOKEN', 'TELEBOT_WEBHOOK_URL', 'TELEBOT_WH_PATH']:
    if var in os.environ:
        botcfg[var] = os.environ[var]
    else:
        raise Exception('Missing env var %s' % var)
