"""
Handlers to deal with registering users via oauth with Twitter.
"""

import cgi
import oauth

from base import BaseHandler, CONSUMER_KEY, CALLBACK_URL, CONSUMER_SECRET
from app.models import SQUser


class Register(BaseHandler):
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
                user = SQUser(oauth_secret='secret', oauth_token='token',
                                user_name=user_name, real_name='real')
                user.put()

                # oauth dance, which ends up at the callback url
                client = oauth.TwitterClient(CONSUMER_KEY, CONSUMER_SECRET,
                                                CALLBACK_URL)
                return self.redirect(client.get_authorization_url())


class Callback(BaseHandler):
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
