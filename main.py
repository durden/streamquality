"""
Main application
"""

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util


def main():
    """main"""

    from app.handlers.static import Main, About, Missing
    from app.handlers.register import Register, Callback
    from app.handlers.vote import Vote, VoteUp

    application = webapp.WSGIApplication([('/', Main),
                                           ('/register/(.*)', Register),
                                           ('/callback/$', Callback),
                                           ('/about/$', About),
                                           ('/vote/(\w+)/$', Vote),
                                           ('/vote/(\w+)/up/(\d+)/$', VoteUp),
                                           ('.*', Missing),
                                        ], debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
