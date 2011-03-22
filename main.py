#!/usr/bin/env python

import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util, template


TEMPLATE_DIR=os.path.join(os.path.dirname(__file__), 'templates/')

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

def main():
    """main"""

    application = webapp.WSGIApplication([('/', MainHandler),
                                        ], debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
