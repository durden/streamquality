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


class Tweet(db.Model):
    """Tweet"""

    # Use strings since id's are really big and can truncate in several
    # instances
    id = db.StringProperty(required=True)
    author_user_name = db.StringProperty(required=True)
    author_real_name = db.StringProperty(required=True)
    author_profile_image_url = db.StringProperty(required=True)
    text = db.StringProperty(required=True)


class Vote(db.Model):
    """Vote on a particular tweet"""

    voter = db.ReferenceProperty(SQUser)
    count = db.IntegerProperty(required=True)
    tweet = db.ReferenceProperty(Tweet)
