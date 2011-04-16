"""
Main application
"""

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

# FIXME: What happens when you don't provide GET and POST for a handler?


def main():
    """main"""

    from app.handlers.static import Main, About, Missing
    from app.handlers.register import Register, Callback
    from app.handlers.vote import Vote

    application = webapp.WSGIApplication([('/', Main),
                                           ('/register/(.*)', Register),
                                           ('/callback/$', Callback),
                                           ('/vote/(\w+)/$', Vote),
                                           ('/about/$', About),
                                           ('.*', Missing),
                                        ], debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
