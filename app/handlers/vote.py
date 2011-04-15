"""
Handler to deal with voting on tweets.
"""

import oauth

from google.appengine.api import urlfetch
from django.utils import simplejson

from base import LocalHandler, CONSUMER_KEY, CALLBACK_URL, CONSUMER_SECRET
from app.models import SQUser


class VoteHandler(LocalHandler):
    """Vote on tweets"""

    def get(self, user_name):
        """Interface for given user to vote"""

        # FIXME: Authenticate user
        try:
            user = SQUser.all().filter('user_name = ', user_name).fetch(1)[0]
        except IndexError:
            self.render_template('vote.html', msg="%s not found" % (user_name))
            return

        # Get 20 most recent tweets from friends/user
        url = ''.join(
                ['http://api.twitter.com/1/statuses/friends_timeline.json'])

        client = oauth.TwitterClient(CONSUMER_KEY, CONSUMER_SECRET,
                                     CALLBACK_URL)
        result = client.make_request(url, token=user.oauth_token,
                                    secret=user.oauth_secret,
                                    additional_params=None,
                                    method=urlfetch.GET)

        if result.status_code != 200:
            self.render_template('vote.html',
                            msg='Status %d returned %s' % (result.status_code,
                            result.content))
            return

        tweets = simplejson.loads(result.content)
        self.render_template('vote.html', user_name=user_name, tweets=tweets)
