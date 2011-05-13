"""
Handlers to deal with registering users via oauth with Twitter.
"""

from google.appengine.api import urlfetch

import cgi
import oauth

from base import BaseHandler, CONSUMER_KEY, CONSUMER_SECRET
from base import REGISTER_CALLBACK_URL, SIGNIN_CALLBACK_URL

from appengine_utilities.sessions import Session

from app.models import SQUser


class OauthHandler(BaseHandler):
    """Simple handler to provide handling an oauth callback request"""

    def handle_callback(self, request):
        """
        Parse out oauth creds returned from request and return them
            - Returns tuple (username, realname, secret token, oauth token)
        """

        client = oauth.TwitterClient(CONSUMER_KEY, CONSUMER_SECRET, None)

        auth_token = request.get('oauth_token', default_value=None)
        auth_verifier = request.get('oauth_verifier', default_value=None)

        if auth_token is None:
            return self.render_template('404.html', msg='Missing oauth_token')

        if auth_verifier is None:
            return self.render_template('404.html',
                                        msg='Missing oauth_verifier')

        try:
            user_info = client.get_user_info(auth_token,
                                                auth_verifier=auth_verifier)
        except oauth.OAuthException, e:
            return self.render_template('404.html', msg=str(e))

        return (user_info['username'], user_info['name'], user_info['secret'],
                user_info['token'])


class Register(OauthHandler):
    """Deal with registering user with local service"""

    def get(self, result=None):
        """GET request"""

        msg = ""
        if result is not None:
            if result == "success":
                msg = "User registered!"
            elif result == "incomplete":
                msg = "Please fill out all required fields"
            elif result == "not_registered":
                msg = "Please register"
            elif result == "duplicate":
                msg = "User already registered"

        self.render_template('register.html', msg=msg)

    def post(self, result=None):
        """POST request"""

        user_name = cgi.escape(self.request.get('user_name'))
        if user_name == '' or not len(user_name):
            self.redirect('/register/incomplete')
        else:
            # If user doesn't already exist, create basic account to be
            # completed in the callback
            if not len(SQUser.all().filter('user_name = ',
                user_name).fetch(1)):
                user = SQUser(oauth_secret='secret', oauth_token='token',
                                user_name=user_name, real_name='real')
                user.put()

            # oauth dance, which ends up at the callback url
            client = oauth.TwitterClient(CONSUMER_KEY, CONSUMER_SECRET,
                                            REGISTER_CALLBACK_URL)
            return self.redirect(client.get_authorization_url())


class RegisterCallback(OauthHandler):
    """Handle callback from register application with Twitter"""

    def get(self):
        """Complete oauth with Twitter and save users tokens for future use"""

        (user_name, real_name, oauth_secret, oauth_token) = \
                                            self.handle_callback(self.request)
        try:
            user = SQUser.all().filter("user_name = ", user_name)[0]
        except IndexError:
            return self.redirect('/register/not_registered')

        user.real_name = real_name
        user.oauth_secret = oauth_secret
        user.oauth_token = oauth_token
        user.put()

        return self.redirect('/register/success')


class Signin(OauthHandler):
    """Handle signing a user in with twitter"""

    def get(self):
        """Start the oauth process for logging in via twitter"""

        # oauth dance, which ends up at the callback url
        client = oauth.TwitterClient(CONSUMER_KEY, CONSUMER_SECRET,
                                        SIGNIN_CALLBACK_URL)
        return self.redirect(client.get_authentication_url())


class SigninCallback(OauthHandler):
    """Handle callback from signing in with Twitter"""

    def get(self):
        """Send user to tweet voting"""

        (user_name, real_name, oauth_secret, oauth_token) = \
                                            self.handle_callback(self.request)
        try:
            SQUser.all().filter("user_name = ", user_name)[0]
        except IndexError:
            return self.redirect('/register/not_registered')

        self.session = Session()
        self.session['user_name'] = user_name

        return self.redirect('/vote/')


class Unfollow(BaseHandler):
    """Handle unfollowing"""

    def get(self, unfollow_user_name):
        """Send unfollow request"""

        user = self.get_logged_in_user()
        url = ''.join(['http://api.twitter.com/1/friendships/destroy.xml'])
        (status_code, resp) = self.send_twitter_request(user.user_name, url,
                        additional_params={'screen_name': unfollow_user_name},
                        method=urlfetch.POST)

        if status_code != 200:
            return self.render_template('404.html', msg=status_code)

        return self.redirect('/myvotes/%s/' % (user.user_name))


class Logout(BaseHandler):
    """Log user out of service"""

    def get(self):
        """Remove session"""

        self.session.delete()
        return self.redirect('/')
