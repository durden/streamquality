"""
Handler to deal with voting on tweets.
"""

from app.models import Vote as VoteModel
from base import BaseHandler


class Vote(BaseHandler):
    """Vote on tweets"""

    def get(self, user_name):
        """Interface for given user to vote"""

        # Get 20 most recent tweets from friends/user
        url = ''.join(
                ['http://api.twitter.com/1/statuses/friends_timeline.json'])

        (status_code, tweets) = self.send_twitter_request(user_name, url)

        if status_code != 200:
            self.render_template('vote.html',
                            msg='Status %d returned' % (status_code))
            return

        self.render_template('vote.html', user_name=user_name, tweets=tweets)


class VoteUp(BaseHandler):
    def get(self, user_name, tweet_id):
        """Process a vote 'up' for given user_name on given tweet"""

        tid = int(tweet_id)
        url = ''.join(
            ['http://api.twitter.com/1/statuses/show/%d.json' % (tid)])

        (status_code, tweet) = self.send_twitter_request(user_name, url)

        if status_code != 200:
            self.render_template('vote.html',
                            msg='Status %d returned' % (status_code))
            return

        # FIXME: Make sure it doesn't exist first
        vote = VoteModel(count=1, tweet_id=tid,
                        tweet_author=tweet['user']['name'])
        vote.put()

        # FIXME: Check if a vote already exists
        self.render_template('vote.html', user_name=user_name)
