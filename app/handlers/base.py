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

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), '../../templates/')

CONSUMER_KEY = "lMbLOg9VXgzLVNEw3IrsGQ"
CONSUMER_SECRET = "4tgcfLT9sUxihC3D6XHJMUBKD6peHhhW9UfBYH0PMYI"
CALLBACK_URL = "http://streamquality.appspot.com/callback/"


class InvalidUser(Exception):
    """Invalid user"""
    pass


# FIXME: Refactor out passing the user_name argument everywhere


class BaseHandler(webapp.RequestHandler):
    """Silly wrapper to provide cleaner template rendering API"""

    def render_template(self, name, *arguments, **keywords):
        """High-level wrapper for loading and directing to template"""

        path = os.path.join(os.path.dirname(__file__), TEMPLATE_DIR + name)
        self.response.out.write(template.render(path, keywords))

    # Provide base get/post methods to redirect to 404 so we don't have to
    # provide both methods for a page that only needs one, etc.
    def get(self):
        """GET request"""
        self.render_template('404.html')

    def post(self):
        """POST request"""
        self.render_template('404.html')

    def send_twitter_request(self, user_name, url):
        """
        Easily send twitter request to given url on behalf of user_name
            - Returns status code (http return code) and json parsed response
              (if the request was successful)
        """

        # FIXME: Authenticate user
        try:
            user = SQUser.all().filter('user_name = ', user_name).fetch(1)[0]
        except IndexError:
            raise InvalidUser()

        client = oauth.TwitterClient(CONSUMER_KEY, CONSUMER_SECRET,
                                     CALLBACK_URL)
        result = client.make_request(url, token=user.oauth_token,
                                    secret=user.oauth_secret,
                                    additional_params=None,
                                    method=urlfetch.GET)
        if result.status_code != 200:
            return (result.status_code, None)

        return (result.status_code, simplejson.loads(result.content))

    def get_tweet_author(self, user_name, tweet_id):
        """
        Get tweet author from twitter by sending request on behalf of user_name
        """

        url = ''.join(
            ['http://api.twitter.com/1/statuses/show/%d.json' % (tweet_id)])

        (status_code, tweet) = self.send_twitter_request(user_name, url)

        if status_code != 200:
            return None

        return tweet['user']['name']
