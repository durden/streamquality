"""
Purpose of this file is mainly just for copy/paste of setup in order to test
requests to the twitter api with the oauth module from the interactive
interpreter.
"""

# Fill in with values for your own app
CALLBACK_URL = "http://streamquality.appspot.com/callback/"
CONSUMER_KEY = "lMbLOg9VXgzLVNEw3IrsGQ"
CONSUMER_SECRET = "4tgcfLT9sUxihC3D6XHJMUBKD6peHhhW9UfBYH0PMYI"

# Fill in with authenticated user creds for your app
user_token = ""
user_secret = ""

try:
    from private_oauth_creds.tokens import *
except ImportError, e:
    print "ERROR: Provide private_oauth_creds module with user_token, " + \
          "user_secret variables or set these variables manually"


# Container object
class User(object):
    def __init__(self, name, tweet):
        self.name = name
        self.tweet = tweet

# Setup stub for url fetch service
from google.appengine.api import urlfetch
from google.appengine.api import apiproxy_stub_map, urlfetch_stub

apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
apiproxy_stub_map.apiproxy.RegisterStub('urlfetch',
                            urlfetch_stub.URLFetchServiceStub())

from django.utils import simplejson

import oauth


def try_request(url=None):
    """Send request to twitter url"""

    # Fill in with url you want to send request to
    url = ''.join(['http://api.twitter.com/1/statuses/friends_timeline.json'])

    # request.content holds json response
    # request.headers holds http headers

    client = oauth.TwitterClient(CONSUMER_KEY, CONSUMER_SECRET, CALLBACK_URL)
    result = client.make_request(url, token=user_token, secret=user_secret,
                                additional_params=None, method=urlfetch.GET)
    json = simplejson.loads(result.content)

    return json

if __name__ == "__main__":
    json = try_request()

    print json

    # Create list of user objects
    #users = []
    #for obj in json:
    #    print obj
        #users.append(User(name=obj['user']['name'], tweet=obj['text']))

    #for user in users:
    #    print "name: %s ======== tweet: %s" % (user.name, user.tweet)
