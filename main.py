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

    application = webapp.WSGIApplication([('/', Main),
                                   ('/register/(.*)', Register),
                                   ('/signin/', Signin),
                                   ('/register_callback/$', RegisterCallback),
                                   ('/signin_callback/$', SigninCallback),
                                   ('/about/$', About),
                                   ('/logout/$', Logout),
                                   ('/vote/up/(\d+)/$', VoteUp),
                                   ('/vote/down/(\d+)/$', VoteDown),
                                   (r'/vote/(\d*)/*(.*)$', Vote),
                                   ('/myvotes/(\w*)$', MyVotes),
                                   ('/unfollow/(\w+)/$', Unfollow),
                                   ('.*', Missing), ], debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
