#!/usr/bin/env python

import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util, template


TEMPLATE_DIR=os.path.join(os.path.dirname(__file__), 'templates')

class MainHandler(webapp.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__),
                            TEMPLATE_DIR + '/index.html')
        self.response.out.write(template.render(path, {}))

def main():
    application = webapp.WSGIApplication([('/', MainHandler)],
                                         debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
