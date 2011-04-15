"""
Main application
"""

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

# FIXME: What happens when you don't provide GET and POST for a handler?
# FIXME: Separate handlers by file to clean things up?


def main():
    """main"""

    from app.handlers.static import Main, About
    from app.handlers.register import Register, Callback
    from app.handlers.vote import Vote

    # FIXME: Don't require ending slash in URLS
    # FIXME: Need a catch-all for 404 error
    application = webapp.WSGIApplication([('/', Main),
                                           ('/register/(.*)', Register),
                                           ('/callback/$', Callback),
                                           ('/vote/(\w+)/$', Vote),
                                           ('/about/$', About),
                                        ], debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
