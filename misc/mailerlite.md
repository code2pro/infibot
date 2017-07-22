http://developers.mailerlite.com/reference#add-single-subscriber

https://stackoverflow.com/questions/42190984/dyld-library-not-loaded-error-preventing-virtualenv-from-loading

http://developers.mailerlite.com/docs/request

https://app.mailerlite.com/integrations/api/

http://developers.mailerlite.com/reference#subscribers-in-a-group-by-type

```
When you pip installed virtualenvwrapper, pip will have installed virtualenv for you as it is a dependency. Unfortunately, that virtualenv is not compatible with Anaconda Python. Fortunately, the Anaconda Distribution has a virtualenv that is compatible. To fix this:

pip uninstall virtualenv
conda install virtualenv
```


```
import requests, json

MAILER_LITE_API_PREFIX = "https://api.mailerlite.com/api/v2"
MAILER_LITE_GROUP_SUB = "/groups/%s/subscribers" % MAILER_LITE_GROUP_ID
MAILER_LITE_USER_GROUPS = "/subscribers/%s/groups" % email

url = "%s%s" % (MAILER_LITE_API_PREFIX, MAILER_LITE_GROUP_SUB)

data = {
    'name'   : 'John',
    'email'  : 'demo@mailerlite.com',
    'fields' : {'company': 'MailerLite'}
}

payload = json.dumps(data)

headers = {
    'content-type': "application/json",
    'x-mailerlite-apikey': MAILER_LITE_API_KEY
}

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)
```
