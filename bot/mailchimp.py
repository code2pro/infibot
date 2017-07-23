from bot.config import botcfg

class MailChimp(object):
    def __init__(self, apikey, group_id):
        self.apikey = apikey
        self.group_id = group_id
