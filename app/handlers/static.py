"""
Collection of simple 'static' handlers, which just render templates.
"""

from base import LocalHandler


class MainHandler(LocalHandler):
    """Homepage"""

    def get(self):
        """GET request"""
        self.render_template('index.html')


class AboutHandler(LocalHandler):
    """About page"""

    def get(self):
        """GET request"""
        self.render_template('about.html')
