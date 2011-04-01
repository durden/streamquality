"""
Main Views
"""

import os
import cgi
import oauth

from google.appengine.ext import webapp
from google.appengine.api import urlfetch
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template

from django.utils import simplejson

from models import SQUser


TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates/')

CONSUMER_KEY = "lMbLOg9VXgzLVNEw3IrsGQ"
CONSUMER_SECRET = "4tgcfLT9sUxihC3D6XHJMUBKD6peHhhW9UfBYH0PMYI"
CALLBACK_URL = "http://streamquality.appspot.com/callback/"

# FIXME: What happens when you don't provide GET and POST for a handler?
# FIXME: Separate handlers by file to clean things up?


class LocalHandler(webapp.RequestHandler):
    """Silly wrapper to provide cleaner template rendering API"""

    def render_template(self, name, *arguments, **keywords):
        """High-level wrapper for loading and directing to template"""

        path = os.path.join(os.path.dirname(__file__), TEMPLATE_DIR + name)
        self.response.out.write(template.render(path, keywords))


class MainHandler(LocalHandler):
    """Homepage"""

    def get(self):
        """GET request"""
        self.render_template('index.html')


class VoteHandler(LocalHandler):
    """Vote on tweets"""

    def get(self, user_name):
        """Interface for given user to vote"""

        # FIXME: Authenticate user
        try:
            user = SQUser.all().filter('user_name = ', user_name).fetch(1)[0]
        except IndexError:
            self.render_template('vote.html', msg="%s not found" % (user_name))
            return

        # Get 20 most recent tweets from friends/user
        url = ''.join(
                ['http://api.twitter.com/1/statuses/friends_timeline.json'])

        client = oauth.TwitterClient(CONSUMER_KEY, CONSUMER_SECRET,
                                     CALLBACK_URL)
        result = client.make_request(url, token=user.oauth_token,
                                    secret=user.oauth_secret,
                                    additional_params=None,
                                    method=urlfetch.GET)

        if result.status_code != 200:
            self.render_template('vote.html',
                    msg='Status %d returned %s' % (result.status_code, result.content))
            return

        json = simplejson.loads(result.content)
        self.render_template('vote.html', user_name=user_name, result=json)


class AboutHandler(LocalHandler):
    """About"""

    def get(self):
        """GET request"""
        self.render_template('about.html')


class RegisterHandler(LocalHandler):
    """Deal with registering user with local service"""

    def get(self, result=None):
        """GET request"""

        msg = ""
        if result is not None:
            if result == "success":
                msg = "User registered!"
            elif result == "incomplete":
                msg = "Please fill out all required fields"
            elif result == "duplicate":
                msg = "User already registered"

        self.render_template('register.html', msg=msg)

    def post(self, result=None):
        """POST request"""

        user_name = cgi.escape(self.request.get('user_name'))
        if user_name == '' or not len(user_name):
            self.redirect('/register/incomplete')
        else:
            # FIXME: Do something about user that starts registration
            # process, but never comes back from callback, in which case they
            # would show up without valid tokens.  Should probably just try
            # to send them back to oauth instead of error
            if len(SQUser.all().filter('user_name = ', user_name).fetch(1)):
                self.redirect('/register/duplicate')
            else:
                # FIXME: Update defaults with n/a or something better
                user = SQUser(oauth_secret='secret', oauth_token='token',
                                user_name=user_name, real_name='real')
                user.put()

                # oauth dance, which ends up at the callback url
                client = oauth.TwitterClient(CONSUMER_KEY, CONSUMER_SECRET,
                                                CALLBACK_URL)
                return self.redirect(client.get_authorization_url())


class CallbackHandler(LocalHandler):
    """Handle callback from oauth with Twitter"""

    def get(self):
        """Complete oauth with Twitter and save users tokens for future use"""

        client = oauth.TwitterClient(CONSUMER_KEY, CONSUMER_SECRET,
                                        CALLBACK_URL)

        # FIXME: What happens when these GET params don't exist?
        auth_token = self.request.get('oauth_token')
        auth_verifier = self.request.get('oauth_verifier')

        try:
            user_info = client.get_user_info(auth_token,
                                                auth_verifier=auth_verifier)
        except oauth.OAuthException:
            # FIXME: Handle -- test by going straight to callback url w/o
            # any of the GET params
            pass

        try:
            user = SQUser.all().filter("user_name = ",
                                            user_info['username'])[0]
        except IndexError:
            self.redirect('/register/incomplete')
            return

        user.real_name = user_info['name']
        user.oauth_secret = user_info['secret']
        user.oauth_token = user_info['token']
        user.put()

        return self.redirect('/register/success')

    def post(self):
        """Should never get a post request for this handler"""
        self.redirect('/')


def main():
    """main"""

    # FIXME: Don't require ending slash in URLS
    # FIXME: Need a catch-all for 404 error
    application = webapp.WSGIApplication([('/', MainHandler),
                                           ('/register/(.*)', RegisterHandler),
                                           ('/callback/$', CallbackHandler),
                                           ('/vote/(\w+)/$', VoteHandler),
                                           ('/about/$', AboutHandler),
                                        ], debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
