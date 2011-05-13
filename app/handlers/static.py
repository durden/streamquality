"""
Collection of simple 'static' handlers, which just render templates.
"""

from base import BaseHandler


class Main(BaseHandler):
    """Homepage"""

    def get(self):
        """GET request"""
        self.render_template('index.html')


class About(BaseHandler):
    """About page"""

    def get(self):
        """GET request"""
        self.render_template('about.html')


class Missing(BaseHandler):
    """404 page"""

    def get(self):
        """GET request"""
        self.render_template('error.html')
