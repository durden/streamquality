"""
Main application
"""

import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util


def main():
    """main"""

    from app.handlers.static import Main, About, Missing
    from app.handlers.register import Register, Callback
    from app.handlers.vote import Vote, VoteUp, VoteDown

    logging.getLogger().setLevel(logging.DEBUG)

    application = webapp.WSGIApplication([('/', Main),
                                   ('/register/(.*)', Register),
                                   ('/callback/$', Callback),
                                   ('/about/$', About),
                                   ('/vote/(\w+)/$', Vote),
                                   ('/vote/(\w+)/up/(\d+)/$', VoteUp),
                                   ('/vote/(\w+)/down/(\d+)/$', VoteDown),
                                   ('.*', Missing), ], debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
