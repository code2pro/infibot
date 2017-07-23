import requests, json
from bot.logger import get_logger

MAILER_LITE_API_PREFIX = "https://api.mailerlite.com/api/v2"
MAILER_LITE_GROUP_SUB_TMPL = MAILER_LITE_API_PREFIX + "/groups/%s/subscribers"
MAILER_LITE_USER_GROUPS_TMPL = MAILER_LITE_API_PREFIX + "/subscribers/%s/groups"

LOG_CATEGORY = 'VSLBOT.UTIL'
logger = get_logger(LOG_CATEGORY)

class MailerLite(object):
    def __init__(self, apikey, group_id):
        self.apikey = apikey
        self.group_id = group_id

    def get_headers(self):
        return {
            'content-type': 'application/json',
            'x-mailerlite-apikey': self.apikey,
        }

    def get_user_groups(self, email):
        '''Get all groups the user has subscribed to'''
        headers = self.get_headers()
        url = MAILER_LITE_USER_GROUPS_TMPL % email.strip().lower()
        r = requests.get(url, headers=headers)
        resp = r.json()
        if r.status_code != 200:
            error = resp['error']
            logger.error("get_user_groups: Got error when querying URL '%s' [status_code=%d,error_code=%d,error_description='%s']" % (
                r.url, r.status_code, error['code'], error['message']
            ))
            return None
        logger.info("get_user_groups: JSON Groups = %s" % resp)
        return resp

    def is_user_subscribed_gid(self, email, group_id):
        '''Check if the user is already subscribed to mail list with specified ID'''
        groups = self.get_user_groups(email)
        if not groups:
            return False
        def cond(group):
            logger.info("is_user_subscribed_gid: cond => group = %s" % group)
            return (group['id'] == group_id and not group['unsubscribed'])
        target_groups = [group['id'] for group in groups if cond(group)]
        logger.info("is_user_subscribed_gid: target_groups = %s" % target_groups)
        if target_groups != [group_id]:
            return False
        return True

    def is_user_subscribed(self, email):
        '''Check if the user is already subscribed to mail list'''
        return self.is_user_subscribed_gid(email, self.group_id)

    def subscribe_user_gid(self, user, group_id):
        '''Subscribe the user to a specified group ID'''
        headers = self.get_headers()
        url = MAILER_LITE_GROUP_SUB_TMPL % group_id
        data = {
            'name'      : user.first_name,
            'last_name' : user.last_name,
            'email'     : user.email,
        }
        payload = json.dumps(data)
        r = requests.post(url, headers=headers, data=payload)
        resp = r.json()
        if r.status_code != 200:
            error = resp['error']
            logger.error("subscribe_user_gid: Got error when querying URL '%s' [status_code=%d,error_code=%d,error_description=%s]" % (
                r.url, r.status_code, error['code'], error['message']
            ))
            return None
        logger.info("get_user_groups: JSON Subscribe user = %s" % resp)
        return True

    def subscribe_user(self, user):
        '''Subscribe the user to the default group'''
        return self.subscribe_user_gid(user, self.group_id)
