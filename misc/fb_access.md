
```
https://developers.facebook.com/tools/explorer/XXXX/?method=GET&path=284739328332602%2Fevents&version=v2.10

https://developers.facebook.com/docs/facebook-login/access-tokens/#apptokens

curl -L "https://graph.facebook.com/oauth/access_token?client_id=$FB_INFIBOT_ID&client_secret=$FB_INFIBOT_SECRET&grant_type=client_credentials" > access_token

curl -i -X GET "https://graph.facebook.com/v2.10/284739328332602/events?access_token=$FB_INFIBOT_ID|$FB_TEMP_ACCESS_TOKEN"
```
