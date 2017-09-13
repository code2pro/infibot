import requests, hashlib, json
from bot.logger import get_logger

MAILCHIMP_API_PREFIX = "https://%s.api.mailchimp.com/3.0"
MAILCHIMP_GROUP_SUB_TMPL = "/lists/%s/members"
MAILCHIMP_USER_GROUPS_TMPL = "/lists/%s/members/%s"

LOG_CATEGORY = 'INFIBOT.UTIL'
logger = get_logger(LOG_CATEGORY)


def get_email_hash(email):
    email = email.strip().lower()
    return hashlib.md5(email.encode('utf-8')).hexdigest()


class MailChimp(object):
    def __init__(self, apikey, group_id):
        apikey = apikey.strip()
        self.apikey = apikey
        self.group_id = group_id
        self.data_center = apikey.split('-')[-1]
        self.MAILCHIMP_API_PREFIX = MAILCHIMP_API_PREFIX % self.data_center
        self.MAILCHIMP_GROUP_SUB_TMPL = self.MAILCHIMP_API_PREFIX + MAILCHIMP_GROUP_SUB_TMPL
        self.MAILCHIMP_USER_GROUPS_TMPL = self.MAILCHIMP_API_PREFIX + MAILCHIMP_USER_GROUPS_TMPL
        logger.info("MAILCHIMP_API_PREFIX = '%s'" % self.MAILCHIMP_API_PREFIX)

    def get_auth(self):
        return ('user1234', self.apikey)

    def is_user_subscribed_gid(self, email, group_id):
        '''Check if the user is already subscribed to mail list with specified ID'''
        email_md5 = get_email_hash(email)
        url = self.MAILCHIMP_USER_GROUPS_TMPL % (group_id, email_md5)
        r = requests.get(url, auth=self.get_auth())
        resp = r.json()
        if r.status_code == 404:
            error = resp
            logger.info("is_user_subscribed_gid: Got error when querying URL '%s' [status_code=%d,error_code=%d,error_title='%s',error_description='%s']" % (
                r.url, r.status_code, error['status'], error['title'], error['detail']
            ))
            return False
        elif r.status_code != 200:
            error = resp
            logger.error("is_user_subscribed_gid: Got error when querying URL '%s' [status_code=%d,error_code=%d,error_title='%s',error_description='%s']" % (
                r.url, r.status_code, error['status'], error['title'], error['detail']
            ))
            return None
        logger.info("is_user_subscribed_gid: resp = %s" % resp)
        return True

    def is_user_subscribed(self, email):
        '''Check if the user is already subscribed to mail list'''
        return self.is_user_subscribed_gid(email, self.group_id)

    def subscribe_user_gid(self, user, group_id, reg_source='TELEGRAM'):
        '''Subscribe the user to a specified group ID'''
        url = self.MAILCHIMP_GROUP_SUB_TMPL % group_id
        data = {
            'status'        : 'pending',
            'email_address' : user.email,
            'merge_fields'  : {
                'EMAIL'          : user.email,
                'FNAME'          : user.first_name,
                'LNAME'          : user.last_name,
                'REG_SOURCE'     : reg_source,
                'ORIG_ID'        : user.orig_id,
            }
        }
        payload = json.dumps(data)
        r = requests.post(url, auth=self.get_auth(), data=payload)
        logger.info("Request = %s" % r)
        resp = r.json()
        if r.status_code != 200:
            error = resp
            logger.error("is_user_subscribed_gid: Got error when querying URL '%s' [status_code=%d,error_code=%d,error_title='%s',error_description='%s']" % (
                r.url, r.status_code, error['status'], error['title'], error['detail']
            ))
            return None
        logger.info("subscribe_user_gid: JSON Subscribe user = %s" % resp)
        return True

    def subscribe_user(self, user):
        '''Subscribe the user to the default group'''
        return self.subscribe_user_gid(user, self.group_id)
