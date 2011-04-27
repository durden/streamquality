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


class Vote(db.Model):
    """Vote on a particular tweet"""

    voter = db.ReferenceProperty(SQUser)
    count = db.IntegerProperty(required=True)

    # Use strings since id's are really big and can truncate in several
    # instances
    tweet_id = db.StringProperty(required=True)

    # user_name of author of tweet voted on
    tweet_author = db.StringProperty(required=True)
    tweet_text = db.StringProperty(required=True)
