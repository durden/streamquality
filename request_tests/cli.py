"""
Purpose of this file is mainly just for copy/paste of setup in order to test
requests to the twitter api with the oauth module from the interactive
interpreter.
"""

# Fill in with values for your own app
CALLBACK_URL = "http://streamquality.appspot.com/register_callback/"
CONSUMER_KEY = "lMbLOg9VXgzLVNEw3IrsGQ"
CONSUMER_SECRET = "4tgcfLT9sUxihC3D6XHJMUBKD6peHhhW9UfBYH0PMYI"

try:
    from private_oauth_creds.tokens import USER_TOKEN, USER_SECRET
except ImportError, e:
    print "ERROR: Provide private_oauth_creds module with user_token, " + \
          "user_secret variables or set these variables manually"
    USER_TOKEN = ""
    USER_SECRET = ""


# Try loading json library
try:
    import json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        try:
            from django.utils import simplejson as json
        except ImportError:
            print "No JSON library found"
            import sys
            sys.exit(-1)


# Setup stub for url fetch service
from google.appengine.api import urlfetch
from google.appengine.api import apiproxy_stub_map, urlfetch_stub

apiproxy_stub_map.apiproxy = apiproxy_stub_map.APIProxyStubMap()
apiproxy_stub_map.apiproxy.RegisterStub('urlfetch',
                            urlfetch_stub.URLFetchServiceStub())

import oauth


def try_request(url='http://api.twitter.com/1/statuses/friends_timeline.json'):
    """Send request to twitter url"""

    # request.content holds json response
    # request.headers holds http headers

    client = oauth.TwitterClient(CONSUMER_KEY, CONSUMER_SECRET, CALLBACK_URL)
    result = client.make_request(url, token=USER_TOKEN, secret=USER_SECRET,
                                additional_params=None, method=urlfetch.GET)
    return json.loads(result.content)


def pretty_print(json_res):
    """Print json result in a pretty format"""

    jstr = json.dumps(json_res, indent=4)
    print '\n'.join([l.rstrip() for l in  jstr.splitlines()])


def dump_user_tweets():
    """Dump user tweets as an example of how to use try_request() method"""

    res = try_request()
    for obj in res:
        print "name: %s, tweet: %s" % (obj['user']['name'], obj['text'])
        print "--------------------------------------------------"


if __name__ == "__main__":
    dump_user_tweets()
