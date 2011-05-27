"""
Models
"""

import datetime

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
    text = db.StringProperty(required=True, multiline=True)
    created_at = db.DateTimeProperty(required=True)

    @staticmethod
    def get_or_create(tweet_info):
        """Get tweet with given id or create/return it"""

        try:
            tweet = Tweet.all().filter('id = ', tweet_info['id']).fetch(1)[0]
        except IndexError:
            tweet = Tweet(id=tweet_info['id'],
                    author_profile_image_url=tweet_info['profile_image_url'],
                    author_real_name=tweet_info['real_name'],
                    author_user_name=tweet_info['user_name'],
                    text=tweet_info['text'],
                    created_at=datetime.datetime.strptime(
                                                tweet_info['created_at'],
                                                "%a %b %d %H:%M:%S +0000 %Y"))
            tweet.put()

        return tweet

class Vote(db.Model):
    """Vote on a particular tweet"""

    voter = db.ReferenceProperty(SQUser)
    count = db.IntegerProperty(required=True)
    tweet = db.ReferenceProperty(Tweet)

    @staticmethod
    def get_or_create(voter, tweet, count):
        """Get vote associated with given tweet or create/return it"""
        try:
            vote = Vote.all().filter('voter = ', voter).filter('tweet = ',
                                                            tweet).fetch(1)[0]
            vote.count = count
        except IndexError:
            vote = Vote(voter=voter, count=count, tweet=tweet)

        vote.put()
        return vote

    @staticmethod
    def get_votes_by_author(voter, author):
        """Get all votes for a given voter and tweet author"""

        db_votes = Vote.all().filter('voter = ', voter)
        tweets = []

        for vote in db_votes:
            tweet = {}

            if vote.tweet.author_user_name != author:
                continue

            tweet['profile_image_url'] = vote.tweet.author_profile_image_url
            tweet['author_name'] = vote.tweet.author_real_name
            tweet['author_screen_name'] = vote.tweet.author_user_name
            tweet['text'] = vote.tweet.text
            tweet['id'] = vote.tweet.id
            tweet['vote_cnt'] = vote.count
            tweet['created_at'] = vote.tweet.created_at

            tweets.append(tweet)

        return tweets

    @staticmethod
    def aggregate_votes_by_author(voter, author):
        """Aggregate votes for a given voter and tweet author"""

        db_votes = Vote.all().filter('voter = ', voter)
        votes = {}

        for vote in db_votes:
            try:
                votes[vote.tweet.author_user_name] += vote.count
            except KeyError:
                votes[vote.tweet.author_user_name] = vote.count

        return votes
