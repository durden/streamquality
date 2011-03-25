"""
Main Views
"""

import os
import cgi

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template

from models import SQUser


TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates/')


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
            if len(SQUser.all().filter('user_name = ', user_name).fetch(1)):
                self.redirect('/register/duplicate')
            else:
                user = SQUser(oauth_secret='secret', oauth_token='token',
                                user_name=user_name, real_name='real')
                user.put()
                self.redirect('/register/success')


def main():
    """main"""

    #FIXME: Need a catch-all for 404 error
    application = webapp.WSGIApplication([('/', MainHandler),
                                           ('/register/(.*)', RegisterHandler),
                                        ], debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
