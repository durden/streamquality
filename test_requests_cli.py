"""
Purpose of this file is mainly just for copy/paste of setup in order to test
requests to the twitter api with the oauth module from the interactive
interpreter.
"""

# Setup stub for url fetch service
from google.appengine.api import urlfetch
from google.appengine.api import apiproxy_stub_map, urlfetch_stub
apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap() 
apiproxy_stub_map.apiproxy.RegisterStub('urlfetch',
                            urlfetch_stub.URLFetchServiceStub()) 

from django.utils import simplejson

import oauth

# Fill in with values for your own app
CALLBACK_URL = "http://streamquality.appspot.com/callback/"
CONSUMER_KEY = "lMbLOg9VXgzLVNEw3IrsGQ"
CONSUMER_SECRET = "4tgcfLT9sUxihC3D6XHJMUBKD6peHhhW9UfBYH0PMYI"

# Fill in with authenticated user creds for your app
user_token = ""
user_secret = ""

# Fill in with url you want to send request to
url = ""

client = oauth.TwitterClient(CONSUMER_KEY, CONSUMER_SECRET, CALLBACK_URL)
result = client.make_request(url, token=user_token, secret=user_secret,
                            additional_params=None, method=urlfetch.GET)

# request.content holds json response
# request.headers holds http headers
json = simplejson.loads(result.content)
