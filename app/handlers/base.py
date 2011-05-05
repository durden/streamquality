"""
Base handler class for project

All handlers should inherit from here.
"""

import os
import oauth

from google.appengine.api import urlfetch
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from django.utils import simplejson

from app.models import SQUser
from appengine_utilities.sessions import Session

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), '../../templates/')

CONSUMER_KEY = "lMbLOg9VXgzLVNEw3IrsGQ"
CONSUMER_SECRET = "4tgcfLT9sUxihC3D6XHJMUBKD6peHhhW9UfBYH0PMYI"
REGISTER_CALLBACK_URL = "http://streamquality.appspot.com/register_callback/"
SIGNIN_CALLBACK_URL = "http://streamquality.appspot.com/signin_callback/"


class NotLoggedIn(Exception):
    """Not logged in"""
    pass


# FIXME: Refactor out passing the user_name argument everywhere


class BaseHandler(webapp.RequestHandler):
    """Wrapper to provide cleaner template rendering and twitter API"""

    def __init__(self):
        """Setup session"""

        # FIXME: Set expire timeout on sessions when created
        self.session = Session()

    def render_template(self, name, *arguments, **keywords):
        """High-level wrapper for loading and directing to template"""

        path = os.path.join(os.path.dirname(__file__), TEMPLATE_DIR + name)

        # Going to tack on whether user is logged in or not, but complain if
        # we are overriding someone else's variable
        if 'logged_in' in keywords:
            raise KeyError

        user = self.get_logged_in_user()
        if user is not None:
            keywords['logged_in_user'] = user.user_name

        self.response.out.write(template.render(path, keywords))

    # Provide base get/post methods to redirect to 404 so we don't have to
    # provide both methods for a page that only needs one, etc.

    def get(self):
        """GET request"""
        return self.render_template('404.html')

    def post(self):
        """POST request"""
        return self.render_template('404.html')

    def send_twitter_request(self, user_name, url):
        """
        Easily send twitter request to given url on behalf of user_name
            - Returns status code (http return code) and json parsed response
              (if the request was successful)
        """

        if not self.logged_in(user_name):
            raise NotLoggedIn()

        user = self.get_logged_in_user()

        client = oauth.TwitterClient(CONSUMER_KEY, CONSUMER_SECRET, None)
        result = client.make_request(url, token=user.oauth_token,
                                    secret=user.oauth_secret,
                                    additional_params=None,
                                    method=urlfetch.GET)
        if result.status_code != 200:
            return (result.status_code, None)

        return (result.status_code, simplejson.loads(result.content))

    def get_tweet_info(self, user_name, tweet_id):
        """
        Get tweet author/text from twitter
        """

        url = ''.join(
            ['http://api.twitter.com/1/statuses/show/%s.json' % (tweet_id)])

        (status_code, resp) = self.send_twitter_request(user_name, url)

        if status_code != 200:
            return None

        tweet = {}
        tweet['user_name'] = resp['user']['screen_name']
        tweet['real_name'] = resp['user']['name']
        tweet['profile_image_url'] = resp['user']['profile_image_url']
        tweet['text'] = resp['text']
        return tweet

    def get_logged_in_user(self):
        """Get logged in user (SQUser)"""

        if self.debug_mode():
            try:
                return SQUser.all().filter('user_name = ',
                                            'durden20').fetch(1)[0]
            except IndexError:
                return None

        try:
            user_name = self.session['user_name']
        except KeyError:
            return None

        try:
            return SQUser.all().filter('user_name = ', user_name).fetch(1)[0]
        except IndexError:
            return None

    def logged_in(self, user_name):
        """See if a user is logged in already or not"""

        if self.debug_mode():
            return 1

        if self.session is None or 'user_name' not in self.session or \
            user_name != self.session['user_name']:
            return 0

        return 1

    def debug_mode(self):
        """Determine if debug mode is on or not"""

        if self.request.url.startswith('http://localhost'):
            import logging
            logging.debug("In debug mode")
            return 1
        else:
            return 0
