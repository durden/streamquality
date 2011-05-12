"""
Main application
"""

import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util


def main():
    """main"""

    from app.handlers.static import Main, About, Missing
    from app.handlers.register import Register, RegisterCallback
    from app.handlers.register import Signin, SigninCallback, Logout, Unfollow
    from app.handlers.vote import Vote, VoteUp, VoteDown, MyVotes

    logging.getLogger().setLevel(logging.DEBUG)

    # FIXME: Remove username from urls, use get_logged_in_user instead
    application = webapp.WSGIApplication([('/', Main),
                                   ('/register/(.*)', Register),
                                   ('/signin/', Signin),
                                   ('/register_callback/$', RegisterCallback),
                                   ('/signin_callback/$', SigninCallback),
                                   ('/about/$', About),
                                   ('/logout/$', Logout),
                                   ('/vote/(\w+)/$', Vote),
                                   ('/vote/(\w+)/up/(\d+)/$', VoteUp),
                                   ('/vote/(\w+)/down/(\d+)/$', VoteDown),
                                   ('/myvotes/(\w+)/(\w*)$', MyVotes),
                                   ('/unfollow/(\w+)/$', Unfollow),
                                   ('.*', Missing), ], debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
