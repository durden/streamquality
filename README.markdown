# About
Simple [Google AppEngine](http://code.google.com/appengine/) application to
help twitter users rate recent tweets from the people they follow.

[Live prototype](http://streamquality.appspot.com/) :be aware that I don't
claim this link will always point to a functional version of the code ;)

## Inspiration/Goals
What I hope to solve and ideas on how.  Feel free to fork away and do
something completely different, but send me a pull request or message so I can
see what awesome ideas everyone has!

### Problem
Difficult to gain insight into which of your followers add value to your stream.

### Solution
Allow users to view individual tweets from their followers and vote on them.

#### Detailed mission statement
When going through the stream there is a lot of noise once your start
following a number of users.   This creates a tendency to subconsciously skip
over tweets form certain users since they rarely add any value to your daily
life.  Tweets are really short and skipping over something isn't hard or
terribly time consuming, but wouldn't it be better to follow less people and
better content?

Maybe you should spend a little bit of time each week culling over who you
follow and cutting the fat.  This is really no different than getting to inbox
zero or deleting rss feeds.  The point of this service is to provide twitter
users with a place to rate and review the content their follow choices.  

Over time users can see that they don't seem to ever find any value in a
particular user or very little value relative to the rest of their stream.
The service can then begin to suggest who you should consider unfollowing.

##### Requirements for MVP
Show random tweet from a person you follow
Allow user to vote up/down
Interface to unfollow user

##### Interface Ideas
Show 10 tweets from 10 different users that person follows each with a thumbs
up or down. Let user submit that and then ask if they want 10 more to vote on.
Don't make judgement on who to follow until a user has been voted on a min of
5 times total.

###### Future Ideas
Crowd source data from other users so that you get a more accurate picture of a
person anymore data without a single person from having to vote a billion
times.
