"""
Collection of simple 'static' handlers, which just render templates.
"""

from base import BaseHandler


class MainHandler(BaseHandler):
    """Homepage"""

    def get(self):
        """GET request"""
        self.render_template('index.html')


class AboutHandler(BaseHandler):
    """About page"""

    def get(self):
        """GET request"""
        self.render_template('about.html')
