"""
Handler to deal with voting on tweets.
"""

import datetime

from django.utils import simplejson

from app.models import Tweet, Vote as VoteModel
from app.handlers.base import BaseHandler, NotLoggedIn


class Vote(BaseHandler):
    """Vote on tweets"""

    def get(self, page=1):
        """Interface for logged in user to vote"""

        # Get 20 most recent tweets from friends/user
        url = ''.join(
                ['http://api.twitter.com/1/statuses/home_timeline.json'])

        try:
            (status_code, timeline) = self.send_twitter_request(url,
                                        additional_params={'page': page})
        except NotLoggedIn:
            return self.render_template('error.html', msg="Must be logged in")

        if status_code != 200:
            return self.render_template('error.html',
                            msg='Status %d returned' % (status_code))

        tweets = []
        user = self.get_logged_in_user()
        votes = VoteModel.all().filter('voter = ', user)

        for entry in timeline:
            tweet = {}

            tweet['profile_image_url'] = entry['user']['profile_image_url']
            tweet['author_screen_name'] = entry['user']['screen_name']
            tweet['author_name'] = entry['user']['name']
            tweet['text'] = entry['text']
            tweet['id'] = entry['id_str']
            tweet['vote_cnt'] = 0
            tweet['created_at'] = datetime.datetime.strptime(
                            entry['created_at'], "%a %b %d %H:%M:%S +0000 %Y")

            for vote in votes:
                if vote.tweet.id == entry['id_str']:
                    tweet['vote_cnt'] = vote.count

            tweets.append(tweet)

        self.render_template('vote.html', user_name=user.user_name,
                             tweets=tweets, page=page)


class VoteTweet(BaseHandler):
    """Base class for voting on a tweet"""

    def vote(self, tweet_id, count):
        """Process a vote 'up' for given user_name on given tweet"""

        tweet_info = self.get_tweet_info(tweet_id)
        if tweet_info is None:
            raise Exception

        # FIXME: Handle error in AJAX request?
        user = self.get_logged_in_user()
        if user is None:
            return None

        tweet = Tweet.get_or_create(tweet_info)
        return VoteModel.get_or_create(user, tweet, count)


class VoteUp(VoteTweet):
    """Handle voting up a tweet"""

    def get(self, tweet_id):
        """Process a vote 'up' on given tweet"""

        new_vote = self.vote(tweet_id, 1)
        self.response.out.write(simplejson.dumps({'vote_cnt': new_vote.count,
                                                  'id': new_vote.tweet.id}))


class VoteDown(VoteTweet):
    """Handle voting down a tweet"""

    def get(self, tweet_id):
        """Process a vote 'down' on given tweet"""

        new_vote = self.vote(tweet_id, -1)
        self.response.out.write(simplejson.dumps({'vote_cnt': new_vote.count,
                                                  'id': new_vote.tweet.id}))


class MyVotes(VoteTweet):
    """Show logged in user tweets they've voted on grouped by author"""

    def get(self, author=""):
        """Show votes logged in user has optionally filtered by author"""

        user = self.get_logged_in_user()
        if user is None:
            return self.render_template('error.html', msg="Must be logged in")

        if author != "":
            tweets = VoteModel.get_votes_by_author(user, author)
            return self.render_template('vote.html', user_name=user.user_name,
                                        tweets=tweets)

        votes = VoteModel.aggregate_votes_by_author(user, author)
        self.render_template('myvotes.html', user_name=user.user_name,
                                votes=votes)
