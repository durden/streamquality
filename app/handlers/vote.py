"""
Handler to deal with voting on tweets.
"""

from django.utils import simplejson

from app.models import Vote as VoteModel
from app.models import SQUser

from base import BaseHandler

# FIXME
debug = True

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

        if not self.logged_in(user_name) and not debug:
            return self.redirect('/')

        user = SQUser.all().filter('user_name = ', user_name).fetch(1)[0]

        for tweet in tweets:
            try:
                vote = VoteModel.all().filter('voter = ', user)\
                                        .filter('tweet_id = ',
                                                tweet['id_str']).fetch(1)[0]
                tweet['vote_cnt'] = vote.count
            # Not found
            except IndexError:
                tweet['vote_cnt'] = 0

        self.render_template('vote.html', user_name=user_name, tweets=tweets,
                                logged_in=1)


class VoteTweet(BaseHandler):
    """Base class for voting on a tweet"""

    def vote(self, user_name, tweet_id, count):
        """Process a vote 'up' for given user_name on given tweet"""

        (author, text) = self.get_tweet_info(user_name, tweet_id)
        if author is None or text is None:
            raise Exception

        # Safe to use here w/o exception b/c exception would have been thrown
        # when sending above request
        user = SQUser.all().filter('user_name = ', user_name).fetch(1)[0]

        # FIXME: Check if a vote already exists
        vote = VoteModel(voter=user, count=count, tweet_id=tweet_id,
                        tweet_author=author, tweet_text=text)
        vote.put()
        return vote


class VoteUp(VoteTweet):
    """Handle voting up a tweet"""

    def get(self, user_name, tweet_id):
        """Process a vote 'up' for given user_name on given tweet"""

        new_vote = self.vote(user_name, tweet_id, 1)
        self.response.out.write(simplejson.dumps({'vote_cnt': new_vote.count,
                                                  'id': new_vote.tweet_id}))

class VoteDown(VoteTweet):
    """Handle voting down a tweet"""

    def get(self, user_name, tweet_id):
        """Process a vote 'up' for given user_name on given tweet"""

        new_vote = self.vote(user_name, tweet_id, -1)
        self.response.out.write(simplejson.dumps({'vote_cnt': new_vote.count,
                                                  'id': new_vote.tweet_id}))
