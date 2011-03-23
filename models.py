"""
Models
"""


from google.appengine.ext import db

class SQUser(db.Model):
    """User of stream quality service"""

    oauth_secret = db.StringProperty(required=True)
    oauth_token = db.StringProperty(required=True)
    real_name = db.StringProperty(required=True)
    user_name = db.StringProperty(required=True)
